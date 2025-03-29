import os
import random


def setup():
    # path to deployment file
    os.environ[
        "ACEDEPLOY_CONFIG_PATH"
    ] = "examples/solutions/MINIMAL_EXAMPLE/deployment.json"
    # path of solution root
    os.environ["PROJECT_FOLDER"] = "examples/solutions/MINIMAL_EXAMPLE"
    # path to git repository root
    os.environ["ACEDEPLOY_SOLUTION_ROOT"] = ""

    # deployment mode: validate, develop, release
    os.environ["ACEDEPLOY_DEPLOYMENT_MODE"] = "develop"
    os.environ["ACEDEPLOY_RELEASE_NAME"] = "{}.{}.{}".format(
        random.randint(0, 10), random.randint(0, 10), random.randint(0, 100)
    )

    os.environ["ACEDEPLOY_REPO_TAG_REGEX"] = "^t[0-9]+$"
    os.environ["ACEDEPLOY_PARALLEL_THREADS"] = "10"
    os.environ["ACTION_SUMMARY_PATH"] = "./test/action_summary.txt"
    os.environ["ACTION_JSON_PATH"] = "./test/action_json.txt"

    os.environ["ACEDEPLOY_IGNORE_GIT_INFORMATION"] = "true"
    os.environ["ACEDEPLOY_DROP_OBJECTS_IF_NOT_IN_PROJECT"] = "false"
    os.environ["ACEDEPLOY_STOP_AT_DATALOSS"] = "true"

    os.environ["ACEDEPLOY_DEPLOY_TO_CLONE"] = "false"
    os.environ["ACEDEPLOY_CLONE_MODE"] = "minimal"
    os.environ["ACEDEPLOY_DROP_CLONE_AFTER_RUN"] = "true"

    os.environ["ACEDEPLOY_HANDLE_POLICY_ASSIGNMENTS"] = "false"
    os.environ["ACEDEPLOY_POLICY_ASSIGNMENTS_PROJECT"] = "PROJECT1"
    os.environ["ACEDEPLOY_POLICY_ASSIGNMENTS_DEPLOYMENT_DB"] = "ACEDEPLOY_TARGET_DB"
    os.environ["ACEDEPLOY_POLICY_ASSIGNMENTS_ROLE"] = ""
    os.environ["ACEDEPLOY_POLICY_ASSIGNMENTS_REPO_PATH"] = ""
    os.environ["ACEDEPLOY_POLICY_ASSIGNMENTS_CONFIG_FILE_PATH"] = "./examples/policies/account1_config.json"
    os.environ["ACEDEPLOY_POLICY_ASSIGNMENTS_SAVE_INFO"] = "true"
    os.environ["ACEDEPLOY_POLICY_ASSIGNMENTS_INFO_OUTPUT_FOLDER_PATH"] = "./test/policies/"
    os.environ["ACEDEPLOY_POLICY_ASSIGNMENTS_CREATE_AZURE_PULL_REQUEST_COMMENTS"] = "true"

    os.environ["ACEDEPLOY_EXECUTE_IN_PARALLEL_SESSIONS"] = "true"

    os.environ["ACEDEPLOY_RESUME_TASKS"] = "true"
    os.environ["ACEDEPLOY_REAPPLY_EXISTING_POLICIES"] = "false"

    os.environ["META_DB"] = "ACEDEPLOY_META_DB"
    os.environ["TARGET_DB"] = "ACEDEPLOY_TARGET_DB"
    # os.environ["TARGET_DB"] = "ACEDEPLOY_TARGET_DB_CLONE_{}".format(random.randint(0, 10000))
    os.environ["CLONE_SOURCE_DB"] = "ACEDEPLOY_TARGET_DB"

    os.environ["TARGET_DB_RETENTION_TIME"] = "10"
    os.environ["TEMP_DB_RETENTION_TIME"] = "1"

    os.environ["ACEDEPLOY_DETAILED_OUTPUT"] = "true"

    os.environ["SNOWFLAKE_EDITION"] = "Enterprise"
    os.environ["SNOWFLAKE_ACCOUNT"] = "xy1245.west-europe.azure"
    os.environ["SNOWFLAKE_USER"] = "U_ACEDEPLOY"
    os.environ["SNOWFLAKE_PASSWORD"] = "123"
    os.environ["SNOWFLAKE_PRIVATE_KEY"] = "-----BEGINENCRYPTEDPRIVATEKEY-----123-----ENDENCRYPTEDPRIVATEKEY-----"
    os.environ["SNOWFLAKE_PRIVATE_KEY_PASS"] = "123"
    os.environ["SNOWFLAKE_ROLE"] = "R_ACEDEPLOY"
    os.environ["SNOWFLAKE_WAREHOUSE"] = "WH_ACEDEPLOY"

    os.environ["MY_VAR_NAME"] = "VAR_FROM_ENV"
    os.environ["MY_VAR_VALUE"] = "VAL_FROM_ENV"
    os.environ["MY_REPLACE_VAR_NAME"] = "VAR_FROM_ENV_2"
    os.environ["MY_REPLACE_VAR_VALUE"] = "VAL_FROM_ENV_2"


if __name__ == "__main__":
    setup()
