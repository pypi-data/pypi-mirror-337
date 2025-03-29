import setup
import datetime
import logging

from acedeploy.extensions.smoketest import Smoketest
from aceutils.database_management import get_client_from_config
from aceutils.logger import LoggingAdapter, DefaultFormatter

logger = logging.getLogger("acedeploy")
logging.getLogger("acedeploy.services.snowflake_service").setLevel(logging.CRITICAL)
logger.setLevel(logging.DEBUG)
log = LoggingAdapter(logger)

sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(DefaultFormatter())
logger.addHandler(sh)

start_time = datetime.datetime.now()
log.info(f"Start time: {start_time}")


def main():
    setup.setup()
    snow_client = get_client_from_config()
    smoketest = Smoketest(
        snow_client,
        smoketest_config_file="examples/scripts/smoketest.json",
        results_file="test/smoketest_output.json",
    )
    smoketest.start_smoketest()


if __name__ == "__main__":
    main()

end_time = datetime.datetime.now()
log.info(f"End time: {end_time}")
log.info(f"Elapsed: {end_time - start_time}")
