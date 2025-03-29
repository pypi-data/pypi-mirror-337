# this script retrieves all DDLs from a snowflake database and stores each object in a separate file
# - the output is compatible with the acedeploy framework
# - supported object: schemas, views(1), tables, procedures, functions, file formats(2) pipes, tasks(3), streams(4) (other objects are ignored)
#     (1)materialized views will be included, but require fixing of the CREATE statement
#     (2)file formats will be included, but require fixing of the CREATE statement
#     (3)tasks need to be edited manually, as they will contain database references
#     (4)streams need to be edited manually, as the referenced tables will be missing the schema name
# - unsupported:
#   - recursive view (will create a file, but object name will contain errors)
#   - objects where the names contain characters not in [a-zA-Z0-9_$]
# - files in output folder will be overwritten without asking
# install dependencies with `pip install -r requirements.txt`
# create a file setup.py to set the connection info (you can use setup.template.py as a template) and enter the required information
# run this script to get the files `python3 load_and_parse_ddls.py`
# you will need to manually review the generated files

import os
import re

import aceservices.snowflake_service as snowflake_service
import setup
from progress.bar import Bar as ProgressBar

snf_config = snowflake_service.SnowClientConfig(
    account=setup.SNOWFLAKE_ACCOUNT,
    user=setup.SNOWFLAKE_USER,
    password=setup.SNOWFLAKE_PASSWORD,
    warehouse=setup.SNOWFLAKE_WAREHOUSE,
    role=setup.SNOWFLAKE_ROLE,
    database=setup.database,
)
snf_client = snowflake_service.SnowClient(snf_config)
snf_client.execute_statement("ALTER SESSION SET QUOTED_IDENTIFIERS_IGNORE_CASE=false;")

schema_ignore_list = ", ".join(
    [f"'{s.upper()}'" for s in setup.schema_blacklist + ["INFORMATION_SCHEMA"]]
)

object_mapping = [
    {
        "type": "VIEW",
        "foldername": "Views",
        "query": f'SELECT TABLE_SCHEMA AS "schema_name", TABLE_NAME AS "name" FROM {setup.database}.INFORMATION_SCHEMA.VIEWS WHERE "schema_name" NOT IN ({schema_ignore_list})',
    },
    {
        "type": "TABLE",
        "foldername": "Tables",
        "query": f'SELECT TABLE_SCHEMA AS "schema_name", TABLE_NAME AS "name" FROM {setup.database}.INFORMATION_SCHEMA.TABLES WHERE "schema_name" NOT IN ({schema_ignore_list}) AND TABLE_TYPE != \'VIEW\'',
    },
    {
        "type": "FUNCTION",
        "foldername": "Functions",
        "query": f'SELECT FUNCTION_SCHEMA AS "schema_name", FUNCTION_NAME AS "name", ARGUMENT_SIGNATURE FROM {setup.database}.INFORMATION_SCHEMA.FUNCTIONS WHERE "schema_name" NOT IN ({schema_ignore_list})',
    },
    {
        "type": "PROCEDURE",
        "foldername": "Procedures",
        "query": f'SELECT PROCEDURE_SCHEMA AS "schema_name", PROCEDURE_NAME AS "name", ARGUMENT_SIGNATURE FROM {setup.database}.INFORMATION_SCHEMA.PROCEDURES WHERE "schema_name" NOT IN ({schema_ignore_list})',
    },
    {
        "type": "FILE_FORMAT",
        "foldername": "Fileformats",
        "query": f'SELECT FILE_FORMAT_SCHEMA AS "schema_name", FILE_FORMAT_NAME AS "name" FROM {setup.database}.INFORMATION_SCHEMA.FILE_FORMATS WHERE "schema_name" NOT IN ({schema_ignore_list})',
    },
    {
        "type": "PIPE",
        "foldername": "Pipes",
        "query": f'SELECT PIPE_SCHEMA AS "schema_name", PIPE_NAME AS "name" FROM {setup.database}.INFORMATION_SCHEMA.PIPES WHERE "schema_name" NOT IN ({schema_ignore_list})',
    },
    {
        "type": "TASK",
        "foldername": "Tasks",
        "query": f"SHOW TASKS IN DATABASE {setup.database};",
    },
    {
        "type": "STREAM",
        "foldername": "Streams",
        "query": f"SHOW STREAMS IN DATABASE {setup.database};",
    },
    {
        "type": "SEQUENCE",
        "foldername": "Sequences",
        "query": f"SHOW SEQUENCES IN DATABASE {setup.database};",
    },
]


def save_file(folder, filename, content):
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(os.path.join(folder, filename), "w", encoding="utf8") as f:
        f.write(content)


def add_schema_to_ddl(ddl, schema, use_replace_or_replace=True):
    ddl_stripped = ddl.strip()
    expression = r'(?:create\s+or\s+replace|create){1}\s+(?P<type>[a-zA-Z0-9_]+)\s+(?:"?[a-zA-Z0-9_$]+"?\.)?"?(?P<name>[a-zA-Z0-9_$]+)"?'
    if use_replace_or_replace:
        replace = r"CREATE OR REPLACE \g<type> {schema}.\g<name>".format(schema=schema)
    else:
        replace = r"CREATE \g<type> {schema}.\g<name>".format(schema=schema)
    return re.sub(expression, replace, ddl_stripped, flags=re.IGNORECASE | re.MULTILINE)


# get schemas
query = f"SELECT SCHEMA_NAME FROM {setup.database}.INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME NOT IN ({schema_ignore_list})"
result = snf_client.execute_query(query)
progress_bar = ProgressBar(
    "Getting Schemas", max=len(result), suffix="%(index)d/%(max)d - ETA: %(eta)ds"
)
for r in result:
    ddl = f"CREATE SCHEMA {r['SCHEMA_NAME']};"
    schema_folder = os.path.join(setup.output_folder, r["SCHEMA_NAME"])
    save_file(schema_folder, f"{r['SCHEMA_NAME']}.sql", ddl)
    progress_bar.next()
progress_bar.finish()

# get objects
for obj_map in object_mapping:
    result = snf_client.execute_query(obj_map["query"])
    progress_bar = ProgressBar(
        f"Getting {obj_map['foldername']}",
        max=len(result),
        suffix="%(index)d/%(max)d - ETA: %(eta)ds",
    )
    for r in result:
        if f"{r['schema_name']}.{r['name']}" in setup.skip_objects:
            progress_bar.next()
            continue
        argument_signature = r.get("ARGUMENT_SIGNATURE", "")
        if argument_signature:
            datatypes = re.findall(
                r"(?:.+?)\s(?P<datatype>[a-zA-Z]+)(?:,|\))", argument_signature
            )
            argument_signature = f" ({','.join(datatypes)})"
        query = f"SELECT GET_DDL('{obj_map['type']}', '{setup.database}.{r['schema_name']}.{r['name']}{argument_signature}')"
        ddl = (snf_client.execute_query(query, use_dict_cursor=False))[0][0]
        ddl_with_schema = add_schema_to_ddl(
            ddl, r["schema_name"], obj_map["type"] != "TABLE"
        )
        object_folder = os.path.join(
            setup.output_folder, r["schema_name"], obj_map["foldername"]
        )
        save_file(object_folder, f"{r['schema_name']}.{r['name']}.sql", ddl_with_schema)
        progress_bar.next()
    progress_bar.finish()
