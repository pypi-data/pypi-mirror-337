import aceutils.database_management as dbm
import aceutils.file_util as file_util
import setup
import os
import ptvsd
import datetime
import logging
import random

from aceutils.logger import (
    LoggingAdapter,
    LogFileFormatter,
    DevOpsFormatter,
    DefaultFormatter,
)

logger = logging.getLogger("acedeploy")
logging.getLogger("acedeploy.services.snowflake_service").setLevel(logging.CRITICAL)
logger.setLevel(logging.DEBUG)
log = LoggingAdapter(logger)

sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(DefaultFormatter())
logger.addHandler(sh)

start_time = datetime.datetime.now()
log.info("Start time: {}".format(start_time))


def main():
    setup.setup()
    snow_client = dbm.get_client_from_config()
    for transient_tables in [False, True]:
        refreshed_tables = dbm.refresh_by_json(
            source_database_name="ACEDEPLOY_TARGET_DB",
            target_database_name="REFRESH_TARGET",
            json_file="examples/scripts/nightly_clone_refresh.json",
            snow_client=snow_client,
            old_table_suffix="_OLD_{}".format(random.randint(0, 10000)),
            overwrite_existing=False,
            ignore_metadata_differences=False,
            ignore_retention_time=True,
            ignore_comment=True,
            transient_tables=transient_tables,
        )

    log.info(f"Refreshed Tables: {refreshed_tables}")

    config = file_util.load_json("examples/scripts/nightly_clone_refresh.json")
    schema_list = list(config["schemasToClone"].keys())
    dbm.resume_reclustering_in_schemas(
        database_name="REFRESH_TARGET", schema_list=schema_list, snow_client=snow_client
    )


if __name__ == "__main__":
    main()

end_time = datetime.datetime.now()
log.info("End time: {}".format(end_time))
log.info("Elapsed: {}".format(end_time - start_time))
