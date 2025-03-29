# PYTHON POSTDEPLOYMENT STEPS ARE CURRENTLY NOT ALLOWED BY THE FRAMEWORK

# when this script is called as a postdeployment step, the first argument (argv[1])
# contains the snowflake connection information as a json string

import snowflake.connector
import sys
import json

print("This is a demo script")
snowflake_config = json.loads(sys.argv[1])
connection = snowflake.connector.connect(**snowflake_config)

statement = (
    "CREATE SCHEMA IF NOT EXISTS TEST; CREATE OR REPLACE TABLE TEST.TEST (id INT);"
)
connection.execute_string(statement)

print("Demo script finished")
