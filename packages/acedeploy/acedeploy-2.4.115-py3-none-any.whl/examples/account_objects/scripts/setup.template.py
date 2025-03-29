import os
import random


def setup():
    # path to deployment file
    os.environ[
        "ACEACCOUNT_CONFIG_PATH"
    ] = "./examples/account_objects/solutions/demo1/config.json"

    os.environ["SNOWFLAKE_EDITION"] = "Enterprise"
    os.environ["SNOWFLAKE_ACCOUNT"] = "xy1245.west-europe.azure"
    os.environ["SNOWFLAKE_USER"] = "U_ACEDEPLOY_ACCOUNT_OBJECTS"
    os.environ["SNOWFLAKE_PASSWORD"] = "123"
    os.environ["SNOWFLAKE_ROLE"] = "R_ACEDEPLOY_ACCOUNT_OBJECTS"
    os.environ["SNOWFLAKE_WAREHOUSE"] = "WH_ACEDEPLOY"


if __name__ == "__main__":
    setup()
