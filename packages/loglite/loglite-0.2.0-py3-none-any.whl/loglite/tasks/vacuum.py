from loguru import logger

from datetime import datetime, timedelta
from loglite.config import Config
from loglite.database import Database
from loglite.types import QueryFilter
from loglite.utils import bytes_to_mb, repeat_every


async def __remove_stale_logs(db: Database, max_age_days: int) -> int:
    now = datetime.now()
    cutoff_dtime = now - timedelta(days=max_age_days)
    min_timestamp = await db.get_min_timestamp()
    if min_timestamp.timestamp() > cutoff_dtime.timestamp():
        return 0

    filters: list[QueryFilter] = [
        {"field": "timestamp", "operator": "<=", "value": cutoff_dtime.isoformat()}
    ]
    n = await db.delete(filters)
    await db.vacuum()
    await db.wal_checkpoint("FULL")
    return n


async def __remove_excessive_logs(
    db: Database, max_size_mb: float, target_size_mb: float, batch_size: int
) -> int:
    db_size = await db.get_size_mb()
    if db_size <= max_size_mb:
        return 0

    min_id = await db.get_min_log_id()
    max_id = await db.get_max_log_id()
    rowcount = max_id - min_id + 1

    # Calculate the percentage of logs to remove
    remove_ratio = (db_size - target_size_mb) / db_size
    remove_max_id = min_id + int(rowcount * remove_ratio) - 1
    remove_count = remove_max_id - min_id + 1
    removed = 0

    # Remove the oldest logs up to the calculated threshold, in multiple chunks to avoid transaction
    # log bloat up
    logger.opt(colors=True).info(
        f"<y>[Log cleanup] db size = {db_size}MB, limit size = {max_size_mb}MB, target size = {target_size_mb}MB. "
        f"removing logs id between {min_id} and {remove_max_id} (n={remove_count}, pct={(100 * remove_ratio):.2f}%)</y>"
    )
    for start_id in range(min_id, remove_max_id, batch_size):
        end_id = min(start_id + batch_size - 1, remove_max_id)
        filters: list[QueryFilter] = [
            {"field": "id", "operator": "<=", "value": end_id}
        ]
        removed += await db.delete(filters)
        logger.opt(colors=True).info(
            f"<y>[Log cleanup] ... already removed {removed} entries</y>"
        )

    await db.vacuum()
    await db.wal_checkpoint("FULL")
    return removed


async def register_database_vacuuming_task(db: Database, config: Config):
    @repeat_every(seconds=(interval := config.task_vacuum_interval))
    async def _task():
        # Do checkpoint to make sure we can then get an accurate estimate of the database size
        await db.wal_checkpoint()

        # Remove logs older than `vacuum_max_days`
        columns = await db.get_log_columns()
        has_timestamp_column = any(
            column["name"] == config.log_timestamp_field for column in columns
        )
        if not has_timestamp_column:
            logger.warning(
                f"log_timestamp_field: {config.log_timestamp_field} not found in columns, "
                "unable to remove stale logs based on timestamp"
            )
        else:
            n = await __remove_stale_logs(db, config.vacuum_max_days)
            if n > 0:
                logger.opt(colors=True).info(
                    f"<r>[Log cleanup] removed {n} stale logs entries (max retention days = {config.vacuum_max_days})</r>"
                )

        # Remove logs if whatever remains still exceeds `vacuum_max_size`
        n = await __remove_excessive_logs(
            db,
            bytes_to_mb(config.vacuum_max_size_bytes),
            bytes_to_mb(config.vacuum_target_size_bytes),
            config.vacuum_delete_batch_size,
        )

        if n > 0:
            db_size = await db.get_size_mb()
            logger.opt(colors=True).info(
                f"<r>[Log cleanup] removed {n} logs entries, database size is now {db_size}MB</r>"
            )

    logger.opt(colors=True).info(
        f"<e>database vacuuming task interval: {interval}s</e>"
    )
    await _task()
