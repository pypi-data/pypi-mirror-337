import aceutils.database_management as dbm
import acedeploy.extensions.permissions as permissions
import setup
import logging
import os

from aceutils.logger import LoggingAdapter, DefaultFormatter


logger = logging.getLogger("acedeploy")
logging.getLogger("acedeploy.services.snowflake_service").setLevel(logging.CRITICAL)
logger.setLevel(logging.DEBUG)
log = LoggingAdapter(logger)

sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(DefaultFormatter())
logger.addHandler(sh)

setup.setup()
snow_client = dbm.get_client_from_config()

permissions.set_permissions_on_database(
    snow_client=snow_client,
    template_path=os.path.join(os.path.dirname(__file__), "permissions.sql.jinja"),
    database_name="P_TEST1",
    schema_list={"blacklist": ["PUBLIC"]},
)
