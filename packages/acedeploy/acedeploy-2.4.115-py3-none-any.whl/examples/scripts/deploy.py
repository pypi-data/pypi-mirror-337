import os, sys

current_working_dir = os.getcwd()
sys.path.append(current_working_dir)

import acedeploy.main as acedeploy_client
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

logs_folder = "test/logs"
if not os.path.exists(logs_folder):
    os.makedirs(logs_folder)
fh = logging.FileHandler("{}/{:%Y-%m-%d}.log".format(logs_folder, datetime.datetime.now()))
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
    acedeploy_client.execute_deployment(config)


if __name__ == "__main__":
    main()

end_time = datetime.datetime.now()
log.info("End time: {}".format(end_time))
log.info("Elapsed: {}".format(end_time - start_time))
