import acedeploy.extensions.comparer as acedeploy_compare
import setup
import os
import datetime
import logging

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
    config = acedeploy_compare.configure()
    acedeploy_compare.compare_files_and_database(config, True)


if __name__ == "__main__":
    main()

end_time = datetime.datetime.now()
log.info("End time: {}".format(end_time))
log.info("Elapsed: {}".format(end_time - start_time))
