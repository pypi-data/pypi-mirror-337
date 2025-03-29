import os, sys

current_working_dir = os.getcwd()
sys.path.append(current_working_dir)

from aceservices.snowflake_service import SnowClient, SnowClientConfig
import acedeploy.main as acedeploy_client
from aceutils.database_management import alter_policy_assignments
import setup
import os
import datetime
import logging

from aceutils.logger import (
    LoggingAdapter,
    LogFileFormatter,
    DevOpsFormatter,
    DefaultFormatter,
    SnowflakeTableHandler,
    SnowflakeConnection,
)

setup.setup()

logger = logging.getLogger("acedeploy")
logger.setLevel(logging.DEBUG)
log = LoggingAdapter(logger)

fh = logging.FileHandler("test/logs/{:%Y-%m-%d}.log".format(datetime.datetime.now()))
fh.setLevel(logging.DEBUG)
fh_formatter = LogFileFormatter()
fh.setFormatter(fh_formatter)
logger.addHandler(fh)

# # log to a snowflake table - might slow down deployment by 50%
# sf_connection = SnowflakeConnection(
# 	account = os.environ["SNOWFLAKE_ACCOUNT"],
#     user = os.environ["SNOWFLAKE_USER"],
#     password = os.environ["SNOWFLAKE_PASSWORD"],
#     role = "R_LOGGER",
#     warehouse = os.environ["SNOWFLAKE_WAREHOUSE"]
# )
# th = SnowflakeTableHandler(sf_connection, 'logging.log.log', os.environ["ACEDEPLOY_RELEASE_NAME"])
# th.setLevel(logging.INFO)
# logger.addHandler(th)

sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(DefaultFormatter())
logger.addHandler(sh)

start_time = datetime.datetime.now()
log.info("Start time: {}".format(start_time))


def main():
    config = acedeploy_client.configure()
    snow_client_target = SnowClient(
        SnowClientConfig.get_from_solution_config(config, config.database_target)
    )
    alter_policy_assignments(
        snow_client_target,
        ["schema_1.table_1","DATA.TABLE7"],
        'TABLE',
        'ACEDEPLOY_TARGET_DB',
        'PROJECT1',
        "./examples/policies/account1_config.json",
        ''
        )



if __name__ == "__main__":
    main()

end_time = datetime.datetime.now()
log.info("End time: {}".format(end_time))
log.info("Elapsed: {}".format(end_time - start_time))
