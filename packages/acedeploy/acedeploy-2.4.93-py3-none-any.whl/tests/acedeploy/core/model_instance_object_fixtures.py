import pytest


@pytest.fixture
def metadata_schema():
    return {
        "DATABASE_NAME": "my_db",
        "SCHEMA_NAME": "my_schema",
        # "IS_MANAGED_ACCESS": "NO",
        "IS_TRANSIENT": "NO",
        "RETENTION_TIME": 1,
        "DATABASE_RETENTION_TIME": 1,
        "COMMENT": None,
    }


@pytest.fixture
def metadata_stage():
    return {
        "database_name": "my_db",
        "schema_name": "my_schema",
        "name": "my_object",
        "has_credentials": "N",
        "has_encryption_key": "N",
        # "region": "eastasia",
        "type": "EXTERNAL",
        # "url": "azure://example.blob.core.windows.net/test",
        "comment": None,
        # "storage_integration": "MY_STORAGE_INTEGRATION",
        "cloud": "AZURE",
        "STAGE_FILE_FORMAT": {},  # might contain values
        "STAGE_COPY_OPTIONS": {},  # usually contains values
        "STAGE_LOCATION": {"URL": "azure://example.blob.core.windows.net/test"},
        "STAGE_INTEGRATION": {"STORAGE_INTEGRATION": "MY_STORAGE_INTEGRATION"},
        "DIRECTORY": {},  # usually contains values
    }


@pytest.fixture
def metadata_fileformat():
    return {
        "name": "MY_OBJECT",
        "database_name": "ACEDEPLOY_META_DB",
        "schema_name": "MY_SCHEMA",
        "type": "CSV",
        "owner": "R_ACEDEPLOY",
        "comment": "",
        "format_options": """{
            "TYPE": "csv",
            "RECORD_DELIMITER": "\\n",
            "FIELD_DELIMITER": "|",
            "FILE_EXTENSION": "NONE",
            "SKIP_HEADER": 1,
            "DATE_FORMAT": "AUTO",
            "TIME_FORMAT": "AUTO",
            "TIMESTAMP_FORMAT": "AUTO",
            "BINARY_FORMAT": "HEX",
            "ESCAPE": "NONE",
            "ESCAPE_UNENCLOSED_FIELD": "\\\\",
            "TRIM_SPACE": false,
            "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE",
            "NULL_IF": [
                "\\\\N"
            ],
            "COMPRESSION": "AUTO",
            "ERROR_ON_COLUMN_COUNT_MISMATCH": true,
            "VALIDATE_UTF8": true,
            "SKIP_BLANK_LINES": false,
            "REPLACE_INVALID_CHARACTERS": false,
            "EMPTY_FIELD_AS_NULL": true,
            "SKIP_BYTE_ORDER_MARK": true,
            "ENCODING": "UTF8"
        }""",
    }


@pytest.fixture
def metadata_stream():
    return {
        "name": "MYSTREAM",
        "database_name": "TWZ_META",
        "schema_name": "MISC",
        "comment": "",
        "table_name": "TWZ_META.DATA.TABLE1",
        "type": "DELTA",
        "stale": "false",
        "mode": "DEFAULT",
    }


@pytest.fixture
def metadata_task():
    return {
        "name": "MYTASK",
        "database_name": "TWZ_META",
        "schema_name": "MISC",
        "comment": "",
        "warehouse": "COMPUTE_WH",
        "schedule": "USING CRON * * * * * UTC",
        "predecessors": None,
        "state": "suspended",
        "definition": "INSERT INTO demo_db.public.t VALUES(1, 1, 1)",
        "condition": None,
        "allow_overlapping_execution": False,
    }


@pytest.fixture
def metadata_pipe():
    return {
        "DATABASE_NAME": "TWZ_META",
        "SCHEMA_NAME": "MISC",
        "OBJECT_NAME": "MYPIPE",
        "DEFINITION": "COPY INTO DATA.TABLE1 FROM @MISC.MY_EXTERNAL_STAGE",
        "IS_AUTOINGEST_ENABLED": "NO",
        "NOTIFICATION_CHANNEL_NAME": None,
        "COMMENT": None,
        "PATTERN": None,
        "integration": "MY_NOTIFICATION_INTEGRATION",
        "execution_state": "RUNNING",
    }


@pytest.fixture
def metadata_sequence():
    return {
        "DATABASE_NAME": "TWZ_META",
        "SCHEMA_NAME": "MISC",
        "OBJECT_NAME": "MYSEQUENCE",
        "DATA_TYPE": "NUMBER",
        "NUMERIC_PRECISION": 38,
        "NUMERIC_PRECISION_RADIX": 10,
        "NUMERIC_SCALE": 0,
        "START_VALUE": 1,
        "INCREMENT": 1,
        "COMMENT": None,
    }


@pytest.fixture
def metadata_function():
    return {
        "DATABASE_NAME": "my_db",
        "SCHEMA_NAME": "my_schema",
        "OBJECT_NAME": "my_object",
        "SIGNATURE": "(F FLOAT, I INT)",
        "DATA_TYPE": "FLOAT",
        "CHARACTER_MAXIMUM_LENGTH": None,
        "CHARACTER_OCTET_LENGTH": None,
        "NUMERIC_PRECISION": None,
        "NUMERIC_PRECISION_RADIX": None,
        "NUMERIC_SCALE": None,
        "LANGUAGE": "SQL",
        "DEFINITION": "\\n    pi() * radius * radius\\n  ",
        "IS_EXTERNAL": "NO",
        "IS_SECURE": "NO",
        "VOLATILITY": "VOLATILE",
        "IS_NULL_CALL": "YES",
        "COMMENT": None,
        "API_INTEGRATION": None,
        "CONTEXT_HEADERS": None,
        "MAX_BATCH_ROWS": None,
        "COMPRESSION": None,
    }


@pytest.fixture
def metadata_procedure():
    return {
        "DATABASE_NAME": "my_db",
        "SCHEMA_NAME": "my_schema",
        "OBJECT_NAME": "my_object",
        "SIGNATURE": "(F FLOAT, I INT)",
        "DATA_TYPE": "VARCHAR(16777216)",
        "CHARACTER_MAXIMUM_LENGTH": 16777216,
        "CHARACTER_OCTET_LENGTH": 16777216,
        "NUMERIC_PRECISION": None,
        "NUMERIC_PRECISION_RADIX": None,
        "NUMERIC_SCALE": None,
        "LANGUAGE": "JAVASCRIPT",
        "DEFINITION": "\n  var rs = snowflake.execute( { sqlText: \n      `INSERT INTO table1 (\"column 1\") \n           SELECT 'value 1' AS \"column 1\" ;`\n       } );\n  return 'Done.';\n  ",
        "COMMENT": None,
    }


@pytest.fixture
def metadata_maskingpolicy():
    return {
        "database_name": "TWZ_META",
        "schema_name": "POLICIES",
        "name": "MYMASKINGPOLICY",
        "kind": "MASKING_POLICY",
        "comment": "my comment",
        "signature": "(N NUMBER)",
        "return_type": "NUMBER(38,0)",
        "body": "1 --dummy policy body",
    }


@pytest.fixture
def metadata_rowaccesspolicy():
    return {
        "database_name": "TWZ_META",
        "schema_name": "POLICIES",
        "name": "MYROWACCESSPOLICY",
        "kind": "MASKING_POLICY",
        "comment": "my comment",
        "signature": "(N NUMBER)",
        "return_type": "BOOLEAN",
        "body": "TRUE --dummy policy body",
    }


@pytest.fixture
def metadata_view():
    return {
        "DATABASE_NAME": "TWZ_META",
        "SCHEMA_NAME": "VIEWS",
        "OBJECT_NAME": "VIEW1",
        "TABLE_TYPE": "VIEW",
        "CLUSTERING_KEY": None,
        "VIEW_DEFINITION": "CREATE VIEW VIEWS.VIEW1\nAS\n\n   SELECT DISTINCT\n   CASE WHEN ID IN (1001,1002) THEN ID\n   ELSE 1000 END AS ID\n   FROM DATA.TABLE1;",
        "IS_SECURE": "NO",
        "COMMENT": None,
        "COLUMN_DETAILS": [  {    "COLUMN_NAME": "ID",    "DATABASE_NAME": "TWZ_META",    "DATA_TYPE": "NUMBER",    "IS_IDENTITY": "NO",    "IS_NULLABLE": "YES",    "IS_SELF_REFERENCING": "NO",    "NUMERIC_PRECISION": 38,    "NUMERIC_PRECISION_RADIX": 10,    "NUMERIC_SCALE": 0,    "ORDINAL_POSITION": 1,    "TABLE_NAME": "VIEW1",    "TABLE_SCHEMA": "VIEWS"  }],
    }


@pytest.fixture
def metadata_externaltable():
    return {
        "DATABASE_NAME": "TWZ_META",
        "SCHEMA_NAME": "MISC",
        "OBJECT_NAME": "EXTTABLE1",
        "TABLE_TYPE": "EXTERNAL TABLE",
        "CLUSTERING_KEY": None,
        "COMMENT": None,
        "LOCATION": "@DB1.S1.STAGE1/",
        "FILE_FORMAT_NAME": None,
        "FILE_FORMAT_TYPE": "CSV",
        "COLUMN_DETAILS": [{"COLUMN_NAME":"ID","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"NO","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"TABLE1","TABLE_SCHEMA":"DATA"}],
    }

@pytest.fixture
def metadata_dynamictable():
    return {
        'DATABASE_NAME': 'TWZ_META',
        'SCHEMA_NAME': 'DATA',
        'OBJECT_NAME': 'DYNAMICTABLE1',
        'TABLE_TYPE': 'BASE TABLE', 
        'QUERY_TEXT': "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;", 
        'CLUSTERING_KEY': None, 
        'RETENTION_TIME': 0, 
        'SCHEMA_RETENTION_TIME': 1, 
        'COMMENT': 'MY COMMENT', 
        'COLUMN_DETAILS': [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }], 
        'TARGET_LAG': '2 hours', 
        'WAREHOUSE': 'COMPUTE_WH', 
        'REFRESH_MODE': 'INCREMENTAL'
    }

@pytest.fixture
def metadata_networkrule():
    return {
                "DATABASE_NAME": "TWZ_META",
                "SCHEMA_NAME": "MISC",
                "OBJECT_NAME": "MY_NETWORK_RULE1",
                "TYPE": "IPV4",
                "MODE": "INGRESS",
                "VALUE_LIST": "('0.0.0.0')",
                "COMMENT": "whitelist"
            }
