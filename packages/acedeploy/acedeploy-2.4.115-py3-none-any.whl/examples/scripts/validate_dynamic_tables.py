import os, sys

current_working_dir = os.getcwd()
sys.path.append(current_working_dir)

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
    # Validate Dynamic Tables (on SOURCE_DB) - Refresh Warehouses Environment Handling
    regex_pattern_warehouse_source_env = r'(?P<prefix>WH_.*?)(?P<env>_P_)(?P<suffix>.*)$'
    target_env_abbreviation = r'\g<prefix>_D_\g<suffix>'
    regex_pattern_warehouse_target_env = r'(?P<prefix>WH_.*?)(?P<env>_D_)(?P<suffix>.*)$'
    dbm.alter_dynamic_tables(
        database_name = "ACEDEPLOY_TARGET_DB",
        target_env_abbreviation = target_env_abbreviation,
        regex_pattern_warehouse_source_env = regex_pattern_warehouse_source_env,
        snow_client = snow_client,
        execute_statements = False,
        regex_pattern_warehouse_target_env = regex_pattern_warehouse_target_env
    )


if __name__ == "__main__":
    main()

end_time = datetime.datetime.now()
log.info("End time: {}".format(end_time))
log.info("Elapsed: {}".format(end_time - start_time))
