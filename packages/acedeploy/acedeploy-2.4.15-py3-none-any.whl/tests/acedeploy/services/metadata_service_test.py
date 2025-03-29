from unittest.mock import MagicMock

import acedeploy.core.model_instance_objects as mio
import acedeploy.services.metadata_service as mds
import pytest
from acedeploy.core.model_database_object import DbObjectType
from aceservices.snowflake_service import SnowClient


def compare(result_list, expected_dict_list):
    assert len(result_list) == len(expected_dict_list)
    for r, e in zip(result_list, expected_dict_list):
        for k, v in e.items():
            assert getattr(r, k) == v


class DummySnowClient(SnowClient):
    def __init__(self):
        self.user = "dummy"
        self.password = "dummy"
        self.account = "dummy"
        self.warehouse = "dummy"
        self.role = "dummy"
        self.database = "TWZ_META"

    def __del__(self):
        pass


def test_get_all_metadata():
    def mock_get_filtered_schema_name_list(schema_list):
        return ["DATA", "VIEWS", "DBP_MSI", "PROCFUNC", "MISC"]

    def mock_query_metadata(
        object_type_description,
        template_path,
        schemas_to_query,
        parallel_threads,
        database_name="",
    ):
        mapping = {
            DbObjectType.TABLE: [
                # {"DATABASE_NAME": "TWZ_META", "SCHEMA_NAME": "DATA", "OBJECT_NAME": "PRE_TEMP_TABLE", "TABLE_TYPE": "BASE TABLE", "CLUSTERING_KEY": None, "COLUMN_DETAILS": '[{"COLUMN_NAME":"ID","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"PRE_TEMP_TABLE","TABLE_SCHEMA":"DATA"}]'},
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "DATA",
                    "OBJECT_NAME": "TABLE1",
                    "TABLE_TYPE": "BASE TABLE",
                    "CLUSTERING_KEY": None,
                    "ROW_COUNT": 10,
                    "BYTES": 100,
                    "RETENTION_TIME": 1,
                    "SCHEMA_RETENTION_TIME": 1,
                    "COMMENT": "",
                    "COLUMN_DETAILS": '[{"COLUMN_NAME":"ID","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"NO","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"TABLE1","TABLE_SCHEMA":"DATA"}]',
                },
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "DATA",
                    "OBJECT_NAME": "TABLE2",
                    "TABLE_TYPE": "BASE TABLE",
                    "CLUSTERING_KEY": None,
                    "ROW_COUNT": 10,
                    "BYTES": 100,
                    "RETENTION_TIME": 1,
                    "SCHEMA_RETENTION_TIME": 1,
                    "COMMENT": "",
                    "COLUMN_DETAILS": '[{"CHARACTER_MAXIMUM_LENGTH":11,"CHARACTER_OCTET_LENGTH":44,"COLLATION_NAME":"en-ci","COLUMN_DEFAULT":"\'x\'","COLUMN_NAME":"T4","DATABASE_NAME":"TWZ_META","DATA_TYPE":"TEXT","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","ORDINAL_POSITION":4,"TABLE_NAME":"TABLE2","TABLE_SCHEMA":"DATA"},{"CHARACTER_MAXIMUM_LENGTH":12,"CHARACTER_OCTET_LENGTH":48,"COLLATION_NAME":"en-ci","COLUMN_NAME":"T2","DATABASE_NAME":"TWZ_META","DATA_TYPE":"TEXT","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","ORDINAL_POSITION":2,"TABLE_NAME":"TABLE2","TABLE_SCHEMA":"DATA"},{"CHARACTER_MAXIMUM_LENGTH":11,"CHARACTER_OCTET_LENGTH":44,"COLUMN_NAME":"T1","DATABASE_NAME":"TWZ_META","DATA_TYPE":"TEXT","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","ORDINAL_POSITION":1,"TABLE_NAME":"TABLE2","TABLE_SCHEMA":"DATA"},{"CHARACTER_MAXIMUM_LENGTH":12,"CHARACTER_OCTET_LENGTH":48,"COLLATION_NAME":"en-ci","COLUMN_NAME":"T3","DATABASE_NAME":"TWZ_META","DATA_TYPE":"TEXT","IS_IDENTITY":"NO","IS_NULLABLE":"NO","IS_SELF_REFERENCING":"NO","ORDINAL_POSITION":3,"TABLE_NAME":"TABLE2","TABLE_SCHEMA":"DATA"}]',
                },
            ],
            "constraint_foreign_keys": [],
            "constraint_primary_keys": [],
            "constraint_unique_keys": [],
            DbObjectType.EXTERNALTABLE: [
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "DATA",
                    "OBJECT_NAME": "EXTTABLE1",
                    "TABLE_TYPE": "EXTERNAL TABLE",
                    "CLUSTERING_KEY": None,
                    "COMMENT": "",
                    "LOCATION": "@DB1.S1.STAGE1/",
                    "FILE_FORMAT_NAME": None,
                    "FILE_FORMAT_TYPE": "CSV",
                    "COLUMN_DETAILS": '[{"COLUMN_NAME":"ID","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"NO","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"TABLE1","TABLE_SCHEMA":"DATA"}]',
                },
            ],
            DbObjectType.VIEW: [
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "RECURSIVE_VIEW",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "VIEW_DEFINITION": "DUMMY DEFINITION",
                    "IS_SECURE": "NO",
                    "COMMENT": "DUMMY COMMENT",
                    "COLUMN_DETAILS": '[{"CHARACTER_MAXIMUM_LENGTH":11,"CHARACTER_OCTET_LENGTH":44,"COLUMN_NAME":"T1","DATABASE_NAME":"TWZ_META","DATA_TYPE":"TEXT","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","ORDINAL_POSITION":1,"TABLE_NAME":"RECURSIVE_VIEW","TABLE_SCHEMA":"VIEWS"}]',
                },
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "VIEW1",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "VIEW_DEFINITION": "DUMMY DEFINITION",
                    "IS_SECURE": "YES",
                    "COMMENT": None,
                    "COLUMN_DETAILS": '[{"COLUMN_NAME":"ID","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}]',
                },
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "VIEW2",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "VIEW_DEFINITION": "DUMMY DEFINITION",
                    "IS_SECURE": "NO",
                    "COMMENT": None,
                    "COLUMN_DETAILS": '[{"COLUMN_NAME":"INT","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":1,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW2","TABLE_SCHEMA":"VIEWS"}]',
                },
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "VIEW3",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "VIEW_DEFINITION": "DUMMY DEFINITION",
                    "IS_SECURE": "NO",
                    "COMMENT": None,
                    "COLUMN_DETAILS": '[{"COLUMN_NAME":"ID","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW3","TABLE_SCHEMA":"VIEWS"}]',
                },
            ],
            DbObjectType.MATERIALIZEDVIEW: [
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "MAT_VIEW1",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "COMMENT": None,
                    "COLUMN_DETAILS": '[{"COLUMN_NAME":"ID","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"MAT_VIEW1","TABLE_SCHEMA":"VIEWS"}]',
                }
            ],
            DbObjectType.SCHEMA: [
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "DATA",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 1,
                    "DATABASE_RETENTION_TIME": 1,
                    "COMMENT": None,
                },
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "DBP_MSI",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 1,
                    "DATABASE_RETENTION_TIME": 1,
                    "COMMENT": None,
                },
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "PROCFUNC",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 1,
                    "DATABASE_RETENTION_TIME": 1,
                    "COMMENT": None,
                },
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "VIEWS",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 1,
                    "DATABASE_RETENTION_TIME": 1,
                    "COMMENT": None,
                },
            ],
            DbObjectType.FUNCTION: [
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "PROCFUNC",
                    "OBJECT_NAME": "AREA",
                    "SIGNATURE": "(RADIUS FLOAT)",
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
            ],
            DbObjectType.PROCEDURE: [
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "PROCFUNC",
                    "OBJECT_NAME": "MYPROC",
                    "SIGNATURE": "()",
                    "DATA_TYPE": "VARCHAR(16777216)",
                    "CHARACTER_MAXIMUM_LENGTH": None,
                    "CHARACTER_OCTET_LENGTH": None,
                    "NUMERIC_PRECISION": None,
                    "NUMERIC_PRECISION_RADIX": None,
                    "NUMERIC_SCALE": None,
                    "DEFINITION": "\n  var rs = snowflake.execute( { sqlText: \n      `INSERT INTO table1 (\"column 1\") \n           SELECT 'value 1' AS \"column 1\" ;`\n       } );\n  return 'Done.';\n  ",
                    "LANGUAGE": "JAVASCRIPT",
                    "COMMENT": None,
                }
            ],
            DbObjectType.STAGE: [
                # see also additional mock below
                {
                    "database_name": "TWZ_META",
                    "schema_name": "MISC",
                    "name": "MY_EXTERNAL_STAGE",
                    "has_credentials": "N",
                    "has_encryption_key": "N",
                    "region": "eastasia",
                    "type": "EXTERNAL",
                    "comment": None,
                    "notification_channel": None,
                    "cloud": "AZURE",
                }
            ],
            DbObjectType.FILEFORMAT: [
                {
                    "name": "MY_CSV_FORMAT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "TWZ_META",
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
            ],
            DbObjectType.STREAM: [
                {
                    "name": "MYSTREAM",
                    "database_name": "TWZ_META",
                    "schema_name": "MISC",
                    "comment": "",
                    "table_name": "TWZ_META.DATA.TABLE1",
                    "type": "DELTA",
                    "stale": "false",
                    "mode": "DEFAULT",
                }
            ],
            DbObjectType.TASK: [
                {
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
            ],
            DbObjectType.PIPE: [
                # see also additional mock below
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "MISC",
                    "OBJECT_NAME": "MYPIPE",
                    "DEFINITION": "COPY INTO DATA.TABLE1 FROM @MISC.MY_EXTERNAL_STAGE",
                    "IS_AUTOINGEST_ENABLED": "NO",
                    "NOTIFICATION_CHANNEL_NAME": None,
                    "COMMENT": None,
                    "PATTERN": None,
                    "integration": "MY_INTEGRATION",
                    "execution_state": "RUNNING",
                }
            ],
            DbObjectType.SEQUENCE: [
                {
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
            ],
            DbObjectType.MASKINGPOLICY: [
                # see also additional mock below
                {
                    "database_name": "TWZ_META",
                    "schema_name": "POLICIES",
                    "name": "MYMASKINGPOLICY",
                    "kind": "MASKING_POLICY",
                    "comment": "my comment",
                }
            ],
            DbObjectType.ROWACCESSPOLICY: [
                # see also additional mock below
                {
                    "database_name": "TWZ_META",
                    "schema_name": "POLICIES",
                    "name": "MYROWACCESSPOLICY",
                    "kind": "MASKING_POLICY",
                    "comment": "my comment",
                }
            ],
            DbObjectType.DYNAMICTABLE: [
                {
                'DATABASE_NAME': 'TWZ_META',
                'SCHEMA_NAME': 'DATA',
                'OBJECT_NAME': 'DYNAMICTABLE1',
                'TABLE_TYPE': 'BASE TABLE', 
                'QUERY_TEXT': "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;", 
                'CLUSTERING_KEY': None, 
                'RETENTION_TIME': 0, 
                'SCHEMA_RETENTION_TIME': 1, 
                'COMMENT': 'TEST COMMENT', 
                'COLUMN_DETAILS': '[{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }]', 
                'target_lag': '2 hours', 
                'warehouse': 'COMPUTE_WH', 
                'refresh_mode': 'INCREMENTAL'}
            ],
            DbObjectType.NETWORKRULE: [
                {
                "DATABASE_NAME": "TWZ_META",
                "SCHEMA_NAME": "MISC",
                "OBJECT_NAME": "MY_NETWORK_RULE1",
                "TYPE": "IPV4",
                "MODE": "INGRESS",
                "VALUE_LIST": "('0.0.0.0')",
                "COMMENT": "whitelist"
            }
            ]
        }
        return mapping[object_type_description]

    def mock_extend_metadata_dynamictables(metadata_list, object_type, schemas_to_query, parallel_threads):
        return (
            [{
                'DATABASE_NAME': 'TWZ_META',
                'SCHEMA_NAME': 'DATA',
                'OBJECT_NAME': 'DYNAMICTABLE1',
                'TABLE_TYPE': 'BASE TABLE', 
                'QUERY_TEXT': "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;", 
                'CLUSTERING_KEY': None, 
                'RETENTION_TIME': 0, 
                'SCHEMA_RETENTION_TIME': 1, 
                'COMMENT': 'TEST COMMENT', 
                'COLUMN_DETAILS': [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }], 
                'TARGET_LAG': '2 hours', 
                'WAREHOUSE': 'COMPUTE_WH', 
                'REFRESH_MODE': 'INCREMENTAL'}]
        )

    def mock_extend_metadata_networkrules(metadata_list, object_type, schemas_to_query, parallel_threads):
        return (
            [{
                "DATABASE_NAME": "TWZ_META",
                "SCHEMA_NAME": "MISC",
                "OBJECT_NAME": "MY_NETWORK_RULE1",
                "TYPE": "IPV4",
                "MODE": "INGRESS",
                "VALUE_LIST": "('0.0.0.0')",
                "COMMENT": "whitelist"
            }]
        )

    def mock_extend_metadata_maskingpolicies(metadata_list):
        return (
            {
                "database_name": "TWZ_META",
                "schema_name": "POLICIES",
                "name": "MYMASKINGPOLICY",
                "kind": "MASKING_POLICY",
                "comment": "my comment",
                "signature": "(N NUMBER)",
                "return_type": "NUMBER(38,0)",
                "body": "1 --dummy policy body",
            },
        )

    def mock_get_rowaccespolicy_metadata(metadata_list):
        return (
            {
                "database_name": "TWZ_META",
                "schema_name": "POLICIES",
                "name": "MYMASKINGPOLICY",
                "kind": "MASKING_POLICY",
                "comment": "my comment",
                "signature": "(N NUMBER)",
                "return_type": "BOOLEAN",
                "body": "TRUE --dummy policy body",
            },
        )

    def mock_extend_metadata_pipes(metadata_list):
        return (
            {
                "DATABASE_NAME": "TWZ_META",
                "SCHEMA_NAME": "MISC",
                "OBJECT_NAME": "MYPIPE",
                "DEFINITION": "COPY INTO DATA.TABLE1 FROM @MISC.MY_EXTERNAL_STAGE",
                "IS_AUTOINGEST_ENABLED": "NO",
                "NOTIFICATION_CHANNEL_NAME": None,
                "COMMENT": None,
                "PATTERN": None,
                "database_name": "TWZ_META",
                "schema_name": "MISC",
                "name": "MYPIPE",
                "definition": "COPY INTO DATA.TABLE1 FROM @MISC.MY_EXTERNAL_STAGE",
                "comment": None,
                "signature": "(N NUMBER)",
                "notification_channel": None,
                "integration": "MY_NOTIFICATION_INTEGRATION",
                "execution_state": "RUNNING",
            },
        )

    def mock_extend_metadata_stages(metadata_list):
        return [
            {
                "database_name": "TWZ_META",
                "schema_name": "MISC",
                "name": "MY_EXTERNAL_STAGE",
                "has_credentials": "N",
                "has_encryption_key": "N",
                "region": "eastasia",
                "type": "EXTERNAL",
                "comment": None,
                "notification_channel": None,
                "cloud": "AZURE",
                "STAGE_FILE_FORMAT": {},
                "STAGE_COPY_OPTIONS": {},
                "STAGE_LOCATION": {"URL": "azure://example.blob.core.windows.net/test"},
                "STAGE_INTEGRATION": {"STORAGE_INTEGRATION": "MY_STORAGE_INTEGRATION"},
                "DIRECTORY": {},
            }
        ]

    metadata_service = mds.MetadataService(DummySnowClient())
    metadata_service._get_filtered_schema_name_list = MagicMock(
        side_effect=mock_get_filtered_schema_name_list
    )
    metadata_service._query_metadata = MagicMock(side_effect=mock_query_metadata)
    metadata_service._extend_metadata_dynamictables = MagicMock(
        side_effect=mock_extend_metadata_dynamictables
    )
    metadata_service._extend_metadata_networkrules = MagicMock(
        side_effect=mock_extend_metadata_networkrules
    )
    metadata_service._extend_metadata_maskingpolicies = MagicMock(
        side_effect=mock_extend_metadata_maskingpolicies
    )
    metadata_service._extend_metadata_rowaccesspolicies = MagicMock(
        side_effect=mock_get_rowaccespolicy_metadata
    )
    metadata_service._extend_metadata_pipes = MagicMock(
        side_effect=mock_extend_metadata_pipes
    )
    metadata_service._extend_metadata_stages = MagicMock(
        side_effect=mock_extend_metadata_stages
    )


    def mock_get_metadata_tags(schemas_to_query, parallel_threads):
        return []
    metadata_service._get_metadata_tags = MagicMock(
    side_effect=mock_get_metadata_tags
    )

    def mock_extend_metadata_with_tags(metadata_list, parallel_threads, object_type):
        return metadata_list
    metadata_service._extend_metadata_with_tags = MagicMock(
    side_effect=mock_extend_metadata_with_tags
    )


    schema_list = {"blacklist": []}
    metadata_service.get_all_metadata(schema_list)

    assert metadata_service.database_name == "TWZ_META"

    expected_schemas = [
        {
            "schema": "DATA",
            "name": "DATA",
            "database_name": "TWZ_META",
            "retention_time": 1,
            "database_retention_time": 1,
            "object_type": DbObjectType.SCHEMA,
        },
        {
            "schema": "DBP_MSI",
            "name": "DBP_MSI",
            "database_name": "TWZ_META",
            "retention_time": 1,
            "database_retention_time": 1,
            "object_type": DbObjectType.SCHEMA,
        },
        {
            "schema": "PROCFUNC",
            "name": "PROCFUNC",
            "database_name": "TWZ_META",
            "retention_time": 1,
            "database_retention_time": 1,
            "object_type": DbObjectType.SCHEMA,
        },
        {
            "schema": "VIEWS",
            "name": "VIEWS",
            "database_name": "TWZ_META",
            "retention_time": 1,
            "database_retention_time": 1,
            "object_type": DbObjectType.SCHEMA,
        },
    ]
    compare(metadata_service.schemas, expected_schemas)
    for schema in metadata_service.schemas:
        assert isinstance(schema, mio.InstanceSchema)

    expected_functions = [
        {
            "schema": "PROCFUNC",
            "name": "AREA",
            "database_name": "TWZ_META",
            "object_type": DbObjectType.FUNCTION,
            "parameters": ["FLOAT"],
        }
    ]
    compare(metadata_service.functions, expected_functions)
    for function in metadata_service.functions:
        assert isinstance(function, mio.InstanceFunction)

    expected_procedures = [
        {
            "schema": "PROCFUNC",
            "name": "MYPROC",
            "database_name": "TWZ_META",
            "object_type": DbObjectType.PROCEDURE,
            "parameters": [],
        }
    ]
    compare(metadata_service.procedures, expected_procedures)
    for procedure in metadata_service.procedures:
        assert isinstance(procedure, mio.InstanceProcedure)

    expected_fileformats = [
        {
            "object_type": DbObjectType.FILEFORMAT,
            "name": "MY_CSV_FORMAT",
            "database_name": "ACEDEPLOY_META_DB",
            "schema": "TWZ_META",
            "file_format_type": "CSV",
            "comment": "",
            "format_options": {
                "RECORD_DELIMITER": "\n",
                "FIELD_DELIMITER": "|",
                "FILE_EXTENSION": "NONE",
                "SKIP_HEADER": 1,
                "DATE_FORMAT": "AUTO",
                "TIME_FORMAT": "AUTO",
                "TIMESTAMP_FORMAT": "AUTO",
                "BINARY_FORMAT": "HEX",
                "ESCAPE": "NONE",
                "ESCAPE_UNENCLOSED_FIELD": "\\",
                "TRIM_SPACE": False,
                "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE",
                "NULL_IF": ["\\N"],
                "COMPRESSION": "AUTO",
                "ERROR_ON_COLUMN_COUNT_MISMATCH": True,
                "VALIDATE_UTF8": True,
                "SKIP_BLANK_LINES": False,
                "REPLACE_INVALID_CHARACTERS": False,
                "EMPTY_FIELD_AS_NULL": True,
                "SKIP_BYTE_ORDER_MARK": True,
                "ENCODING": "UTF8",
            },
        }
    ]
    compare(metadata_service.fileformats, expected_fileformats)
    for fileformat in metadata_service.fileformats:
        assert isinstance(fileformat, mio.InstanceFileformat)

    expected_stages = [
        {
            "database_name": "TWZ_META",
            "schema": "MISC",
            "name": "MY_EXTERNAL_STAGE",
            "object_type": DbObjectType.STAGE,
            "has_credentials": "N",
            "has_encryption_key": "N",
            "type": "EXTERNAL",
            "comment": None,
            "cloud": "AZURE",
            "stage_file_format": {},
            "stage_copy_options": {},
            "stage_location": {"URL": "azure://example.blob.core.windows.net/test"},
            "stage_integration": {"STORAGE_INTEGRATION": "MY_STORAGE_INTEGRATION"},
            "directory": {},
        }
    ]
    compare(metadata_service.stages, expected_stages)
    for stage in metadata_service.stages:
        assert isinstance(stage, mio.InstanceStage)

    expected_streams = [
        {
            "schema": "MISC",
            "name": "MYSTREAM",
            "database_name": "TWZ_META",
            "object_type": DbObjectType.STREAM,
            "comment": "",
            "table_name": "DATA.TABLE1",
            "type": "DELTA",
            "stale": "false",
            "mode": "DEFAULT",
        }
    ]
    compare(metadata_service.streams, expected_streams)
    for stream in metadata_service.streams:
        assert isinstance(stream, mio.InstanceStream)

    expected_tasks = [
        {
            "schema": "MISC",
            "name": "MYTASK",
            "database_name": "TWZ_META",
            "object_type": DbObjectType.TASK,
            "comment": "",
            "warehouse": "COMPUTE_WH",
            "schedule": "USING CRON * * * * * UTC",
            "predecessors": [],
            "state": "suspended",
            "definition": "INSERT INTO demo_db.public.t VALUES(1, 1, 1)",
            "condition": None,
            "allow_overlapping_execution": False,
        }
    ]
    compare(metadata_service.tasks, expected_tasks)
    for task in metadata_service.tasks:
        assert isinstance(task, mio.InstanceTask)

    expected_pipes = [
        {
            "schema": "MISC",
            "name": "MYPIPE",
            "database_name": "TWZ_META",
            "object_type": DbObjectType.PIPE,
            "comment": None,
            "definition": "COPY INTO DATA.TABLE1 FROM @MISC.MY_EXTERNAL_STAGE",
            "is_autoingest_enabled": "NO",
            "notification_channel_name": None,
            "pattern": None,
            "integration": "MY_NOTIFICATION_INTEGRATION",
            "execution_state": "RUNNING",
        }
    ]
    compare(metadata_service.pipes, expected_pipes)
    for pipe in metadata_service.pipes:
        assert isinstance(pipe, mio.InstancePipe)

    expected_sequences = [
        {
            "schema": "MISC",
            "name": "MYSEQUENCE",
            "database_name": "TWZ_META",
            "object_type": DbObjectType.SEQUENCE,
            "data_type": "NUMBER",
            "numeric_precision": 38,
            "numeric_precision_radix": 10,
            "numeric_scale": 0,
            "start_value": 1,
            "increment": 1,
            "comment": None,
        }
    ]
    compare(metadata_service.sequences, expected_sequences)
    for sequence in metadata_service.sequences:
        assert isinstance(sequence, mio.InstanceSequence)

    expected_tables = [
        {
            "schema": "DATA",
            "name": "TABLE1",
            "database_name": "TWZ_META",
            "object_type": DbObjectType.TABLE,
            "retention_time": 1,
            "schema_retention_time": 1,
            "comment": "",
        },
        {
            "schema": "DATA",
            "name": "TABLE2",
            "database_name": "TWZ_META",
            "object_type": DbObjectType.TABLE,
            "retention_time": 1,
            "schema_retention_time": 1,
            "comment": "",
        },
    ]
    compare(metadata_service.tables, expected_tables)
    for table in metadata_service.tables:
        assert isinstance(table, mio.InstanceTable)
        for column in table.table_columns:
            assert isinstance(column, mio.ColumnInstance)

    expected_table_columns = [
        {
            "table_id": 0,
            "columns": [
                {
                    "database_name": "TWZ_META",
                    "object_schema": "DATA",
                    "object_name": "TABLE1",
                    "column_name": "ID",
                    "ordinal_position": 1,
                    "column_default": None,
                    "is_nullable": "NO",
                    "data_type": "NUMBER",
                    "character_maximum_length": None,
                    "character_octet_length": None,
                    "numeric_precision": 38,
                    "numeric_precision_radix": 10,
                    "numeric_scale": 0,
                    "datetime_precision": None,
                    "interval_type": None,
                    "interval_precision": None,
                    "character_set_catalog": None,
                    "character_set_schema": None,
                    "character_set_name": None,
                    "collation_catalog": None,
                    "collation_schema": None,
                    "collation_name": None,
                    "domain_catalog": None,
                    "domain_schema": None,
                    "domain_name": None,
                    "udt_catalog": None,
                    "udt_schema": None,
                    "udt_name": None,
                    "scope_catalog": None,
                    "scope_schema": None,
                    "scope_name": None,
                    "maximum_cardinality": None,
                    "dtd_identifier": None,
                    "is_self_referencing": "NO",
                    "is_identity": "NO",
                    "identity_generation": None,
                    "identity_start": None,
                    "identity_increment": None,
                    "identity_maximum": None,
                    "identity_minimum": None,
                    "identity_cycle": None,
                    "comment": None,
                }
            ],
        },
        {
            "table_id": 1,
            "columns": [
                {
                    "database_name": "TWZ_META",
                    "object_schema": "DATA",
                    "object_name": "TABLE2",
                    "column_name": "T1",
                    "ordinal_position": 1,
                    "column_default": None,
                    "is_nullable": "YES",
                    "data_type": "TEXT",
                    "character_maximum_length": 11,
                    "character_octet_length": 44,
                    "numeric_precision": None,
                    "numeric_precision_radix": None,
                    "numeric_scale": None,
                    "datetime_precision": None,
                    "interval_type": None,
                    "interval_precision": None,
                    "character_set_catalog": None,
                    "character_set_schema": None,
                    "character_set_name": None,
                    "collation_catalog": None,
                    "collation_schema": None,
                    "collation_name": None,
                    "domain_catalog": None,
                    "domain_schema": None,
                    "domain_name": None,
                    "udt_catalog": None,
                    "udt_schema": None,
                    "udt_name": None,
                    "scope_catalog": None,
                    "scope_schema": None,
                    "scope_name": None,
                    "maximum_cardinality": None,
                    "dtd_identifier": None,
                    "is_self_referencing": "NO",
                    "is_identity": "NO",
                    "identity_generation": None,
                    "identity_start": None,
                    "identity_increment": None,
                    "identity_maximum": None,
                    "identity_minimum": None,
                    "identity_cycle": None,
                    "comment": None,
                },
                {
                    "database_name": "TWZ_META",
                    "object_schema": "DATA",
                    "object_name": "TABLE2",
                    "column_name": "T2",
                    "ordinal_position": 2,
                    "column_default": None,
                    "is_nullable": "YES",
                    "data_type": "TEXT",
                    "character_maximum_length": 12,
                    "character_octet_length": 48,
                    "numeric_precision": None,
                    "numeric_precision_radix": None,
                    "numeric_scale": None,
                    "datetime_precision": None,
                    "interval_type": None,
                    "interval_precision": None,
                    "character_set_catalog": None,
                    "character_set_schema": None,
                    "character_set_name": None,
                    "collation_catalog": None,
                    "collation_schema": None,
                    "collation_name": "en-ci",
                    "domain_catalog": None,
                    "domain_schema": None,
                    "domain_name": None,
                    "udt_catalog": None,
                    "udt_schema": None,
                    "udt_name": None,
                    "scope_catalog": None,
                    "scope_schema": None,
                    "scope_name": None,
                    "maximum_cardinality": None,
                    "dtd_identifier": None,
                    "is_self_referencing": "NO",
                    "is_identity": "NO",
                    "identity_generation": None,
                    "identity_start": None,
                    "identity_increment": None,
                    "identity_maximum": None,
                    "identity_minimum": None,
                    "identity_cycle": None,
                    "comment": None,
                },
                {
                    "database_name": "TWZ_META",
                    "object_schema": "DATA",
                    "object_name": "TABLE2",
                    "column_name": "T3",
                    "ordinal_position": 3,
                    "column_default": None,
                    "is_nullable": "NO",
                    "data_type": "TEXT",
                    "character_maximum_length": 12,
                    "character_octet_length": 48,
                    "numeric_precision": None,
                    "numeric_precision_radix": None,
                    "numeric_scale": None,
                    "datetime_precision": None,
                    "interval_type": None,
                    "interval_precision": None,
                    "character_set_catalog": None,
                    "character_set_schema": None,
                    "character_set_name": None,
                    "collation_catalog": None,
                    "collation_schema": None,
                    "collation_name": "en-ci",
                    "domain_catalog": None,
                    "domain_schema": None,
                    "domain_name": None,
                    "udt_catalog": None,
                    "udt_schema": None,
                    "udt_name": None,
                    "scope_catalog": None,
                    "scope_schema": None,
                    "scope_name": None,
                    "maximum_cardinality": None,
                    "dtd_identifier": None,
                    "is_self_referencing": "NO",
                    "is_identity": "NO",
                    "identity_generation": None,
                    "identity_start": None,
                    "identity_increment": None,
                    "identity_maximum": None,
                    "identity_minimum": None,
                    "identity_cycle": None,
                    "comment": None,
                },
                {
                    "database_name": "TWZ_META",
                    "object_schema": "DATA",
                    "object_name": "TABLE2",
                    "column_name": "T4",
                    "ordinal_position": 4,
                    "column_default": "'x'",
                    "is_nullable": "YES",
                    "data_type": "TEXT",
                    "character_maximum_length": 11,
                    "character_octet_length": 44,
                    "numeric_precision": None,
                    "numeric_precision_radix": None,
                    "numeric_scale": None,
                    "datetime_precision": None,
                    "interval_type": None,
                    "interval_precision": None,
                    "character_set_catalog": None,
                    "character_set_schema": None,
                    "character_set_name": None,
                    "collation_catalog": None,
                    "collation_schema": None,
                    "collation_name": "en-ci",
                    "domain_catalog": None,
                    "domain_schema": None,
                    "domain_name": None,
                    "udt_catalog": None,
                    "udt_schema": None,
                    "udt_name": None,
                    "scope_catalog": None,
                    "scope_schema": None,
                    "scope_name": None,
                    "maximum_cardinality": None,
                    "dtd_identifier": None,
                    "is_self_referencing": "NO",
                    "is_identity": "NO",
                    "identity_generation": None,
                    "identity_start": None,
                    "identity_increment": None,
                    "identity_maximum": None,
                    "identity_minimum": None,
                    "identity_cycle": None,
                    "comment": None,
                },
            ],
        },
    ]
    for column_dict in expected_table_columns:
        compare(
            metadata_service.tables[column_dict["table_id"]].table_columns,
            column_dict["columns"],
        )

    expected_externaltables = [
        {
            "schema": "DATA",
            "name": "EXTTABLE1",
            "database_name": "TWZ_META",
            "object_type": DbObjectType.EXTERNALTABLE,
            "comment": "",
            "location": "@DB1.S1.STAGE1/",
            "file_format_name": None,
            "file_format_type": "CSV",
        },
    ]
    compare(metadata_service.externaltables, expected_externaltables)
    for exttable in metadata_service.externaltables:
        assert isinstance(exttable, mio.InstanceExternalTable)
        for column in exttable.table_columns:
            assert isinstance(column, mio.ColumnInstance)

    expected_externaltable_columns = [
        {
            "table_id": 0,
            "columns": [
                {
                    "database_name": "TWZ_META",
                    "object_schema": "DATA",
                    "object_name": "TABLE1",
                    "column_name": "ID",
                    "ordinal_position": 1,
                    "column_default": None,
                    "is_nullable": "NO",
                    "data_type": "NUMBER",
                    "character_maximum_length": None,
                    "character_octet_length": None,
                    "numeric_precision": 38,
                    "numeric_precision_radix": 10,
                    "numeric_scale": 0,
                    "datetime_precision": None,
                    "interval_type": None,
                    "interval_precision": None,
                    "character_set_catalog": None,
                    "character_set_schema": None,
                    "character_set_name": None,
                    "collation_catalog": None,
                    "collation_schema": None,
                    "collation_name": None,
                    "domain_catalog": None,
                    "domain_schema": None,
                    "domain_name": None,
                    "udt_catalog": None,
                    "udt_schema": None,
                    "udt_name": None,
                    "scope_catalog": None,
                    "scope_schema": None,
                    "scope_name": None,
                    "maximum_cardinality": None,
                    "dtd_identifier": None,
                    "is_self_referencing": "NO",
                    "is_identity": "NO",
                    "identity_generation": None,
                    "identity_start": None,
                    "identity_increment": None,
                    "identity_maximum": None,
                    "identity_minimum": None,
                    "identity_cycle": None,
                    "comment": None,
                }
            ],
        },
    ]
    for column_dict in expected_externaltable_columns:
        compare(
            metadata_service.externaltables[column_dict["table_id"]].table_columns,
            column_dict["columns"],
        )

    expected_views = [
        {
            "schema": "VIEWS",
            "name": "RECURSIVE_VIEW",
            "database_name": "TWZ_META",
            "object_type": DbObjectType.VIEW,
            "view_definition": "DUMMY DEFINITION",
            "is_secure": "NO",
            "comment": "DUMMY COMMENT",
        },
        {
            "schema": "VIEWS",
            "name": "VIEW1",
            "database_name": "TWZ_META",
            "object_type": DbObjectType.VIEW,
            "view_definition": "DUMMY DEFINITION",
            "is_secure": "YES",
            "comment": None,
        },
        {
            "schema": "VIEWS",
            "name": "VIEW2",
            "database_name": "TWZ_META",
            "object_type": DbObjectType.VIEW,
            "view_definition": "DUMMY DEFINITION",
            "is_secure": "NO",
            "comment": None,
        },
        {
            "schema": "VIEWS",
            "name": "VIEW3",
            "database_name": "TWZ_META",
            "object_type": DbObjectType.VIEW,
            "view_definition": "DUMMY DEFINITION",
            "is_secure": "NO",
            "comment": None,
        },
    ]
    compare(metadata_service.views, expected_views)
    for view in metadata_service.views:
        assert isinstance(view, mio.InstanceView)
        for column in view.table_columns:
            assert isinstance(column, mio.ColumnInstance)

    expected_view_columns = [
        {
            "table_id": 0,
            "columns": [
                {
                    "database_name": "TWZ_META",
                    "object_schema": "VIEWS",
                    "object_name": "RECURSIVE_VIEW",
                    "column_name": "T1",
                    "ordinal_position": 1,
                    "column_default": None,
                    "is_nullable": "YES",
                    "data_type": "TEXT",
                    "character_maximum_length": 11,
                    "character_octet_length": 44,
                    "numeric_precision": None,
                    "numeric_precision_radix": None,
                    "numeric_scale": None,
                    "datetime_precision": None,
                    "interval_type": None,
                    "interval_precision": None,
                    "character_set_catalog": None,
                    "character_set_schema": None,
                    "character_set_name": None,
                    "collation_catalog": None,
                    "collation_schema": None,
                    "collation_name": None,
                    "domain_catalog": None,
                    "domain_schema": None,
                    "domain_name": None,
                    "udt_catalog": None,
                    "udt_schema": None,
                    "udt_name": None,
                    "scope_catalog": None,
                    "scope_schema": None,
                    "scope_name": None,
                    "maximum_cardinality": None,
                    "dtd_identifier": None,
                    "is_self_referencing": "NO",
                    "is_identity": "NO",
                    "identity_generation": None,
                    "identity_start": None,
                    "identity_increment": None,
                    "identity_maximum": None,
                    "identity_minimum": None,
                    "identity_cycle": None,
                    "comment": None,
                }
            ],
        },
        {
            "table_id": 1,
            "columns": [
                {
                    "database_name": "TWZ_META",
                    "object_schema": "VIEWS",
                    "object_name": "VIEW1",
                    "column_name": "ID",
                    "ordinal_position": 1,
                    "column_default": None,
                    "is_nullable": "YES",
                    "data_type": "NUMBER",
                    "character_maximum_length": None,
                    "character_octet_length": None,
                    "numeric_precision": 38,
                    "numeric_precision_radix": 10,
                    "numeric_scale": 0,
                    "datetime_precision": None,
                    "interval_type": None,
                    "interval_precision": None,
                    "character_set_catalog": None,
                    "character_set_schema": None,
                    "character_set_name": None,
                    "collation_catalog": None,
                    "collation_schema": None,
                    "collation_name": None,
                    "domain_catalog": None,
                    "domain_schema": None,
                    "domain_name": None,
                    "udt_catalog": None,
                    "udt_schema": None,
                    "udt_name": None,
                    "scope_catalog": None,
                    "scope_schema": None,
                    "scope_name": None,
                    "maximum_cardinality": None,
                    "dtd_identifier": None,
                    "is_self_referencing": "NO",
                    "is_identity": "NO",
                    "identity_generation": None,
                    "identity_start": None,
                    "identity_increment": None,
                    "identity_maximum": None,
                    "identity_minimum": None,
                    "identity_cycle": None,
                    "comment": None,
                }
            ],
        },
        {
            "table_id": 2,
            "columns": [
                {
                    "database_name": "TWZ_META",
                    "object_schema": "VIEWS",
                    "object_name": "VIEW2",
                    "column_name": "INT",
                    "ordinal_position": 1,
                    "column_default": None,
                    "is_nullable": "YES",
                    "data_type": "NUMBER",
                    "character_maximum_length": None,
                    "character_octet_length": None,
                    "numeric_precision": 1,
                    "numeric_precision_radix": 10,
                    "numeric_scale": 0,
                    "datetime_precision": None,
                    "interval_type": None,
                    "interval_precision": None,
                    "character_set_catalog": None,
                    "character_set_schema": None,
                    "character_set_name": None,
                    "collation_catalog": None,
                    "collation_schema": None,
                    "collation_name": None,
                    "domain_catalog": None,
                    "domain_schema": None,
                    "domain_name": None,
                    "udt_catalog": None,
                    "udt_schema": None,
                    "udt_name": None,
                    "scope_catalog": None,
                    "scope_schema": None,
                    "scope_name": None,
                    "maximum_cardinality": None,
                    "dtd_identifier": None,
                    "is_self_referencing": "NO",
                    "is_identity": "NO",
                    "identity_generation": None,
                    "identity_start": None,
                    "identity_increment": None,
                    "identity_maximum": None,
                    "identity_minimum": None,
                    "identity_cycle": None,
                    "comment": None,
                }
            ],
        },
        {
            "table_id": 3,
            "columns": [
                {
                    "database_name": "TWZ_META",
                    "object_schema": "VIEWS",
                    "object_name": "VIEW3",
                    "column_name": "ID",
                    "ordinal_position": 1,
                    "column_default": None,
                    "is_nullable": "YES",
                    "data_type": "NUMBER",
                    "character_maximum_length": None,
                    "character_octet_length": None,
                    "numeric_precision": 38,
                    "numeric_precision_radix": 10,
                    "numeric_scale": 0,
                    "datetime_precision": None,
                    "interval_type": None,
                    "interval_precision": None,
                    "character_set_catalog": None,
                    "character_set_schema": None,
                    "character_set_name": None,
                    "collation_catalog": None,
                    "collation_schema": None,
                    "collation_name": None,
                    "domain_catalog": None,
                    "domain_schema": None,
                    "domain_name": None,
                    "udt_catalog": None,
                    "udt_schema": None,
                    "udt_name": None,
                    "scope_catalog": None,
                    "scope_schema": None,
                    "scope_name": None,
                    "maximum_cardinality": None,
                    "dtd_identifier": None,
                    "is_self_referencing": "NO",
                    "is_identity": "NO",
                    "identity_generation": None,
                    "identity_start": None,
                    "identity_increment": None,
                    "identity_maximum": None,
                    "identity_minimum": None,
                    "identity_cycle": None,
                    "comment": None,
                }
            ],
        },
    ]
    for column_dict in expected_view_columns:
        compare(
            metadata_service.views[column_dict["table_id"]].table_columns,
            column_dict["columns"],
        )

    expected_materializedviews = [
        {
            "schema": "VIEWS",
            "name": "MAT_VIEW1",
            "database_name": "TWZ_META",
            "object_type": DbObjectType.MATERIALIZEDVIEW,
        }
    ]
    compare(metadata_service.materializedviews, expected_materializedviews)
    for materializedview in metadata_service.materializedviews:
        assert isinstance(materializedview, mio.InstanceMaterializedView)
        for column in materializedview.table_columns:
            assert isinstance(column, mio.ColumnInstance)

    expected_materializedview_columns = [
        {
            "table_id": 0,
            "columns": [
                {
                    "database_name": "TWZ_META",
                    "object_schema": "VIEWS",
                    "object_name": "MAT_VIEW1",
                    "column_name": "ID",
                    "ordinal_position": 1,
                    "column_default": None,
                    "is_nullable": "YES",
                    "data_type": "NUMBER",
                    "character_maximum_length": None,
                    "character_octet_length": None,
                    "numeric_precision": 38,
                    "numeric_precision_radix": 10,
                    "numeric_scale": 0,
                    "datetime_precision": None,
                    "interval_type": None,
                    "interval_precision": None,
                    "character_set_catalog": None,
                    "character_set_schema": None,
                    "character_set_name": None,
                    "collation_catalog": None,
                    "collation_schema": None,
                    "collation_name": None,
                    "domain_catalog": None,
                    "domain_schema": None,
                    "domain_name": None,
                    "udt_catalog": None,
                    "udt_schema": None,
                    "udt_name": None,
                    "scope_catalog": None,
                    "scope_schema": None,
                    "scope_name": None,
                    "maximum_cardinality": None,
                    "dtd_identifier": None,
                    "is_self_referencing": "NO",
                    "is_identity": "NO",
                    "identity_generation": None,
                    "identity_start": None,
                    "identity_increment": None,
                    "identity_maximum": None,
                    "identity_minimum": None,
                    "identity_cycle": None,
                    "comment": None,
                }
            ],
        }
    ]
    for column_dict in expected_materializedview_columns:
        compare(
            metadata_service.materializedviews[column_dict["table_id"]].table_columns,
            column_dict["columns"],
        )

    expected_dynamictables = [
        {
        'database_name': 'TWZ_META',
        'schema': 'DATA',
        'object_type': DbObjectType.DYNAMICTABLE,
        'name': 'DYNAMICTABLE1',
        'table_type': 'BASE TABLE', 
        'query_text': "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;", 
        'clustering_key': None, 
        'retention_time': 0, 
        'schema_retention_time': 1, 
        'comment': 'TEST COMMENT', 
        'target_lag': '2 hours', 
        'warehouse': 'COMPUTE_WH', 
        'refresh_mode': 'INCREMENTAL'
    },
    ]
    compare(metadata_service.dynamictables, expected_dynamictables)
    for dynamictable in metadata_service.dynamictables:
        assert isinstance(dynamictable, mio.InstanceDynamicTable)
        for column in dynamictable.table_columns:
            assert isinstance(column, mio.ColumnInstance)

    expected_dynamictable_columns = [
        {
            "table_id": 0,
            "columns": [
                {
                    "database_name": "TWZ_META",
                    "object_schema": "DATA",
                    "object_name": "DYNAMICTABLE1",
                    "column_name": "COLUMN_1",
                    "ordinal_position": 1,
                    "column_default": None,
                    "is_nullable": "YES",
                    "data_type": "TEXT",
                    "character_maximum_length": 16777216,
                    "character_octet_length": 16777216,
                    "numeric_precision": None,
                    "numeric_precision_radix": None,
                    "numeric_scale": None,
                    "datetime_precision": None,
                    "interval_type": None,
                    "interval_precision": None,
                    "character_set_catalog": None,
                    "character_set_schema": None,
                    "character_set_name": None,
                    "collation_catalog": None,
                    "collation_schema": None,
                    "collation_name": None,
                    "domain_catalog": None,
                    "domain_schema": None,
                    "domain_name": None,
                    "udt_catalog": None,
                    "udt_schema": None,
                    "udt_name": None,
                    "scope_catalog": None,
                    "scope_schema": None,
                    "scope_name": None,
                    "maximum_cardinality": None,
                    "dtd_identifier": None,
                    "is_self_referencing": "NO",
                    "is_identity": "NO",
                    "identity_generation": None,
                    "identity_start": None,
                    "identity_increment": None,
                    "identity_maximum": None,
                    "identity_minimum": None,
                    "identity_cycle": None,
                    "comment": None,
                },
                {
                    "database_name": "TWZ_META",
                    "object_schema": "DATA",
                    "object_name": "DYNAMICTABLE1",
                    "column_name": "COLUMN_2",
                    "ordinal_position": 2,
                    "column_default": None,
                    "is_nullable": "YES",
                    "data_type": "TEXT",
                    "character_maximum_length": 16777216,
                    "character_octet_length": 16777216,
                    "numeric_precision": None,
                    "numeric_precision_radix": None,
                    "numeric_scale": None,
                    "datetime_precision": None,
                    "interval_type": None,
                    "interval_precision": None,
                    "character_set_catalog": None,
                    "character_set_schema": None,
                    "character_set_name": None,
                    "collation_catalog": None,
                    "collation_schema": None,
                    "collation_name": None,
                    "domain_catalog": None,
                    "domain_schema": None,
                    "domain_name": None,
                    "udt_catalog": None,
                    "udt_schema": None,
                    "udt_name": None,
                    "scope_catalog": None,
                    "scope_schema": None,
                    "scope_name": None,
                    "maximum_cardinality": None,
                    "dtd_identifier": None,
                    "is_self_referencing": "NO",
                    "is_identity": "NO",
                    "identity_generation": None,
                    "identity_start": None,
                    "identity_increment": None,
                    "identity_maximum": None,
                    "identity_minimum": None,
                    "identity_cycle": None,
                    "comment": None,
                }
            ],
        },
    ]
    for column_dict in expected_dynamictable_columns:
        compare(
            metadata_service.dynamictables[column_dict["table_id"]].table_columns,
            column_dict["columns"],
        )

    expected_networkrules = [
        {
                "database_name": "TWZ_META",
                "schema": "MISC",
                "name": "MY_NETWORK_RULE1",
                "type": "IPV4",
                "mode": "INGRESS",
                "value_list": "('0.0.0.0')",
                "comment": "whitelist"
            }
    ]
    compare(metadata_service.networkrules, expected_networkrules)
    for networkrule in metadata_service.networkrules:
        assert isinstance(networkrule, mio.InstanceNetworkRule)


@pytest.mark.parametrize(
    "config_json_schema_list, schemas_on_db_list, expected",
    [
        (
            {"blacklist": []},
            ["MY_SCHEMA1", "MY_SCHEMA2", "MY_SCHEMA3", "MY_SCHEMA4"],
            ["MY_SCHEMA1", "MY_SCHEMA2", "MY_SCHEMA3", "MY_SCHEMA4"],
        ),
        (
            {"blacklist": ["MY_SCHEMA1", "MY_SCHEMA4"]},
            ["MY_SCHEMA1", "MY_SCHEMA2", "MY_SCHEMA3", "MY_SCHEMA4"],
            ["MY_SCHEMA2", "MY_SCHEMA3"],
        ),
        (
            {"blacklist": ["MY_SCHEMA1", "MY_SCHEMA_NOT_ON_DB"]},
            ["MY_SCHEMA1", "MY_SCHEMA2", "MY_SCHEMA3", "MY_SCHEMA4"],
            ["MY_SCHEMA2", "MY_SCHEMA3", "MY_SCHEMA4"],
        ),
        (
            {"whitelist": []},
            ["MY_SCHEMA1", "MY_SCHEMA2", "MY_SCHEMA3", "MY_SCHEMA4"],
            [],
        ),
        (
            {"whitelist": ["MY_SCHEMA1", "MY_SCHEMA2", "MY_SCHEMA3", "MY_SCHEMA4"]},
            ["MY_SCHEMA1", "MY_SCHEMA2", "MY_SCHEMA3", "MY_SCHEMA4"],
            ["MY_SCHEMA1", "MY_SCHEMA2", "MY_SCHEMA3", "MY_SCHEMA4"],
        ),
        (
            {"whitelist": ["MY_SCHEMA2", "MY_SCHEMA3"]},
            ["MY_SCHEMA1", "MY_SCHEMA2", "MY_SCHEMA3", "MY_SCHEMA4"],
            ["MY_SCHEMA2", "MY_SCHEMA3"],
        ),
        (
            {"whitelist": ["MY_SCHEMA2", "MY_SCHEMA_NOT_ON_DB"]},
            ["MY_SCHEMA1", "MY_SCHEMA2", "MY_SCHEMA3", "MY_SCHEMA4"],
            ["MY_SCHEMA2"],
        ),
    ],
)
def test_get_filtered_schema_name_list(
    config_json_schema_list, schemas_on_db_list, expected
):
    metadata_service = mds.MetadataService(DummySnowClient())
    metadata_service._get_meta_data_schema_names = MagicMock(
        return_value=schemas_on_db_list
    )
    assert (
        metadata_service._get_filtered_schema_name_list(config_json_schema_list)
        == expected
    )
