
from typing import List
from unittest.mock import patch

import acedeploy.core.model_instance_objects as mio
import acedeploy.core.model_object_action_entities as oae
import acedeploy.core.model_solution_entities as mse
import pytest
from acedeploy.core.model_instance_objects import (
    InstanceFileformat,
    InstanceMaskingPolicy,
    InstancePipe,
    InstanceRowAccessPolicy,
    InstanceSchema,
    InstanceSequence,
    InstanceStage,
    InstanceStream,
    InstanceView,
    InstanceDynamicTable,
    InstanceNetworkRule,
)
from acedeploy.core.model_sql_entities import DbActionType, DbObjectType
from pytest_lazyfixture import lazy_fixture  # pylint: disable=unused-import

from model_instance_object_fixtures import (
    metadata_fileformat,  # pylint: disable=unused-import
    metadata_function,
    metadata_maskingpolicy,
    metadata_pipe,
    metadata_procedure,
    metadata_rowaccesspolicy,
    metadata_schema,
    metadata_sequence,
    metadata_stage,
    metadata_stream,
    metadata_task,
    metadata_externaltable,
    metadata_dynamictable,
    metadata_networkrule,
)


@pytest.mark.parametrize(
    "input, expected_id, expected_full_name, expected_repr",
    [
        (
            oae.ViewAction("my_schema", "my_object", DbActionType.ADD, "dummy content"),
            "DbObjectType.VIEW MY_SCHEMA.MY_OBJECT",
            "MY_SCHEMA.MY_OBJECT",
            "ViewAction: DbObjectType.VIEW MY_SCHEMA.MY_OBJECT",
        ),
        (
            oae.FileformatAction(
                "my_schema", "my_object", DbActionType.ADD, "dummy content"
            ),
            "DbObjectType.FILEFORMAT MY_SCHEMA.MY_OBJECT",
            "MY_SCHEMA.MY_OBJECT",
            "FileformatAction: DbObjectType.FILEFORMAT MY_SCHEMA.MY_OBJECT",
        ),
        (
            oae.ExternalTableAction(
                "my_schema", "my_object", DbActionType.ADD, "dummy content"
            ),
            "DbObjectType.EXTERNALTABLE MY_SCHEMA.MY_OBJECT",
            "MY_SCHEMA.MY_OBJECT",
            "ExternalTableAction: DbObjectType.EXTERNALTABLE MY_SCHEMA.MY_OBJECT",
        ),
        (
            oae.StageAction(
                "my_schema", "my_object", DbActionType.ADD, "dummy content"
            ),
            "DbObjectType.STAGE MY_SCHEMA.MY_OBJECT",
            "MY_SCHEMA.MY_OBJECT",
            "StageAction: DbObjectType.STAGE MY_SCHEMA.MY_OBJECT",
        ),
        (
            oae.FunctionAction(
                "my_schema", "my_object", DbActionType.ADD, "", "dummy content"
            ),
            "DbObjectType.FUNCTION MY_SCHEMA.MY_OBJECT ()",
            "MY_SCHEMA.MY_OBJECT ()",
            "FunctionAction: DbObjectType.FUNCTION MY_SCHEMA.MY_OBJECT ()",
        ),
        (
            oae.FunctionAction(
                "my_schema",
                "my_object",
                DbActionType.ADD,
                ["FLOAT", "INT"],
                "dummy content",
            ),
            "DbObjectType.FUNCTION MY_SCHEMA.MY_OBJECT (FLOAT, NUMBER)",
            "MY_SCHEMA.MY_OBJECT (FLOAT, NUMBER)",
            "FunctionAction: DbObjectType.FUNCTION MY_SCHEMA.MY_OBJECT (FLOAT, NUMBER)",
        ),
        (
            oae.ProcedureAction(
                "my_schema", "my_object", DbActionType.ADD, "", "dummy content"
            ),
            "DbObjectType.PROCEDURE MY_SCHEMA.MY_OBJECT ()",
            "MY_SCHEMA.MY_OBJECT ()",
            "ProcedureAction: DbObjectType.PROCEDURE MY_SCHEMA.MY_OBJECT ()",
        ),
        (
            oae.ProcedureAction(
                "my_schema",
                "my_object",
                DbActionType.ADD,
                ["FLOAT", "INT"],
                "dummy content",
            ),
            "DbObjectType.PROCEDURE MY_SCHEMA.MY_OBJECT (FLOAT, NUMBER)",
            "MY_SCHEMA.MY_OBJECT (FLOAT, NUMBER)",
            "ProcedureAction: DbObjectType.PROCEDURE MY_SCHEMA.MY_OBJECT (FLOAT, NUMBER)",
        ),
        (
            oae.SchemaAction(
                "my_schema", "my_schema", DbActionType.ADD, "dummy content"
            ),
            "DbObjectType.SCHEMA MY_SCHEMA",
            "MY_SCHEMA",
            "SchemaAction: DbObjectType.SCHEMA MY_SCHEMA",
        ),
        (
            oae.StreamAction(
                "my_schema", "my_stream", DbActionType.ADD, "dummy content"
            ),
            "DbObjectType.STREAM MY_SCHEMA.MY_STREAM",
            "MY_SCHEMA.MY_STREAM",
            "StreamAction: DbObjectType.STREAM MY_SCHEMA.MY_STREAM",
        ),
        (
            oae.TaskAction("my_schema", "my_task", DbActionType.ADD, "dummy content"),
            "DbObjectType.TASK MY_SCHEMA.MY_TASK",
            "MY_SCHEMA.MY_TASK",
            "TaskAction: DbObjectType.TASK MY_SCHEMA.MY_TASK",
        ),
        (
            oae.PipeAction("my_schema", "my_pipe", DbActionType.ADD, "dummy content"),
            "DbObjectType.PIPE MY_SCHEMA.MY_PIPE",
            "MY_SCHEMA.MY_PIPE",
            "PipeAction: DbObjectType.PIPE MY_SCHEMA.MY_PIPE",
        ),
        (
            oae.SequenceAction(
                "my_schema", "my_sequence", DbActionType.ADD, "dummy content"
            ),
            "DbObjectType.SEQUENCE MY_SCHEMA.MY_SEQUENCE",
            "MY_SCHEMA.MY_SEQUENCE",
            "SequenceAction: DbObjectType.SEQUENCE MY_SCHEMA.MY_SEQUENCE",
        ),
        (
            oae.MaskingPolicyAction(
                "my_schema", "my_maskingpolicy", DbActionType.ADD, "dummy content"
            ),
            "DbObjectType.MASKINGPOLICY MY_SCHEMA.MY_MASKINGPOLICY",
            "MY_SCHEMA.MY_MASKINGPOLICY",
            "MaskingPolicyAction: DbObjectType.MASKINGPOLICY MY_SCHEMA.MY_MASKINGPOLICY",
        ),
        (
            oae.RowAccessPolicyAction(
                "my_schema", "my_rowaccesspolicy", DbActionType.ADD, "dummy content"
            ),
            "DbObjectType.ROWACCESSPOLICY MY_SCHEMA.MY_ROWACCESSPOLICY",
            "MY_SCHEMA.MY_ROWACCESSPOLICY",
            "RowAccessPolicyAction: DbObjectType.ROWACCESSPOLICY MY_SCHEMA.MY_ROWACCESSPOLICY",
        ),
        (
            oae.DynamicTableAction(
                "my_schema", "my_dynamictable", DbActionType.ADD, "dummy content"
            ),
            "DbObjectType.DYNAMICTABLE MY_SCHEMA.MY_DYNAMICTABLE",
            "MY_SCHEMA.MY_DYNAMICTABLE",
            "DynamicTableAction: DbObjectType.DYNAMICTABLE MY_SCHEMA.MY_DYNAMICTABLE",
        ),
        (
            oae.NetworkRuleAction(
                "my_schema", "my_networkrule", DbActionType.ADD, "dummy content"
            ),
            "DbObjectType.NETWORKRULE MY_SCHEMA.MY_NETWORKRULE",
            "MY_SCHEMA.MY_NETWORKRULE",
            "NetworkRuleAction: DbObjectType.NETWORKRULE MY_SCHEMA.MY_NETWORKRULE",
        ),
    ],
)
def test_ActionObject_properties(input, expected_id, expected_full_name, expected_repr):
    assert input.id == expected_id
    assert input.full_name == expected_full_name
    assert str(input) == expected_repr
    assert repr(input) == expected_repr


@pytest.mark.parametrize(
    "solution_object, action, expected_type",
    [
        (
            mse.SolutionTable(
                "/my/file/path/myschema.mytable.sql",
                "CREATE OR REPLACE TABLE MYSCHEMA.MYTABLE ()",
            ),
            DbActionType.ADD,
            DbObjectType.TABLE,
        ),
        (
            mse.SolutionView(
                "/my/file/path/myschema.myview.sql",
                "CREATE OR REPLACE VIEW MYSCHEMA.MYVIEW ()",
            ),
            DbActionType.ADD,
            DbObjectType.VIEW,
        ),
        (
            mse.SolutionMaterializedView(
                "/my/file/path/myschema.mymatview.sql",
                "CREATE OR REPLACE MATERIALIZED VIEW MYSCHEMA.MYMATVIEW ()",
            ),
            DbActionType.ADD,
            DbObjectType.MATERIALIZEDVIEW,
        ),
        (
            mse.SolutionFunction(
                "/my/file/path/myschema.myfunction.sql",
                "CREATE OR REPLACE FUNCTION MYSCHEMA.MYFUNCTION (V VARCHAR)",
            ),
            DbActionType.ADD,
            DbObjectType.FUNCTION,
        ),
        (
            mse.SolutionProcedure(
                "/my/file/path/myschema.myprocedure.sql",
                "CREATE OR REPLACE PROCEDURE MYSCHEMA.MYPROCEDURE (V VARCHAR)",
            ),
            DbActionType.ADD,
            DbObjectType.PROCEDURE,
        ),
        (
            mse.SolutionFileformat(
                "/my/file/path/myschema.myfileformat.sql",
                "CREATE OR REPLACE FILE FORMAT MYSCHEMA.MYFILEFORMAT ()",
            ),
            DbActionType.ADD,
            DbObjectType.FILEFORMAT,
        ),
        (
            mse.SolutionExternalTable(
                "/my/file/path/myschema.myexttable.sql",
                "CREATE OR REPLACE EXTERNAL TABLE MYSCHEMA.MYEXTTABLE ()",
            ),
            DbActionType.ADD,
            DbObjectType.EXTERNALTABLE,
        ),
        (
            mse.SolutionStage(
                "/my/file/path/myschema.mystage.sql",
                "CREATE OR REPLACE STAGE MYSCHEMA.MYSTAGE ()",
            ),
            DbActionType.ADD,
            DbObjectType.STAGE,
        ),
        (
            mse.SolutionStream(
                "/my/file/path/myschema.mystream.sql",
                "CREATE OR REPLACE STREAM MYSCHEMA.MYSTREAM ()",
            ),
            DbActionType.ADD,
            DbObjectType.STREAM,
        ),
        (
            mse.SolutionTask(
                "/my/file/path/myschema.mytask.sql",
                "CREATE OR REPLACE TASK MYSCHEMA.MYTASK ()",
            ),
            DbActionType.ADD,
            DbObjectType.TASK,
        ),
        (
            mse.SolutionPipe(
                "/my/file/path/myschema.mypipe.sql",
                "CREATE OR REPLACE PIPE MYSCHEMA.MYPIPE ()",
            ),
            DbActionType.ADD,
            DbObjectType.PIPE,
        ),
        (
            mse.SolutionSequence(
                "/my/file/path/myschema.mysequence.sql",
                "CREATE SEQUENCE MYSCHEMA.MYSEQUENCE ...",
            ),
            DbActionType.ADD,
            DbObjectType.SEQUENCE,
            # ),(
            #     mse.SolutionMaskingP('/my/file/path/myschema.mysequence.sql', 'CREATE SEQUENCE MYSCHEMA.MYSEQUENCE ...'), DbActionType.ADD, DbObjectType.SEQUENCE,
            # ),(
            #     mse.SolutionSequence('/my/file/path/myschema.mysequence.sql', 'CREATE SEQUENCE MYSCHEMA.MYSEQUENCE ...'), DbActionType.ADD, DbObjectType.SEQUENCE,
        ),
        (
            mse.SolutionDynamicTable(
                "/my/file/path/myschema.mydynamictable.sql",
                "CREATE OR REPLACE DYNAMIC TABLE MYSCHEMA.MYDYNAMICTABLE ()",
            ),
            DbActionType.ADD,
            DbObjectType.DYNAMICTABLE,
        ),
        (
            mse.SolutionNetworkRule(
                "/my/file/path/myschema.mynetworkrule.sql",
                "CREATE OR REPLACE NETWORK RULE MYSCHEMA.MYNETWORKRULE ()",
            ),
            DbActionType.ADD,
            DbObjectType.NETWORKRULE,
        ),
    ],
)
def test_DbObjectAction_factory_from_solution_object(
    solution_object, action, expected_type
):
    # arrange
    object_action = oae.DbObjectAction.factory_from_solution_object(
        solution_object, action
    )

    # assert
    assert object_action.object_type == expected_type


@pytest.mark.parametrize(
    "solution_object, action",
    [
        (
            mse.SolutionTable(
                "/my/file/path/myschema.mytable.sql",
                "CREATE OR REPLACE TABLE MYSCHEMA.MYTABLE ()",
            ),
            DbActionType.ALTER,
        )
    ],
)
def test_DbObjectAction_factory_from_solution_object_error(solution_object, action):
    with pytest.raises(ValueError):
        __ = oae.DbObjectAction.factory_from_solution_object(solution_object, action)


@pytest.mark.parametrize(
    "instance_object_class, metadata, action, expected_type",
    [
        (
            mio.InstanceSchema,
            pytest.lazy_fixture("metadata_schema"),
            DbActionType.DROP,
            DbObjectType.SCHEMA,
        ),
        (
            mio.InstanceFileformat,
            pytest.lazy_fixture("metadata_fileformat"),
            DbActionType.DROP,
            DbObjectType.FILEFORMAT,
        ),
        (
            mio.InstanceExternalTable,
            pytest.lazy_fixture("metadata_externaltable"),
            DbActionType.DROP,
            DbObjectType.EXTERNALTABLE,
        ),
        (
            mio.InstanceStage,
            pytest.lazy_fixture("metadata_stage"),
            DbActionType.DROP,
            DbObjectType.STAGE,
        ),
        (
            mio.InstanceFunction,
            pytest.lazy_fixture("metadata_function"),
            DbActionType.DROP,
            DbObjectType.FUNCTION,
        ),
        (
            mio.InstanceProcedure,
            pytest.lazy_fixture("metadata_procedure"),
            DbActionType.DROP,
            DbObjectType.PROCEDURE,
        ),
        (
            mio.InstanceTable,
            {
                "DATABASE_NAME": "TWZ_META",
                "SCHEMA_NAME": "DATA",
                "OBJECT_NAME": "TABLE2",
                "TABLE_TYPE": "BASE TABLE",
                "CLUSTERING_KEY": None,
                "RETENTION_TIME": 1,
                "SCHEMA_RETENTION_TIME": 1,
                "COMMENT": "",
                "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH":11,"CHARACTER_OCTET_LENGTH":44,"COLLATION_NAME":"en-ci","COLUMN_DEFAULT":"\'x\'","COLUMN_NAME":"T4","DATABASE_NAME":"TWZ_META","DATA_TYPE":"TEXT","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","ORDINAL_POSITION":4,"TABLE_NAME":"TABLE2","TABLE_SCHEMA":"DATA"},{"CHARACTER_MAXIMUM_LENGTH":12,"CHARACTER_OCTET_LENGTH":48,"COLLATION_NAME":"en-ci","COLUMN_NAME":"T2","DATABASE_NAME":"TWZ_META","DATA_TYPE":"TEXT","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","ORDINAL_POSITION":2,"TABLE_NAME":"TABLE2","TABLE_SCHEMA":"DATA"},{"CHARACTER_MAXIMUM_LENGTH":11,"CHARACTER_OCTET_LENGTH":44,"COLUMN_NAME":"T1","DATABASE_NAME":"TWZ_META","DATA_TYPE":"TEXT","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","ORDINAL_POSITION":1,"TABLE_NAME":"TABLE2","TABLE_SCHEMA":"DATA"},{"CHARACTER_MAXIMUM_LENGTH":12,"CHARACTER_OCTET_LENGTH":48,"COLLATION_NAME":"en-ci","COLUMN_NAME":"T3","DATABASE_NAME":"TWZ_META","DATA_TYPE":"TEXT","IS_IDENTITY":"NO","IS_NULLABLE":"NO","IS_SELF_REFERENCING":"NO","ORDINAL_POSITION":3,"TABLE_NAME":"TABLE2","TABLE_SCHEMA":"DATA"}],
                "constraint_foreign_keys": [],
                "constraint_primary_keys": [],
                "constraint_unique_keys": [],
            },
            DbActionType.DROP,
            DbObjectType.TABLE,
        ),
        (
            mio.InstanceView,
            {
                "DATABASE_NAME": "TWZ_META",
                "SCHEMA_NAME": "VIEWS",
                "OBJECT_NAME": "VIEW1",
                "TABLE_TYPE": "VIEW",
                "CLUSTERING_KEY": None,
                "VIEW_DEFINITION": "DUMMY DEFINITION",
                "IS_SECURE": "NO",
                "COMMENT": None,
                "COLUMN_DETAILS": [{"COLUMN_NAME":"ID","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}],
            },
            DbActionType.DROP,
            DbObjectType.VIEW,
        ),
        (
            mio.InstanceMaterializedView,
            {
                "DATABASE_NAME": "TWZ_META",
                "SCHEMA_NAME": "VIEWS",
                "OBJECT_NAME": "VIEW1",
                "TABLE_TYPE": "VIEW",
                "CLUSTERING_KEY": None,
                "COMMENT": None,
                "COLUMN_DETAILS": [{"COLUMN_NAME":"ID","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}],
            },
            DbActionType.DROP,
            DbObjectType.MATERIALIZEDVIEW,
        ),
        (
            mio.InstanceStream,
            {
                "name": "MYSTREAM",
                "database_name": "TWZ_META",
                "schema_name": "MISC",
                "comment": "",
                "table_name": "TWZ_META.DATA.TABLE1",
                "type": "DELTA",
                "stale": "false",
                "mode": "DEFAULT",
            },
            DbActionType.DROP,
            DbObjectType.STREAM,
        ),
        (
            mio.InstanceTask,
            {
                "name": "MYTASK",
                "database_name": "TWZ_META",
                "schema_name": "MISC",
                "comment": "",
                "warehouse": "COMPUTE_WH",
                "schedule": "USING CRON * * * * * UTC",
                "predecessors": None,
                "mode": "DEFAULT",
                "state": "suspended",
                "definition": "INSERT INTO demo_db.public.t VALUES(1, 1, 1)",
                "condition": None,
                "allow_overlapping_execution": False,
            },
            DbActionType.DROP,
            DbObjectType.TASK,
        ),
        (
            mio.InstancePipe,
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
            },
            DbActionType.DROP,
            DbObjectType.PIPE,
        ),
        (
            mio.InstanceSequence,
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
            },
            DbActionType.DROP,
            DbObjectType.SEQUENCE,
        ),
        (
            mio.InstanceMaskingPolicy,
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
            DbActionType.DROP,
            DbObjectType.MASKINGPOLICY,
        ),
        (
            mio.InstanceRowAccessPolicy,
            {
                "database_name": "TWZ_META",
                "schema_name": "POLICIES",
                "name": "MYROWACCESSPOLICY",
                "kind": "MASKING_POLICY",
                "comment": "my comment",
                "signature": "(N NUMBER)",
                "return_type": "BOOLEAN",
                "body": "TRUE --dummy policy body",
            },
            DbActionType.DROP,
            DbObjectType.ROWACCESSPOLICY,
        ),
        (
            mio.InstanceDynamicTable,
            {
                "DATABASE_NAME": "TWZ_META",
                "SCHEMA_NAME": "DATA",
                "OBJECT_NAME": "DYNAMICTABLE1",
                "TABLE_TYPE": "BASE TABLE",
                "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                "CLUSTERING_KEY": None,
                "RETENTION_TIME": 0,
                "SCHEMA_RETENTION_TIME": 1,
                "COMMENT": "MY COMMENT",
                "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                "TARGET_LAG": "2 hours",
                "WAREHOUSE": "COMPUTE_WH",
                "REFRESH_MODE": "INCREMENTAL",
            },
            DbActionType.DROP,
            DbObjectType.DYNAMICTABLE,
        ),
        (
            mio.InstanceNetworkRule,
            {
                "DATABASE_NAME": "TWZ_META",
                "SCHEMA_NAME": "MISC",
                "OBJECT_NAME": "MY_NETWORK_RULE1",
                "TYPE": "IPV4",
                "MODE": "INGRESS",
                "VALUE_LIST": "('0.0.0.0')",
                "COMMENT": "whitelist"
            },
            DbActionType.DROP,
            DbObjectType.NETWORKRULE,
        ),
    ],
)
def test_DbObjectAction_factory_from_instance_object(
    instance_object_class, metadata, action, expected_type
):
    # arrange
    instance_object = instance_object_class(metadata)
    object_action = oae.DbObjectAction.factory_from_instance_object(
        instance_object, action
    )

    # assert
    assert object_action.object_type == expected_type


@pytest.mark.parametrize(
    "instance_object, action",
    [
        (
            mio.InstanceView(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "VIEW1",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "VIEW_DEFINITION": "DUMMY DEFINITION",
                    "IS_SECURE": "NO",
                    "COMMENT": None,
                    "COLUMN_DETAILS": [{"COLUMN_NAME":"ID","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}],
                }
            ),
            DbActionType.ADD,
        ),
        (
            mio.InstanceView(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "VIEW1",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "VIEW_DEFINITION": "DUMMY DEFINITION",
                    "IS_SECURE": "NO",
                    "COMMENT": None,
                    "COLUMN_DETAILS": [{"COLUMN_NAME":"ID","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}],
                }
            ),
            DbActionType.ALTER,
        ),
    ],
)
def test_DbObjectAction_factory_from_instance_object_error(instance_object, action):
    with pytest.raises(ValueError):
        __ = oae.DbObjectAction.factory_from_instance_object(instance_object, action)


def test_generate_statement_object():
    with patch(
        "acedeploy.core.model_object_action_entities.ViewAction._generate_statement"
    ) as mock_generate_statement:
        mock_generate_statement.return_value = "dummy"
        obj = oae.ViewAction(
            "my_schema", "my_object", DbActionType.ADD, "dummy content"
        )
        result = obj.generate_statement_object()
    assert result.schema == "MY_SCHEMA"
    assert result.name == "MY_OBJECT"
    assert result.statement == "dummy"
    assert result.object_type == DbObjectType.VIEW


@pytest.mark.parametrize(
    "object_name, schema_name, content, object_type, action, expected_statement",
    [
        (
            "myschema",
            "myschema",
            "CREATE SCHEMA myschema;",
            DbObjectType.SCHEMA,
            DbActionType.ADD,
            "CREATE SCHEMA myschema;",
        ),
        # ALTER SCHEMA is tested below
        (
            "myschema",
            "myschema",
            "",
            DbObjectType.SCHEMA,
            DbActionType.DROP,
            "DROP SCHEMA IF EXISTS myschema",
        ),
        (
            "myview",
            "myschema",
            "CREATE OR REPLACE VIEW myschema.myview AS SELECT * FROM s.t;",
            DbObjectType.VIEW,
            DbActionType.ADD,
            "CREATE VIEW myschema.myview AS SELECT * FROM s.t;",
        ),
        # ALTER VIEW is tested below
        (
            "myview",
            "myschema",
            "",
            DbObjectType.VIEW,
            DbActionType.DROP,
            "DROP VIEW IF EXISTS myschema.myview",
        ),
        (
            "myview",
            "myschema",
            "CREATE OR REPLACE MATERIALIZED VIEW myschema.myview AS SELECT * FROM s.t;",
            DbObjectType.MATERIALIZEDVIEW,
            DbActionType.ADD,
            "CREATE MATERIALIZED VIEW myschema.myview AS SELECT * FROM s.t;",
        ),
        (
            "myview",
            "myschema",
            "CREATE OR REPLACE MATERIALIZED VIEW myschema.myview AS SELECT * FROM s.t;",
            DbObjectType.MATERIALIZEDVIEW,
            DbActionType.ALTER,
            "CREATE OR REPLACE MATERIALIZED VIEW myschema.myview AS SELECT * FROM s.t;",
        ),
        (
            "myview",
            "myschema",
            "",
            DbObjectType.MATERIALIZEDVIEW,
            DbActionType.DROP,
            "DROP MATERIALIZED VIEW IF EXISTS myschema.myview",
        ),
        (
            "mytable",
            "myschema",
            "CREATE TABLE myschema.mytable (I INT);",
            DbObjectType.TABLE,
            DbActionType.ADD,
            "CREATE TABLE myschema.mytable (I INT);",
        ),
        # ALTER TABLE is tested below
        (
            "mytable",
            "myschema",
            "",
            DbObjectType.TABLE,
            DbActionType.DROP,
            "DROP TABLE IF EXISTS myschema.mytable",
        ),
        (
            "myfileformat",
            "myschema",
            "CREATE OR REPLACE FILE FORMAT myschema.myfileformat ...;",
            DbObjectType.FILEFORMAT,
            DbActionType.ADD,
            "CREATE FILE FORMAT myschema.myfileformat ...;",
        ),
        # ALTER FILE FORMAT is tested in a separate file
        (
            "myfileformat",
            "myschema",
            "",
            DbObjectType.FILEFORMAT,
            DbActionType.DROP,
            "DROP FILE FORMAT IF EXISTS myschema.myfileformat",
        ),
        (
            "myexttable",
            "myschema",
            "CREATE OR REPLACE EXTERNAL TABLE myschema.myexttable ...;",
            DbObjectType.EXTERNALTABLE,
            DbActionType.ADD,
            "CREATE EXTERNAL TABLE myschema.myexttable ...;",
        ),
        (
            "myexttable",
            "myschema",
            "CREATE OR REPLACE EXTERNAL TABLE myschema.myexttable ...;",
            DbObjectType.EXTERNALTABLE,
            DbActionType.ALTER,
            "CREATE OR REPLACE EXTERNAL TABLE myschema.myexttable ...;",
        ),
        (
            "myexttable",
            "myschema",
            "",
            DbObjectType.EXTERNALTABLE,
            DbActionType.DROP,
            "DROP EXTERNAL TABLE IF EXISTS myschema.myexttable",
        ),
        (
            "mystage",
            "myschema",
            "CREATE OR REPLACE STAGE myschema.mystage ...;",
            DbObjectType.STAGE,
            DbActionType.ADD,
            "CREATE STAGE myschema.mystage ...;",
        ),
        # ALTER STAGE is tested below
        (
            "mystage",
            "myschema",
            "",
            DbObjectType.STAGE,
            DbActionType.DROP,
            "DROP STAGE IF EXISTS myschema.mystage",
        ),
        (
            "mystream",
            "myschema",
            "CREATE OR REPLACE STREAM myschema.mystream ...;",
            DbObjectType.STREAM,
            DbActionType.ADD,
            "CREATE STREAM myschema.mystream ...;",
        ),
        # alter stream is tested below
        (
            "mystream",
            "myschema",
            "",
            DbObjectType.STREAM,
            DbActionType.DROP,
            "DROP STREAM IF EXISTS myschema.mystream",
        ),
        (
            "mytask",
            "myschema",
            "CREATE OR REPLACE TASK myschema.mytask ...;",
            DbObjectType.TASK,
            DbActionType.ADD,
            "CREATE TASK myschema.mytask ...;",
        ),
        (
            "mytask",
            "myschema",
            "CREATE OR REPLACE TASK myschema.mytask ...;",
            DbObjectType.TASK,
            DbActionType.ALTER,
            "CREATE OR REPLACE TASK myschema.mytask ...;",
        ),
        (
            "mytask",
            "myschema",
            "",
            DbObjectType.TASK,
            DbActionType.DROP,
            "DROP TASK IF EXISTS myschema.mytask",
        ),
        (
            "mypipe",
            "myschema",
            "CREATE OR REPLACE PIPE myschema.mypipe ...;",
            DbObjectType.PIPE,
            DbActionType.ADD,
            "CREATE PIPE myschema.mypipe ...;",
        ),
        # alter pipe is tested below
        (
            "mypipe",
            "myschema",
            "",
            DbObjectType.PIPE,
            DbActionType.DROP,
            "DROP PIPE IF EXISTS myschema.mypipe",
        ),
        (
            "mysequence",
            "myschema",
            "CREATE OR REPLACE SEQUENCE myschema.mysequence ...;",
            DbObjectType.SEQUENCE,
            DbActionType.ADD,
            "CREATE SEQUENCE myschema.mysequence ...;",
        ),
        # alter sequence is tested below
        (
            "mysequence",
            "myschema",
            "",
            DbObjectType.SEQUENCE,
            DbActionType.DROP,
            "DROP SEQUENCE IF EXISTS myschema.mysequence",
        ),
        (
            "mymaskingpolicy",
            "myschema",
            "CREATE OR REPLACE MASKING POLICY myschema.mymaskingpolicy ...;",
            DbObjectType.MASKINGPOLICY,
            DbActionType.ADD,
            "CREATE MASKING POLICY myschema.mymaskingpolicy ...;",
        ),
        # alter maskign policy is tested below
        (
            "mymaskingpolicy",
            "myschema",
            "",
            DbObjectType.MASKINGPOLICY,
            DbActionType.DROP,
            "DROP MASKING POLICY IF EXISTS myschema.mymaskingpolicy",
        ),
        (
            "myrowaccesspolicy",
            "myschema",
            "CREATE OR REPLACE ROW ACCESS POLICY myschema.myrowaccesspolicy ...;",
            DbObjectType.ROWACCESSPOLICY,
            DbActionType.ADD,
            "CREATE ROW ACCESS POLICY myschema.myrowaccesspolicy ...;",
        ),
        # alter masking policy is tested below
        (
            "myrowaccesspolicy",
            "myschema",
            "",
            DbObjectType.ROWACCESSPOLICY,
            DbActionType.DROP,
            "DROP ROW ACCESS POLICY IF EXISTS myschema.myrowaccesspolicy",
        ),
        # alter dynamic table is tested below
        (
            "mydynamictable",
            "myschema",
            "CREATE OR REPLACE DYNAMIC TABLE myschema.mydynamictable ...;",
            DbObjectType.DYNAMICTABLE,
            DbActionType.ADD,
            "CREATE DYNAMIC TABLE myschema.mydynamictable ...;",
        ),
        (
            "mydynamictable",
            "myschema",
            "",
            DbObjectType.DYNAMICTABLE,
            DbActionType.DROP,
            "DROP DYNAMIC TABLE IF EXISTS myschema.mydynamictable",
        ),
        # alter network rule is tested below
        (
            "mynetworkrule",
            "myschema",
            "CREATE OR REPLACE NETWORK RULE myschema.mynetworkrule ...;",
            DbObjectType.NETWORKRULE,
            DbActionType.ADD,
            "CREATE NETWORK RULE myschema.mynetworkrule ...;",
        ),
        (
            "mynetworkrule",
            "myschema",
            "",
            DbObjectType.NETWORKRULE,
            DbActionType.DROP,
            "DROP NETWORK RULE IF EXISTS myschema.mynetworkrule",
        ),
    ],
)
def test_DbObjectAction_statement(
    object_name, schema_name, content, object_type, action, expected_statement
):
    # arrange
    object_action = oae.DbObjectAction.factory(
        schema_name, object_name, object_type, action, file_content=content
    )

    # act
    statement = object_action._generate_statement()

    # assert
    assert statement.lower() == expected_statement.lower()


@pytest.mark.parametrize(
    "object_name, schema_name, file_content, object_type, actions_type, parameters, expected_statement",
    [
        (
            "myfunction",
            "myschema",
            "CREATE FUNCTION myschema.myfunction;",
            DbObjectType.FUNCTION,
            DbActionType.DROP,
            [],
            "DROP FUNCTION IF EXISTS myschema.myfunction ()",
        ),
        (
            "myproc",
            "myschema",
            "CREATE PROCEDURE myschema.myproc;",
            DbObjectType.PROCEDURE,
            DbActionType.DROP,
            [],
            "DROP PROCEDURE IF EXISTS myschema.myproc ()",
        ),
        (
            "myfunction",
            "myschema",
            "CREATE FUNCTION myschema.myfunction;",
            DbObjectType.FUNCTION,
            DbActionType.DROP,
            ["param1", "param2"],
            "DROP FUNCTION IF EXISTS myschema.myfunction (param1, param2)",
        ),
        (
            "myproc",
            "myschema",
            "CREATE PROCEDURE myschema.myproc;",
            DbObjectType.PROCEDURE,
            DbActionType.DROP,
            ["param1", "param2"],
            "DROP PROCEDURE IF EXISTS myschema.myproc (param1, param2)",
        ),
    ],
)
def test_drop_parameters_object_statement(
    object_name,
    schema_name,
    file_content,
    object_type,
    actions_type,
    parameters,
    expected_statement,
):
    # arrange
    object_action = oae.DbObjectAction.factory(
        schema_name,
        object_name,
        object_type,
        actions_type,
        file_content=file_content,
        parameters=parameters,
    )
    # act
    statement = object_action._generate_statement()

    # assert
    assert statement.lower() == expected_statement.lower()


# region schema alter


@pytest.mark.parametrize(
    "current_instance, desired_instance, expected",
    [
        (  # current == desired (no changes required)
            InstanceSchema(
                {
                    "DATABASE_NAME": "my_db",
                    "SCHEMA_NAME": "my_schema",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 1,
                    "DATABASE_RETENTION_TIME": 1,
                    "COMMENT": None,
                }
            ),
            InstanceSchema(
                {
                    "DATABASE_NAME": "my_db",
                    "SCHEMA_NAME": "my_schema",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 1,
                    "DATABASE_RETENTION_TIME": 1,
                    "COMMENT": None,
                }
            ),
            "",
        ),
        (  # set comment
            InstanceSchema(
                {
                    "DATABASE_NAME": "my_db",
                    "SCHEMA_NAME": "my_schema",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 1,
                    "DATABASE_RETENTION_TIME": 1,
                    "COMMENT": None,
                }
            ),
            InstanceSchema(
                {
                    "DATABASE_NAME": "my_db",
                    "SCHEMA_NAME": "my_schema",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 1,
                    "DATABASE_RETENTION_TIME": 1,
                    "COMMENT": "test",
                }
            ),
            "ALTER SCHEMA MY_SCHEMA SET COMMENT = 'test';",
        ),
        (  # unset comment
            InstanceSchema(
                {
                    "DATABASE_NAME": "my_db",
                    "SCHEMA_NAME": "my_schema",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 1,
                    "DATABASE_RETENTION_TIME": 1,
                    "COMMENT": "test",
                }
            ),
            InstanceSchema(
                {
                    "DATABASE_NAME": "my_db",
                    "SCHEMA_NAME": "my_schema",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 1,
                    "DATABASE_RETENTION_TIME": 1,
                    "COMMENT": None,
                }
            ),
            "ALTER SCHEMA MY_SCHEMA UNSET COMMENT;",
        ),
        (  # data retention time
            InstanceSchema(
                {
                    "DATABASE_NAME": "my_db",
                    "SCHEMA_NAME": "my_schema",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 90,
                    "DATABASE_RETENTION_TIME": 90,
                    "COMMENT": None,
                }
            ),
            InstanceSchema(
                {
                    "DATABASE_NAME": "my_db",
                    "SCHEMA_NAME": "my_schema",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 90,
                    "DATABASE_RETENTION_TIME": 90,
                    "COMMENT": None,
                }
            ),
            "",
        ),
        (  # data retention time
            InstanceSchema(
                {
                    "DATABASE_NAME": "my_db",
                    "SCHEMA_NAME": "my_schema",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 1,
                    "DATABASE_RETENTION_TIME": 90,
                    "COMMENT": None,
                }
            ),
            InstanceSchema(
                {
                    "DATABASE_NAME": "my_db",
                    "SCHEMA_NAME": "my_schema",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 90,
                    "DATABASE_RETENTION_TIME": 90,
                    "COMMENT": None,
                }
            ),
            "ALTER SCHEMA MY_SCHEMA UNSET DATA_RETENTION_TIME_IN_DAYS;",
        ),
        (  # data retention time
            InstanceSchema(
                {
                    "DATABASE_NAME": "my_db",
                    "SCHEMA_NAME": "my_schema",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 90,
                    "DATABASE_RETENTION_TIME": 1,
                    "COMMENT": None,
                }
            ),
            InstanceSchema(
                {
                    "DATABASE_NAME": "my_db",
                    "SCHEMA_NAME": "my_schema",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 90,
                    "DATABASE_RETENTION_TIME": 90,
                    "COMMENT": None,
                }
            ),
            "ALTER SCHEMA MY_SCHEMA UNSET DATA_RETENTION_TIME_IN_DAYS;",
        ),
        (  # data retention time
            InstanceSchema(
                {
                    "DATABASE_NAME": "my_db",
                    "SCHEMA_NAME": "my_schema",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 90,
                    "DATABASE_RETENTION_TIME": 90,
                    "COMMENT": None,
                }
            ),
            InstanceSchema(
                {
                    "DATABASE_NAME": "my_db",
                    "SCHEMA_NAME": "my_schema",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 1,
                    "DATABASE_RETENTION_TIME": 90,
                    "COMMENT": None,
                }
            ),
            "ALTER SCHEMA MY_SCHEMA SET DATA_RETENTION_TIME_IN_DAYS = 1;",
        ),
        (  # data retention time
            InstanceSchema(
                {
                    "DATABASE_NAME": "my_db",
                    "SCHEMA_NAME": "my_schema",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 90,
                    "DATABASE_RETENTION_TIME": 90,
                    "COMMENT": None,
                }
            ),
            InstanceSchema(
                {
                    "DATABASE_NAME": "my_db",
                    "SCHEMA_NAME": "my_schema",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 90,
                    "DATABASE_RETENTION_TIME": 1,
                    "COMMENT": None,
                }
            ),
            "ALTER SCHEMA MY_SCHEMA SET DATA_RETENTION_TIME_IN_DAYS = 90;",
        ),
        (  # data retention time
            InstanceSchema(
                {
                    "DATABASE_NAME": "my_db",
                    "SCHEMA_NAME": "my_schema",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 1,
                    "DATABASE_RETENTION_TIME": 90,
                    "COMMENT": None,
                }
            ),
            InstanceSchema(
                {
                    "DATABASE_NAME": "my_db",
                    "SCHEMA_NAME": "my_schema",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 1,
                    "DATABASE_RETENTION_TIME": 90,
                    "COMMENT": None,
                }
            ),
            "",
        ),
        # (  # enable managed access
        #     InstanceSchema(
        #         {
        #             "DATABASE_NAME": "my_db",
        #             "SCHEMA_NAME": "my_schema",
        #             "IS_MANAGED_ACCESS": "NO",
        #             "IS_TRANSIENT": "NO",
        #             "RETENTION_TIME": 1,
        #             "COMMENT": None,
        #         }
        #     ),
        #     InstanceSchema(
        #         {
        #             "DATABASE_NAME": "my_db",
        #             "SCHEMA_NAME": "my_schema",
        #             "IS_MANAGED_ACCESS": "YES",
        #             "IS_TRANSIENT": "NO",
        #             "RETENTION_TIME": 1,
        #             "COMMENT": None,
        #         }
        #     ),
        #     "ALTER SCHEMA MY_SCHEMA ENABLE MANAGED ACCESS;",
        # ),
        # (  # disable managed access
        #     InstanceSchema(
        #         {
        #             "DATABASE_NAME": "my_db",
        #             "SCHEMA_NAME": "my_schema",
        #             "IS_MANAGED_ACCESS": "YES",
        #             "IS_TRANSIENT": "NO",
        #             "RETENTION_TIME": 1,
        #             "COMMENT": None,
        #         }
        #     ),
        #     InstanceSchema(
        #         {
        #             "DATABASE_NAME": "my_db",
        #             "SCHEMA_NAME": "my_schema",
        #             "IS_MANAGED_ACCESS": "NO",
        #             "IS_TRANSIENT": "NO",
        #             "RETENTION_TIME": 1,
        #             "COMMENT": None,
        #         }
        #     ),
        #     "ALTER SCHEMA MY_SCHEMA DISABLE MANAGED ACCESS;",
        # ),
    ],
)
def test_schema_generate_alter_statement(
    current_instance: InstanceSchema, desired_instance: InstanceSchema, expected: str
):
    result = oae.SchemaAction._generate_alter_statement(
        current_instance, desired_instance
    )
    assert result == expected


@pytest.mark.parametrize(
    "object_name, schema_name, object_type, action, current_instance, desired_instance, expected_statement",
    [
        (  # change increment
            "MYSCHEMA",
            "MYSCHEMA",
            DbObjectType.SCHEMA,
            DbActionType.ALTER,
            InstanceSchema(
                {
                    "DATABASE_NAME": "my_db",
                    "SCHEMA_NAME": "my_schema",
                    "IS_MANAGED_ACCESS": "NO",
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 1,
                    "DATABASE_RETENTION_TIME": 1,
                    "COMMENT": None,
                }
            ),
            InstanceSchema(
                {
                    "DATABASE_NAME": "my_db",
                    "SCHEMA_NAME": "my_schema",
                    "IS_MANAGED_ACCESS": "YES",  # property is currently ignored
                    "IS_TRANSIENT": "NO",
                    "RETENTION_TIME": 90,
                    "DATABASE_RETENTION_TIME": 1,
                    "COMMENT": "hello",
                }
            ),
            "ALTER SCHEMA MY_SCHEMA SET COMMENT = 'hello'; ALTER SCHEMA MY_SCHEMA SET DATA_RETENTION_TIME_IN_DAYS = 90;",
        )
    ],
)
def test_DbObjectAction_statement_schema_alter(
    object_name,
    schema_name,
    object_type,
    action,
    current_instance,
    desired_instance,
    expected_statement,
):
    # arrange
    object_action = oae.DbObjectAction.factory(
        schema_name,
        object_name,
        object_type,
        action,
        current_instance=current_instance,
        desired_instance=desired_instance,
    )

    # act
    statement = object_action._generate_statement()

    # assert
    assert statement.lower() == expected_statement.lower()


# endregion schema alter


# region view alter


@pytest.mark.parametrize(
    "current_instance, desired_instance, expected",
    [
        (  # current == desired (ignores differences in comments) and returns empty alter statement when view_definitions are the same (ignores whitespaces and case)
            mio.InstanceView(
                {
                    "DATABASE_NAME": "TWZ_TARGET",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "VIEW1",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "VIEW_DEFINITION": "CREATE OR REPLACE VIEW VIEWS.VIEW1 AS SELECT 1 I;",
                    "IS_SECURE": "NO",
                    "COMMENT": None,
                    "COLUMN_DETAILS": [{"COLUMN_NAME":"ID","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}],
                }
            ),
            mio.InstanceView(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "VIEW1",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "VIEW_DEFINITION": "CREATE OR REPLACE VIEW VIEWS.VIEW1 AS SELECT 1 I;",
                    "IS_SECURE": "NO",
                    "COMMENT": None,
                    "COLUMN_DETAILS": [{"COLUMN_NAME":"ID","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}],
                }
            ),
            "",
        ),
        (  # masking policy was applied before deployment
            mio.InstanceView(
                {
                    "APPLIED_POLICIES_LEGACY": [
                        {
                            "POLICY_DB": "TWZ_TARGET",
                            "POLICY_SCHEMA": "POLICIES",
                            "POLICY_NAME": "MP1",
                            "POLICY_KIND": "MASKING_POLICY",
                            "REF_DATABASE_NAME": "TWZ_TARGET",
                            "REF_SCHEMA_NAME": "VIEWS",
                            "REF_ENTITY_NAME": "VIEW1",
                            "REF_ENTITY_DOMAIN": "VIEW",
                            "REF_COLUMN_NAME": "I",
                            "REF_ARG_COLUMN_NAMES": None,
                        }
                    ],
                    "DATABASE_NAME": "TWZ_TARGET",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "VIEW1",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "VIEW_DEFINITION": "CREATE OR REPLACE VIEW VIEWS.VIEW1 AS SELECT 1 I;",
                    "IS_SECURE": "NO",
                    "COMMENT": None,
                    "COLUMN_DETAILS": [{"COLUMN_NAME":"I","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}],
                }
            ),
            mio.InstanceView(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "VIEW1",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "VIEW_DEFINITION": "CREATE OR REPLACE VIEW VIEWS.VIEW1 AS SELECT 1 I;",
                    "IS_SECURE": "NO",
                    "COMMENT": None,
                    "COLUMN_DETAILS": [{"COLUMN_NAME":"I","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}],
                }
            ),
            'CREATE OR REPLACE VIEW VIEWS.VIEW1 COPY GRANTS  AS SELECT 1 I; ALTER VIEW VIEWS.VIEW1 ALTER COLUMN I SET MASKING POLICY "TWZ_TARGET"."POLICIES"."MP1";',
        ),
        (  # masking policy on two columns was applied before deployment
            mio.InstanceView(
                {
                    "APPLIED_POLICIES_LEGACY": [
                        {
                            "POLICY_DB": "TWZ_TARGET",
                            "POLICY_SCHEMA": "POLICIES",
                            "POLICY_NAME": "MP1",
                            "POLICY_KIND": "MASKING_POLICY",
                            "REF_DATABASE_NAME": "TWZ_TARGET",
                            "REF_SCHEMA_NAME": "VIEWS",
                            "REF_ENTITY_NAME": "VIEW1",
                            "REF_ENTITY_DOMAIN": "VIEW",
                            "REF_COLUMN_NAME": "I",
                            "REF_ARG_COLUMN_NAMES": None,
                        },
                        {
                            "POLICY_DB": "TWZ_TARGET",
                            "POLICY_SCHEMA": "POLICIES",
                            "POLICY_NAME": "MP1",
                            "POLICY_KIND": "MASKING_POLICY",
                            "REF_DATABASE_NAME": "TWZ_TARGET",
                            "REF_SCHEMA_NAME": "VIEWS",
                            "REF_ENTITY_NAME": "VIEW1",
                            "REF_ENTITY_DOMAIN": "VIEW",
                            "REF_COLUMN_NAME": "J",
                            "REF_ARG_COLUMN_NAMES": None,
                        },
                    ],
                    "DATABASE_NAME": "TWZ_TARGET",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "VIEW1",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "VIEW_DEFINITION": "CREATE OR REPLACE VIEW VIEWS.VIEW1 AS SELECT 1 I, 2 J;",
                    "IS_SECURE": "NO",
                    "COMMENT": None,
                    "COLUMN_DETAILS": [{"COLUMN_NAME":"I","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}, {"COLUMN_NAME":"J","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":2,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}],
                }
            ),
            mio.InstanceView(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "VIEW1",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "VIEW_DEFINITION": "CREATE OR REPLACE VIEW VIEWS.VIEW1 AS SELECT 1 I, 2 J;",
                    "IS_SECURE": "NO",
                    "COMMENT": None,
                    "COLUMN_DETAILS": [{"COLUMN_NAME":"I","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}, {"COLUMN_NAME":"J","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":2,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}],
                }
            ),
            'CREATE OR REPLACE VIEW VIEWS.VIEW1 COPY GRANTS  AS SELECT 1 I, 2 J; ALTER VIEW VIEWS.VIEW1 ALTER COLUMN I SET MASKING POLICY "TWZ_TARGET"."POLICIES"."MP1"; ALTER VIEW VIEWS.VIEW1 ALTER COLUMN J SET MASKING POLICY "TWZ_TARGET"."POLICIES"."MP1";',
        ),
        (  # row access policy was applied before deployment
            mio.InstanceView(
                {
                    "APPLIED_POLICIES_LEGACY": [
                        {
                            "POLICY_DB": "TWZ_TARGET",
                            "POLICY_SCHEMA": "POLICIES",
                            "POLICY_NAME": "RAP1",
                            "POLICY_KIND": "ROW_ACCESS_POLICY",
                            "REF_DATABASE_NAME": "TWZ_TARGET",
                            "REF_SCHEMA_NAME": "VIEWS",
                            "REF_ENTITY_NAME": "VIEW6",
                            "REF_ENTITY_DOMAIN": "VIEW",
                            "REF_COLUMN_NAME": None,
                            "REF_ARG_COLUMN_NAMES": '[ "I" ]',
                        }
                    ],
                    "DATABASE_NAME": "TWZ_TARGET",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "VIEW1",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "VIEW_DEFINITION": "CREATE OR REPLACE VIEW VIEWS.VIEW1 AS SELECT 1 I;",
                    "IS_SECURE": "NO",
                    "COMMENT": None,
                    "COLUMN_DETAILS": [{"COLUMN_NAME":"I","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}],
                }
            ),
            mio.InstanceView(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "VIEW1",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "VIEW_DEFINITION": "CREATE OR REPLACE VIEW VIEWS.VIEW1 AS SELECT 1 I;",
                    "IS_SECURE": "NO",
                    "COMMENT": None,
                    "COLUMN_DETAILS": [{"COLUMN_NAME":"I","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}],
                }
            ),
            'CREATE OR REPLACE VIEW VIEWS.VIEW1 COPY GRANTS  AS SELECT 1 I; ALTER VIEW VIEWS.VIEW1 ADD ROW ACCESS POLICY "TWZ_TARGET"."POLICIES"."RAP1" ON (I);',
        ),
        (  # row access policy on two columns was applied before deployment
            mio.InstanceView(
                {
                    "APPLIED_POLICIES_LEGACY": [
                        {
                            "POLICY_DB": "TWZ_TARGET",
                            "POLICY_SCHEMA": "POLICIES",
                            "POLICY_NAME": "RAP1",
                            "POLICY_KIND": "ROW_ACCESS_POLICY",
                            "REF_DATABASE_NAME": "TWZ_TARGET",
                            "REF_SCHEMA_NAME": "VIEWS",
                            "REF_ENTITY_NAME": "VIEW6",
                            "REF_ENTITY_DOMAIN": "VIEW",
                            "REF_COLUMN_NAME": None,
                            "REF_ARG_COLUMN_NAMES": '[ "I", "J" ]',
                        }
                    ],
                    "DATABASE_NAME": "TWZ_TARGET",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "VIEW1",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "VIEW_DEFINITION": "CREATE OR REPLACE VIEW VIEWS.VIEW1 AS SELECT 1 I, 2 J;",
                    "IS_SECURE": "NO",
                    "COMMENT": None,
                    "COLUMN_DETAILS": [{"COLUMN_NAME":"I","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}, {"COLUMN_NAME":"J","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":2,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}],
                }
            ),
            mio.InstanceView(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "VIEW1",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "VIEW_DEFINITION": "CREATE OR REPLACE VIEW VIEWS.VIEW1 AS SELECT 1 I, 2 J;",
                    "IS_SECURE": "NO",
                    "COMMENT": None,
                    "COLUMN_DETAILS": [{"COLUMN_NAME":"I","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}, {"COLUMN_NAME":"J","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":2,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}],
                }
            ),
            'CREATE OR REPLACE VIEW VIEWS.VIEW1 COPY GRANTS  AS SELECT 1 I, 2 J; ALTER VIEW VIEWS.VIEW1 ADD ROW ACCESS POLICY "TWZ_TARGET"."POLICIES"."RAP1" ON (I,J);',
        ),
    ],
)
def test_view_generate_alter_statement(
    current_instance: InstanceView, desired_instance: InstanceView, expected: str
):
    result = oae.ViewAction._generate_alter_statement(
        current_instance, desired_instance
    )
    assert result == expected


@pytest.mark.parametrize(
    "current_instance, desired_instance",
    [
        (  # masking policy was applied before deployment on column J, after deployment column is named I
            mio.InstanceView(
                {
                    "APPLIED_POLICIES_LEGACY": [
                        {
                            "POLICY_DB": "TWZ_TARGET",
                            "POLICY_SCHEMA": "POLICIES",
                            "POLICY_NAME": "MP1",
                            "POLICY_KIND": "MASKING_POLICY",
                            "REF_DATABASE_NAME": "TWZ_TARGET",
                            "REF_SCHEMA_NAME": "VIEWS",
                            "REF_ENTITY_NAME": "VIEW1",
                            "REF_ENTITY_DOMAIN": "VIEW",
                            "REF_COLUMN_NAME": "J",
                            "REF_ARG_COLUMN_NAMES": None,
                        }
                    ],
                    "DATABASE_NAME": "TWZ_TARGET",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "VIEW1",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "VIEW_DEFINITION": "CREATE OR REPLACE VIEW VIEWS.VIEW1 AS SELECT 1 J;",
                    "IS_SECURE": "NO",
                    "COMMENT": None,
                    "COLUMN_DETAILS": [{"COLUMN_NAME":"J","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}],
                }
            ),
            mio.InstanceView(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "VIEW1",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "VIEW_DEFINITION": "CREATE OR REPLACE VIEW VIEWS.VIEW1 AS SELECT 1 I;",
                    "IS_SECURE": "NO",
                    "COMMENT": None,
                    "COLUMN_DETAILS": [{"COLUMN_NAME":"I","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}],
                }
            ),
        ),
        (  # row access policy was applied before deployment on column J, after deployment column is named I
            mio.InstanceView(
                {
                    "APPLIED_POLICIES_LEGACY": [
                        {
                            "POLICY_DB": "TWZ_TARGET",
                            "POLICY_SCHEMA": "POLICIES",
                            "POLICY_NAME": "RAP1",
                            "POLICY_KIND": "ROW_ACCESS_POLICY",
                            "REF_DATABASE_NAME": "TWZ_TARGET",
                            "REF_SCHEMA_NAME": "VIEWS",
                            "REF_ENTITY_NAME": "VIEW6",
                            "REF_ENTITY_DOMAIN": "VIEW",
                            "REF_COLUMN_NAME": None,
                            "REF_ARG_COLUMN_NAMES": '[ "J" ]',
                        }
                    ],
                    "DATABASE_NAME": "TWZ_TARGET",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "VIEW1",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "VIEW_DEFINITION": "CREATE OR REPLACE VIEW VIEWS.VIEW1 AS SELECT 1 J;",
                    "IS_SECURE": "NO",
                    "COMMENT": None,
                    "COLUMN_DETAILS": [{"COLUMN_NAME":"J","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}],
                }
            ),
            mio.InstanceView(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "VIEW1",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "VIEW_DEFINITION": "CREATE OR REPLACE VIEW VIEWS.VIEW1 AS SELECT 1 I;",
                    "IS_SECURE": "NO",
                    "COMMENT": None,
                    "COLUMN_DETAILS": [{"COLUMN_NAME":"I","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}],
                }
            ),
        ),
    ],
)
def test_view_generate_alter_statement_error(
    current_instance: InstanceView, desired_instance: InstanceView
):
    with pytest.raises(ValueError):
        __ = oae.ViewAction._generate_alter_statement(
            current_instance, desired_instance
        )


@pytest.mark.parametrize(
    "object_name, schema_name, object_type, action, current_instance, desired_instance, expected_statement",
    [
        (
            "VIEW1",
            "VIEWS",
            DbObjectType.VIEW,
            DbActionType.ALTER,
            mio.InstanceView(
                {
                    "DATABASE_NAME": "TWZ_TARGET",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "VIEW1",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "VIEW_DEFINITION": "CREATE OR REPLACE VIEW VIEWS.VIEW1 AS SELECT 1 I;",
                    "IS_SECURE": "NO",
                    "COMMENT": None,
                    "COLUMN_DETAILS": [{"COLUMN_NAME":"ID","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}],
                }
            ),
            mio.InstanceView(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "VIEWS",
                    "OBJECT_NAME": "VIEW1",
                    "TABLE_TYPE": "VIEW",
                    "CLUSTERING_KEY": None,
                    "VIEW_DEFINITION": "CREATE OR REPLACE VIEW VIEWS.VIEW1 AS SELECT 2 I;",
                    "IS_SECURE": "NO",
                    "COMMENT": None,
                    "COLUMN_DETAILS": [{"COLUMN_NAME":"ID","DATABASE_NAME":"TWZ_META","DATA_TYPE":"NUMBER","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","NUMERIC_PRECISION":38,"NUMERIC_PRECISION_RADIX":10,"NUMERIC_SCALE":0,"ORDINAL_POSITION":1,"TABLE_NAME":"VIEW1","TABLE_SCHEMA":"VIEWS"}],
                }
            ),
            "CREATE OR REPLACE VIEW VIEWS.VIEW1 COPY GRANTS  AS SELECT 2 I;",
        )
    ],
)
def test_DbObjectAction_statement_view_alter(
    object_name,
    schema_name,
    object_type,
    action,
    current_instance,
    desired_instance,
    expected_statement,
):
    # arrange
    object_action = oae.DbObjectAction.factory(
        schema_name,
        object_name,
        object_type,
        action,
        current_instance=current_instance,
        desired_instance=desired_instance,
    )

    # act
    statement = object_action._generate_statement()

    # assert
    assert statement.lower() == expected_statement.lower()

# endregion view alter


# region pipe alter


@pytest.mark.parametrize(
    "current_instance, desired_instance, expected",
    [
        (  # current == desired (no changes required)
            InstancePipe(
                {
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
            ),
            InstancePipe(
                {
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
            ),
            "",
        ),
        (  # change comment from null
            InstancePipe(
                {
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
            ),
            InstancePipe(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "MISC",
                    "OBJECT_NAME": "MYPIPE",
                    "DEFINITION": "COPY INTO DATA.TABLE1 FROM @MISC.MY_EXTERNAL_STAGE",
                    "IS_AUTOINGEST_ENABLED": "NO",
                    "NOTIFICATION_CHANNEL_NAME": None,
                    "COMMENT": "test",
                    "PATTERN": None,
                    "integration": "MY_NOTIFICATION_INTEGRATION",
                    "execution_state": "RUNNING",
                }
            ),
            "ALTER PIPE MISC.MYPIPE SET COMMENT = 'test';",
        ),
        (  # change comment from old value
            InstancePipe(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "MISC",
                    "OBJECT_NAME": "MYPIPE",
                    "DEFINITION": "COPY INTO DATA.TABLE1 FROM @MISC.MY_EXTERNAL_STAGE",
                    "IS_AUTOINGEST_ENABLED": "NO",
                    "NOTIFICATION_CHANNEL_NAME": None,
                    "COMMENT": "old",
                    "PATTERN": None,
                    "integration": "MY_NOTIFICATION_INTEGRATION",
                    "execution_state": "RUNNING",
                }
            ),
            InstancePipe(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "MISC",
                    "OBJECT_NAME": "MYPIPE",
                    "DEFINITION": "COPY INTO DATA.TABLE1 FROM @MISC.MY_EXTERNAL_STAGE",
                    "IS_AUTOINGEST_ENABLED": "NO",
                    "NOTIFICATION_CHANNEL_NAME": None,
                    "COMMENT": "new",
                    "PATTERN": None,
                    "integration": "MY_NOTIFICATION_INTEGRATION",
                    "execution_state": "RUNNING",
                }
            ),
            "ALTER PIPE MISC.MYPIPE SET COMMENT = 'new';",
        ),
        (  # unset comment
            InstancePipe(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "MISC",
                    "OBJECT_NAME": "MYPIPE",
                    "DEFINITION": "COPY INTO DATA.TABLE1 FROM @MISC.MY_EXTERNAL_STAGE",
                    "IS_AUTOINGEST_ENABLED": "NO",
                    "NOTIFICATION_CHANNEL_NAME": None,
                    "COMMENT": "test",
                    "PATTERN": None,
                    "integration": "MY_NOTIFICATION_INTEGRATION",
                    "execution_state": "RUNNING",
                }
            ),
            InstancePipe(
                {
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
            ),
            "ALTER PIPE MISC.MYPIPE UNSET COMMENT;",
        ),
        (  # change defintion
            InstancePipe(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "MISC",
                    "OBJECT_NAME": "MYPIPE",
                    "DEFINITION": "COPY INTO DATA.TABLE1 FROM @MISC.MY_EXTERNAL_STAGE",
                    "IS_AUTOINGEST_ENABLED": "NO",
                    "NOTIFICATION_CHANNEL_NAME": None,
                    "COMMENT": "alt",
                    "PATTERN": None,
                    "integration": "MY_NOTIFICATION_INTEGRATION",
                    "execution_state": "RUNNING",
                }
            ),
            InstancePipe(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "MISC",
                    "OBJECT_NAME": "MYPIPE",
                    "DEFINITION": "COPY INTO DATA.TABLE2 FROM @MISC.MY_EXTERNAL_STAGE",
                    "IS_AUTOINGEST_ENABLED": "NO",
                    "NOTIFICATION_CHANNEL_NAME": None,
                    "COMMENT": "neu",
                    "PATTERN": None,
                    "integration": "MY_NOTIFICATION_INTEGRATION",
                    "execution_state": "RUNNING",
                }
            ),
            "CREATE OR REPLACE PIPE ...;",
        ),
        (  # change defintion, execution paused
            InstancePipe(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "MISC",
                    "OBJECT_NAME": "MYPIPE",
                    "DEFINITION": "COPY INTO DATA.TABLE1 FROM @MISC.MY_EXTERNAL_STAGE",
                    "IS_AUTOINGEST_ENABLED": "NO",
                    "NOTIFICATION_CHANNEL_NAME": None,
                    "COMMENT": "alt",
                    "PATTERN": None,
                    "integration": "MY_NOTIFICATION_INTEGRATION",
                    "execution_state": "PAUSED",
                }
            ),
            InstancePipe(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "MISC",
                    "OBJECT_NAME": "MYPIPE",
                    "DEFINITION": "COPY INTO DATA.TABLE2 FROM @MISC.MY_EXTERNAL_STAGE",
                    "IS_AUTOINGEST_ENABLED": "NO",
                    "NOTIFICATION_CHANNEL_NAME": None,
                    "COMMENT": "neu",
                    "PATTERN": None,
                    "integration": "MY_NOTIFICATION_INTEGRATION",
                    "execution_state": "RUNNING",
                }
            ),
            "CREATE OR REPLACE PIPE ...; ALTER PIPE MISC.MYPIPE SET PIPE_EXECUTION_PAUSED = TRUE;",
        ),
    ],
)
def test_pipe_generate_alter_statement(
    current_instance: InstancePipe, desired_instance: InstancePipe, expected: str
):
    result = oae.PipeAction._generate_alter_statement(
        current_instance, desired_instance, file_content="CREATE PIPE ...;"
    )
    assert result == expected


@pytest.mark.parametrize(
    "object_name, schema_name, object_type, action, current_instance, desired_instance, file_content, expected_statement",
    [
        (  # change definition
            "MYPIPE",
            "MISC",
            DbObjectType.PIPE,
            DbActionType.ALTER,
            InstancePipe(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "MISC",
                    "OBJECT_NAME": "MYPIPE",
                    "DEFINITION": "COPY INTO DATA.TABLE1 FROM @MISC.MY_EXTERNAL_STAGE",
                    "IS_AUTOINGEST_ENABLED": "NO",
                    "NOTIFICATION_CHANNEL_NAME": None,
                    "COMMENT": "old",
                    "PATTERN": None,
                    "integration": "MY_NOTIFICATION_INTEGRATION",
                    "execution_state": "PAUSED",
                }
            ),
            InstancePipe(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "MISC",
                    "OBJECT_NAME": "MYPIPE",
                    "DEFINITION": "COPY INTO DATA.TABLE2 FROM @MISC.MY_EXTERNAL_STAGE",
                    "IS_AUTOINGEST_ENABLED": "NO",
                    "NOTIFICATION_CHANNEL_NAME": None,
                    "COMMENT": "new",
                    "PATTERN": None,
                    "integration": "MY_NOTIFICATION_INTEGRATION",
                    "execution_state": "RUNNING",
                }
            ),
            "CREATE PIPE MISC.MYPIPE AUTO_INGEST = FALSE AS COPY INTO DATA.TABLE2 FROM @MISC.MY_EXTERNAL_STAGE FILE_FORMAT = (format_name = MISC.MY_CSV_FORMAT);",
            "CREATE OR REPLACE PIPE MISC.MYPIPE AUTO_INGEST = FALSE AS COPY INTO DATA.TABLE2 FROM @MISC.MY_EXTERNAL_STAGE FILE_FORMAT = (format_name = MISC.MY_CSV_FORMAT); ALTER PIPE MISC.MYPIPE SET PIPE_EXECUTION_PAUSED = TRUE;",
        )
    ],
)
def test_DbObjectAction_statement_pipe_alter(
    object_name,
    schema_name,
    object_type,
    action,
    current_instance,
    desired_instance,
    file_content,
    expected_statement,
):
    # arrange
    object_action = oae.DbObjectAction.factory(
        schema_name,
        object_name,
        object_type,
        action,
        current_instance=current_instance,
        desired_instance=desired_instance,
        file_content=file_content,
    )

    # act
    statement = object_action._generate_statement()

    # assert
    assert statement.lower() == expected_statement.lower()


# endregion pipe alter


# region stage alter


@pytest.mark.parametrize(
    "current_instance, desired_instance, expected",
    [
        (  # current == desired (no changes required)
            InstanceStage(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "MISC",
                    "name": "MY_EXTERNAL_STAGE",
                    "has_credentials": "N",
                    "has_encryption_key": "N",
                    "region": "eastasia",
                    "type": "EXTERNAL",
                    "url": "azure://example.blob.core.windows.net/test",
                    "comment": None,
                    "notification_channel": None,
                    "storage_integration": "MY_STORAGE_INTEGRATION",
                    "cloud": "AZURE",
                    "STAGE_FILE_FORMAT": {},
                    "STAGE_COPY_OPTIONS": {},
                    "STAGE_LOCATION": {
                        "URL": "azure://example.blob.core.windows.net/test"
                    },
                    "STAGE_INTEGRATION": {
                        "STORAGE_INTEGRATION": "MY_STORAGE_INTEGRATION"
                    },
                    "DIRECTORY": {},
                }
            ),
            InstanceStage(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "MISC",
                    "name": "MY_EXTERNAL_STAGE",
                    "has_credentials": "N",
                    "has_encryption_key": "N",
                    "region": "eastasia",
                    "type": "EXTERNAL",
                    "url": "azure://example.blob.core.windows.net/test",
                    "comment": None,
                    "notification_channel": None,
                    "storage_integration": "MY_STORAGE_INTEGRATION",
                    "cloud": "AZURE",
                    "STAGE_FILE_FORMAT": {},
                    "STAGE_COPY_OPTIONS": {},
                    "STAGE_LOCATION": {
                        "URL": "azure://example.blob.core.windows.net/test"
                    },
                    "STAGE_INTEGRATION": {
                        "STORAGE_INTEGRATION": "MY_STORAGE_INTEGRATION"
                    },
                    "DIRECTORY": {},
                }
            ),
            "",
        ),
        (  # change comment from null
            InstanceStage(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "MISC",
                    "name": "MY_EXTERNAL_STAGE",
                    "has_credentials": "N",
                    "has_encryption_key": "N",
                    "region": "eastasia",
                    "type": "EXTERNAL",
                    "url": "azure://example.blob.core.windows.net/test",
                    "comment": None,
                    "notification_channel": None,
                    "storage_integration": "MY_STORAGE_INTEGRATION",
                    "cloud": "AZURE",
                    "STAGE_FILE_FORMAT": {},
                    "STAGE_COPY_OPTIONS": {},
                    "STAGE_LOCATION": {
                        "URL": "azure://example.blob.core.windows.net/test"
                    },
                    "STAGE_INTEGRATION": {
                        "STORAGE_INTEGRATION": "MY_STORAGE_INTEGRATION"
                    },
                    "DIRECTORY": {},
                }
            ),
            InstanceStage(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "MISC",
                    "name": "MY_EXTERNAL_STAGE",
                    "has_credentials": "N",
                    "has_encryption_key": "N",
                    "region": "eastasia",
                    "type": "EXTERNAL",
                    "url": "azure://example.blob.core.windows.net/test",
                    "comment": "test",
                    "notification_channel": None,
                    "storage_integration": "MY_STORAGE_INTEGRATION",
                    "cloud": "AZURE",
                    "STAGE_FILE_FORMAT": {},
                    "STAGE_COPY_OPTIONS": {},
                    "STAGE_LOCATION": {
                        "URL": "azure://example.blob.core.windows.net/test"
                    },
                    "STAGE_INTEGRATION": {
                        "STORAGE_INTEGRATION": "MY_STORAGE_INTEGRATION"
                    },
                    "DIRECTORY": {},
                }
            ),
            "ALTER STAGE MISC.MY_EXTERNAL_STAGE SET COMMENT = 'test';",
        ),
        (  # change comment from old value
            InstanceStage(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "MISC",
                    "name": "MY_EXTERNAL_STAGE",
                    "has_credentials": "N",
                    "has_encryption_key": "N",
                    "region": "eastasia",
                    "type": "EXTERNAL",
                    "url": "azure://example.blob.core.windows.net/test",
                    "comment": "old",
                    "notification_channel": None,
                    "storage_integration": "MY_STORAGE_INTEGRATION",
                    "cloud": "AZURE",
                    "STAGE_FILE_FORMAT": {},
                    "STAGE_COPY_OPTIONS": {},
                    "STAGE_LOCATION": {
                        "URL": "azure://example.blob.core.windows.net/test"
                    },
                    "STAGE_INTEGRATION": {
                        "STORAGE_INTEGRATION": "MY_STORAGE_INTEGRATION"
                    },
                    "DIRECTORY": {},
                }
            ),
            InstanceStage(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "MISC",
                    "name": "MY_EXTERNAL_STAGE",
                    "has_credentials": "N",
                    "has_encryption_key": "N",
                    "region": "eastasia",
                    "type": "EXTERNAL",
                    "url": "azure://example.blob.core.windows.net/test",
                    "comment": "new",
                    "notification_channel": None,
                    "storage_integration": "MY_STORAGE_INTEGRATION",
                    "cloud": "AZURE",
                    "STAGE_FILE_FORMAT": {},
                    "STAGE_COPY_OPTIONS": {},
                    "STAGE_LOCATION": {
                        "URL": "azure://example.blob.core.windows.net/test"
                    },
                    "STAGE_INTEGRATION": {
                        "STORAGE_INTEGRATION": "MY_STORAGE_INTEGRATION"
                    },
                    "DIRECTORY": {},
                }
            ),
            "ALTER STAGE MISC.MY_EXTERNAL_STAGE SET COMMENT = 'new';",
        ),
        (  # unset comment
            InstanceStage(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "MISC",
                    "name": "MY_EXTERNAL_STAGE",
                    "has_credentials": "N",
                    "has_encryption_key": "N",
                    "region": "eastasia",
                    "type": "EXTERNAL",
                    "url": "azure://example.blob.core.windows.net/test",
                    "comment": "old",
                    "notification_channel": None,
                    "storage_integration": "MY_STORAGE_INTEGRATION",
                    "cloud": "AZURE",
                    "STAGE_FILE_FORMAT": {},
                    "STAGE_COPY_OPTIONS": {},
                    "STAGE_LOCATION": {
                        "URL": "azure://example.blob.core.windows.net/test"
                    },
                    "STAGE_INTEGRATION": {
                        "STORAGE_INTEGRATION": "MY_STORAGE_INTEGRATION"
                    },
                    "DIRECTORY": {},
                }
            ),
            InstanceStage(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "MISC",
                    "name": "MY_EXTERNAL_STAGE",
                    "has_credentials": "N",
                    "has_encryption_key": "N",
                    "region": "eastasia",
                    "type": "EXTERNAL",
                    "url": "azure://example.blob.core.windows.net/test",
                    "comment": None,
                    "notification_channel": None,
                    "storage_integration": "MY_STORAGE_INTEGRATION",
                    "cloud": "AZURE",
                    "STAGE_FILE_FORMAT": {},
                    "STAGE_COPY_OPTIONS": {},
                    "STAGE_LOCATION": {
                        "URL": "azure://example.blob.core.windows.net/test"
                    },
                    "STAGE_INTEGRATION": {
                        "STORAGE_INTEGRATION": "MY_STORAGE_INTEGRATION"
                    },
                    "DIRECTORY": {},
                }
            ),
            "ALTER STAGE MISC.MY_EXTERNAL_STAGE SET COMMENT = '';",
        ),
    ],
)
def test_stage_generate_alter_statement(
    current_instance: InstancePipe, desired_instance: InstancePipe, expected: str
):
    result = oae.StageAction._generate_alter_statement(
        current_instance, desired_instance
    )
    assert result == expected


@pytest.mark.parametrize(
    "object_name, schema_name, object_type, action, current_instance, desired_instance, expected_statement",
    [
        (  # change comment
            "MY_EXTERNAL_STAGE",
            "MISC",
            DbObjectType.STAGE,
            DbActionType.ALTER,
            InstanceStage(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "MISC",
                    "name": "MY_EXTERNAL_STAGE",
                    "has_credentials": "N",
                    "has_encryption_key": "N",
                    "region": "eastasia",
                    "type": "EXTERNAL",
                    "url": "azure://example.blob.core.windows.net/test",
                    "comment": "old",
                    "notification_channel": None,
                    "storage_integration": "MY_STORAGE_INTEGRATION",
                    "cloud": "AZURE",
                    "STAGE_FILE_FORMAT": {},
                    "STAGE_COPY_OPTIONS": {},
                    "STAGE_LOCATION": {
                        "URL": "azure://example.blob.core.windows.net/test"
                    },
                    "STAGE_INTEGRATION": {
                        "STORAGE_INTEGRATION": "MY_STORAGE_INTEGRATION"
                    },
                    "DIRECTORY": {},
                }
            ),
            InstanceStage(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "MISC",
                    "name": "MY_EXTERNAL_STAGE",
                    "has_credentials": "N",
                    "has_encryption_key": "N",
                    "region": "eastasia",
                    "type": "EXTERNAL",
                    "url": "azure://example.blob.core.windows.net/test",
                    "comment": "new",
                    "notification_channel": None,
                    "storage_integration": "MY_STORAGE_INTEGRATION",
                    "cloud": "AZURE",
                    "STAGE_FILE_FORMAT": {},
                    "STAGE_COPY_OPTIONS": {},
                    "STAGE_LOCATION": {
                        "URL": "azure://example.blob.core.windows.net/test"
                    },
                    "STAGE_INTEGRATION": {
                        "STORAGE_INTEGRATION": "MY_STORAGE_INTEGRATION"
                    },
                    "DIRECTORY": {},
                }
            ),
            "ALTER STAGE MISC.MY_EXTERNAL_STAGE SET COMMENT = 'new';",
        )
    ],
)
def test_DbObjectAction_statement_stage_alter(
    object_name,
    schema_name,
    object_type,
    action,
    current_instance,
    desired_instance,
    expected_statement,
):
    # arrange
    object_action = oae.DbObjectAction.factory(
        schema_name,
        object_name,
        object_type,
        action,
        current_instance=current_instance,
        desired_instance=desired_instance,
    )

    # act
    statement = object_action._generate_statement()

    # assert
    assert statement.lower() == expected_statement.lower()


# endregion stage alter


# region sequence alter


@pytest.mark.parametrize(
    "current_instance, desired_instance, expected",
    [
        (  # current == desired (no changes required)
            InstanceSequence(
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
            ),
            InstanceSequence(
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
            ),
            "",
        ),
        (  # change increment
            InstanceSequence(
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
            ),
            InstanceSequence(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "MISC",
                    "OBJECT_NAME": "MYSEQUENCE",
                    "DATA_TYPE": "NUMBER",
                    "NUMERIC_PRECISION": 38,
                    "NUMERIC_PRECISION_RADIX": 10,
                    "NUMERIC_SCALE": 0,
                    "START_VALUE": 1,
                    "INCREMENT": 10,
                    "COMMENT": None,
                }
            ),
            "ALTER SEQUENCE MISC.MYSEQUENCE SET INCREMENT 10;",
        ),
        (  # change comment from null
            InstanceSequence(
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
            ),
            InstanceSequence(
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
                    "COMMENT": "new comment",
                }
            ),
            "ALTER SEQUENCE MISC.MYSEQUENCE SET COMMENT = 'new comment';",
        ),
        (  # change comment from old value
            InstanceSequence(
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
                    "COMMENT": "old comment",
                }
            ),
            InstanceSequence(
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
                    "COMMENT": "new comment",
                }
            ),
            "ALTER SEQUENCE MISC.MYSEQUENCE SET COMMENT = 'new comment';",
        ),
        (  # unset comment
            InstanceSequence(
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
                    "COMMENT": "old comment",
                }
            ),
            InstanceSequence(
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
            ),
            "ALTER SEQUENCE MISC.MYSEQUENCE UNSET COMMENT;",
        ),
        (  # change comment and increment
            InstanceSequence(
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
                    "COMMENT": "old comment",
                }
            ),
            InstanceSequence(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "MISC",
                    "OBJECT_NAME": "MYSEQUENCE",
                    "DATA_TYPE": "NUMBER",
                    "NUMERIC_PRECISION": 38,
                    "NUMERIC_PRECISION_RADIX": 10,
                    "NUMERIC_SCALE": 0,
                    "START_VALUE": 1,
                    "INCREMENT": 10,
                    "COMMENT": "new comment",
                }
            ),
            "ALTER SEQUENCE MISC.MYSEQUENCE SET COMMENT = 'new comment'; ALTER SEQUENCE MISC.MYSEQUENCE SET INCREMENT 10;",
        ),
    ],
)
def test_sequence_generate_alter_statement(
    current_instance: InstanceSequence,
    desired_instance: InstanceSequence,
    expected: str,
):
    result = oae.SequenceAction._generate_alter_statement(
        current_instance, desired_instance
    )
    assert result == expected


@pytest.mark.parametrize(
    "object_name, schema_name, object_type, action, current_instance, desired_instance, expected_statement",
    [
        (  # change increment
            "MYSEQUENCE",
            "MISC",
            DbObjectType.SEQUENCE,
            DbActionType.ALTER,
            InstanceSequence(
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
            ),
            InstanceSequence(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "MISC",
                    "OBJECT_NAME": "MYSEQUENCE",
                    "DATA_TYPE": "NUMBER",
                    "NUMERIC_PRECISION": 38,
                    "NUMERIC_PRECISION_RADIX": 10,
                    "NUMERIC_SCALE": 0,
                    "START_VALUE": 1,
                    "INCREMENT": 10,
                    "COMMENT": None,
                }
            ),
            "ALTER SEQUENCE MISC.MYSEQUENCE SET INCREMENT 10;",
        )
    ],
)
def test_DbObjectAction_statement_sequence_alter(
    object_name,
    schema_name,
    object_type,
    action,
    current_instance,
    desired_instance,
    expected_statement,
):
    # arrange
    object_action = oae.DbObjectAction.factory(
        schema_name,
        object_name,
        object_type,
        action,
        current_instance=current_instance,
        desired_instance=desired_instance,
    )

    # act
    statement = object_action._generate_statement()

    # assert
    assert statement.lower() == expected_statement.lower()


# endregion sequence alter


# region stream alter
@pytest.mark.parametrize(
    "current_instance, desired_instance, expected",
    [
        (  # current == desired (no changes required)
            InstanceStream(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "MISC",
                    "name": "MYSTREAM",
                    "comment": "test",
                    "table_name": "S.TABLE",
                    "type": "DELTA",
                    "stale": True,
                    "mode": "APPEND_ONLY",
                }
            ),
            InstanceStream(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "MISC",
                    "name": "MYSTREAM",
                    "comment": "test",
                    "table_name": "S.TABLE",
                    "type": "DELTA",
                    "stale": True,
                    "mode": "APPEND_ONLY",
                }
            ),
            "",
        ),
        (  # change comment
            InstanceStream(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "MISC",
                    "name": "MYSTREAM",
                    "comment": "test",
                    "table_name": "S.TABLE",
                    "type": "DELTA",
                    "stale": True,
                    "mode": "APPEND_ONLY",
                }
            ),
            InstanceStream(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "MISC",
                    "name": "MYSTREAM",
                    "comment": "new comment",
                    "table_name": "S.TABLE",
                    "type": "DELTA",
                    "stale": True,
                    "mode": "APPEND_ONLY",
                }
            ),
            "ALTER STREAM MISC.MYSTREAM SET COMMENT = 'new comment';",
        ),
        (  # remove comment
            InstanceStream(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "MISC",
                    "name": "MYSTREAM",
                    "comment": "test",
                    "table_name": "S.TABLE",
                    "type": "DELTA",
                    "stale": True,
                    "mode": "APPEND_ONLY",
                }
            ),
            InstanceStream(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "MISC",
                    "name": "MYSTREAM",
                    "comment": None,
                    "table_name": "S.TABLE",
                    "type": "DELTA",
                    "stale": True,
                    "mode": "APPEND_ONLY",
                }
            ),
            "ALTER STREAM MISC.MYSTREAM UNSET COMMENT;",
        ),
    ],
)
def test_stream_generate_alter_statement(
    current_instance: InstanceStream, desired_instance: InstanceStream, expected: str
):
    result = oae.StreamAction._generate_alter_statement(
        current_instance, desired_instance
    )
    assert result == expected


@pytest.mark.parametrize(
    "object_name, schema_name, object_type, action, current_instance, desired_instance, expected_statement",
    [
        (  # change increment
            "MYSTREAM",
            "MISC",
            DbObjectType.STREAM,
            DbActionType.ALTER,
            InstanceStream(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "MISC",
                    "name": "MYSTREAM",
                    "comment": "test",
                    "table_name": "S.TABLE",
                    "type": "DELTA",
                    "stale": True,
                    "mode": "APPEND_ONLY",
                }
            ),
            InstanceStream(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "MISC",
                    "name": "MYSTREAM",
                    "comment": "new comment",
                    "table_name": "S.TABLE",
                    "type": "DELTA",
                    "stale": True,
                    "mode": "APPEND_ONLY",
                }
            ),
            "ALTER STREAM MISC.MYSTREAM SET COMMENT = 'new comment';",
        )
    ],
)
def test_DbObjectAction_statement_stream_alter(
    object_name,
    schema_name,
    object_type,
    action,
    current_instance,
    desired_instance,
    expected_statement,
):
    # arrange
    object_action = oae.DbObjectAction.factory(
        schema_name,
        object_name,
        object_type,
        action,
        current_instance=current_instance,
        desired_instance=desired_instance,
    )

    # act
    statement = object_action._generate_statement()

    # assert
    assert statement.lower() == expected_statement.lower()


# endregion stream


# region masking policy alter
@pytest.mark.parametrize(
    "current_instance, desired_instance, expected",
    [
        (  # current == desired (no changes required)
            InstanceMaskingPolicy(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "POLICIES",
                    "name": "MYMASKINGPOLICY",
                    "kind": "MASKING_POLICY",
                    "comment": "my comment",
                    "signature": "(N NUMBER)",
                    "return_type": "NUMBER(38,0)",
                    "body": "1 --dummy policy body",
                }
            ),
            InstanceMaskingPolicy(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "POLICIES",
                    "name": "MYMASKINGPOLICY",
                    "kind": "MASKING_POLICY",
                    "comment": "my comment",
                    "signature": "(N NUMBER)",
                    "return_type": "NUMBER(38,0)",
                    "body": "1 --dummy policy body",
                }
            ),
            "",
        ),
        (  # change comment
            InstanceMaskingPolicy(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "POLICIES",
                    "name": "MYMASKINGPOLICY",
                    "kind": "MASKING_POLICY",
                    "comment": "my comment",
                    "signature": "(N NUMBER)",
                    "return_type": "NUMBER(38,0)",
                    "body": "1 --dummy policy body",
                }
            ),
            InstanceMaskingPolicy(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "POLICIES",
                    "name": "MYMASKINGPOLICY",
                    "kind": "MASKING_POLICY",
                    "comment": "new comment",
                    "signature": "(N NUMBER)",
                    "return_type": "NUMBER(38,0)",
                    "body": "1 --dummy policy body",
                }
            ),
            "ALTER MASKING POLICY POLICIES.MYMASKINGPOLICY SET COMMENT = 'new comment';",
        ),
        (  # remove comment
            InstanceMaskingPolicy(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "POLICIES",
                    "name": "MYMASKINGPOLICY",
                    "kind": "MASKING_POLICY",
                    "comment": "my comment",
                    "signature": "(N NUMBER)",
                    "return_type": "NUMBER(38,0)",
                    "body": "1 --dummy policy body",
                }
            ),
            InstanceMaskingPolicy(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "POLICIES",
                    "name": "MYMASKINGPOLICY",
                    "kind": "MASKING_POLICY",
                    "comment": None,
                    "signature": "(N NUMBER)",
                    "return_type": "NUMBER(38,0)",
                    "body": "1 --dummy policy body",
                }
            ),
            "ALTER MASKING POLICY POLICIES.MYMASKINGPOLICY UNSET COMMENT;",
        ),
        (  # change body
            InstanceMaskingPolicy(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "POLICIES",
                    "name": "MYMASKINGPOLICY",
                    "kind": "MASKING_POLICY",
                    "comment": "my comment",
                    "signature": "(N NUMBER)",
                    "return_type": "NUMBER(38,0)",
                    "body": "1 /*dummy policy body*/",
                }
            ),
            InstanceMaskingPolicy(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "POLICIES",
                    "name": "MYMASKINGPOLICY",
                    "kind": "MASKING_POLICY",
                    "comment": "my comment",
                    "signature": "(N NUMBER)",
                    "return_type": "NUMBER(38,0)",
                    "body": "2 /*dummy policy body*/",
                }
            ),
            "ALTER MASKING POLICY POLICIES.MYMASKINGPOLICY SET BODY -> 2 /*dummy policy body*/;",
        ),
    ],
)
def test_maskingpolicy_generate_alter_statement(
    current_instance: InstanceMaskingPolicy,
    desired_instance: InstanceMaskingPolicy,
    expected: str,
):
    result = oae.MaskingPolicyAction._generate_alter_statement(
        current_instance, desired_instance
    )
    assert result == expected


@pytest.mark.parametrize(
    "object_name, schema_name, object_type, action, current_instance, desired_instance, expected_statement",
    [
        (  # change increment
            "MYMASKINGPOLICY",
            "POLICIES",
            DbObjectType.MASKINGPOLICY,
            DbActionType.ALTER,
            InstanceMaskingPolicy(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "POLICIES",
                    "name": "MYMASKINGPOLICY",
                    "kind": "MASKING_POLICY",
                    "comment": "my comment",
                    "signature": "(N NUMBER)",
                    "return_type": "NUMBER(38,0)",
                    "body": "1 --dummy policy body",
                }
            ),
            InstanceMaskingPolicy(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "POLICIES",
                    "name": "MYMASKINGPOLICY",
                    "kind": "MASKING_POLICY",
                    "comment": "new comment",
                    "signature": "(N NUMBER)",
                    "return_type": "NUMBER(38,0)",
                    "body": "1 --dummy policy body",
                }
            ),
            "ALTER MASKING POLICY POLICIES.MYMASKINGPOLICY SET COMMENT = 'new comment';",
        )
    ],
)
def test_DbObjectAction_statement_maskingpolicy_alter(
    object_name,
    schema_name,
    object_type,
    action,
    current_instance,
    desired_instance,
    expected_statement,
):
    # arrange
    object_action = oae.DbObjectAction.factory(
        schema_name,
        object_name,
        object_type,
        action,
        current_instance=current_instance,
        desired_instance=desired_instance,
    )

    # act
    statement = object_action._generate_statement()

    # assert
    assert statement.lower() == expected_statement.lower()


# endregion masking policy


# region row access policy alter
@pytest.mark.parametrize(
    "current_instance, desired_instance, expected",
    [
        (  # current == desired (no changes required)
            InstanceRowAccessPolicy(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "POLICIES",
                    "name": "MYROWACCESSPOLICY",
                    "kind": "ROW_ACCESS_POLICY",
                    "comment": "my comment",
                    "signature": "(N NUMBER)",
                    "return_type": "BOOLEAN",
                    "body": "TRUE /*dummy policy body*/",
                }
            ),
            InstanceRowAccessPolicy(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "POLICIES",
                    "name": "MYROWACCESSPOLICY",
                    "kind": "ROW_ACCESS_POLICY",
                    "comment": "my comment",
                    "signature": "(N NUMBER)",
                    "return_type": "BOOLEAN",
                    "body": "TRUE /*dummy policy body*/",
                }
            ),
            "",
        ),
        (  # change comment
            InstanceRowAccessPolicy(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "POLICIES",
                    "name": "MYROWACCESSPOLICY",
                    "kind": "ROW_ACCESS_POLICY",
                    "comment": "my comment",
                    "signature": "(N NUMBER)",
                    "return_type": "BOOLEAN",
                    "body": "TRUE /*dummy policy body*/",
                }
            ),
            InstanceRowAccessPolicy(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "POLICIES",
                    "name": "MYROWACCESSPOLICY",
                    "kind": "ROW_ACCESS_POLICY",
                    "comment": "new comment",
                    "signature": "(N NUMBER)",
                    "return_type": "BOOLEAN",
                    "body": "TRUE /*dummy policy body*/",
                }
            ),
            "ALTER ROW ACCESS POLICY POLICIES.MYROWACCESSPOLICY SET COMMENT = 'new comment';",
        ),
        (  # remove comment
            InstanceRowAccessPolicy(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "POLICIES",
                    "name": "MYROWACCESSPOLICY",
                    "kind": "ROW_ACCESS_POLICY",
                    "comment": "my comment",
                    "signature": "(N NUMBER)",
                    "return_type": "BOOLEAN",
                    "body": "TRUE /*dummy policy body*/",
                }
            ),
            InstanceRowAccessPolicy(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "POLICIES",
                    "name": "MYROWACCESSPOLICY",
                    "kind": "ROW_ACCESS_POLICY",
                    "comment": None,
                    "signature": "(N NUMBER)",
                    "return_type": "BOOLEAN",
                    "body": "TRUE /*dummy policy body*/",
                }
            ),
            "ALTER ROW ACCESS POLICY POLICIES.MYROWACCESSPOLICY UNSET COMMENT;",
        ),
        (  # change body
            InstanceRowAccessPolicy(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "POLICIES",
                    "name": "MYROWACCESSPOLICY",
                    "kind": "ROW_ACCESS_POLICY",
                    "comment": "my comment",
                    "signature": "(N NUMBER)",
                    "return_type": "BOOLEAN",
                    "body": "TRUE /*dummy policy body*/",
                }
            ),
            InstanceRowAccessPolicy(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "POLICIES",
                    "name": "MYROWACCESSPOLICY",
                    "kind": "ROW_ACCESS_POLICY",
                    "comment": "my comment",
                    "signature": "(N NUMBER)",
                    "return_type": "BOOLEAN",
                    "body": "FALSE /*dummy policy body*/",
                }
            ),
            "ALTER ROW ACCESS POLICY POLICIES.MYROWACCESSPOLICY SET BODY -> FALSE /*dummy policy body*/;",
        ),
    ],
)
def test_rowaccesspolicy_generate_alter_statement(
    current_instance: InstanceRowAccessPolicy,
    desired_instance: InstanceRowAccessPolicy,
    expected: str,
):
    result = oae.RowAccessPolicyAction._generate_alter_statement(
        current_instance, desired_instance
    )
    assert result == expected


@pytest.mark.parametrize(
    "object_name, schema_name, object_type, action, current_instance, desired_instance, expected_statement",
    [
        (  # change increment
            "MYROWACCESSPOLICY",
            "POLICIES",
            DbObjectType.ROWACCESSPOLICY,
            DbActionType.ALTER,
            InstanceRowAccessPolicy(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "POLICIES",
                    "name": "MYROWACCESSPOLICY",
                    "kind": "ROW_ACCESS_POLICY",
                    "comment": "my comment",
                    "signature": "(N NUMBER)",
                    "return_type": "BOOLEAN",
                    "body": "TRUE --dummy policy body",
                }
            ),
            InstanceRowAccessPolicy(
                {
                    "database_name": "TWZ_META",
                    "schema_name": "POLICIES",
                    "name": "MYROWACCESSPOLICY",
                    "kind": "ROW_ACCESS_POLICY",
                    "comment": "new comment",
                    "signature": "(N NUMBER)",
                    "return_type": "BOOLEAN",
                    "body": "TRUE --dummy policy body",
                }
            ),
            "ALTER ROW ACCESS POLICY POLICIES.MYROWACCESSPOLICY SET COMMENT = 'new comment';",
        )
    ],
)
def test_DbObjectAction_statement_rowaccesspolicy_alter(
    object_name,
    schema_name,
    object_type,
    action,
    current_instance,
    desired_instance,
    expected_statement,
):
    # arrange
    object_action = oae.DbObjectAction.factory(
        schema_name,
        object_name,
        object_type,
        action,
        current_instance=current_instance,
        desired_instance=desired_instance,
    )

    # act
    statement = object_action._generate_statement()

    # assert
    assert statement.lower() == expected_statement.lower()


# endregion row access policy


# region dynamic table alter
@pytest.mark.parametrize(
    "dynamic_table_action, expected",
    [
        (  # current == desired (no changes required)
            oae.DynamicTableAction(
                "DATA",
                "DYNAMICTABLE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
            ),
            "",
        ),
        (  # change query text
            oae.DynamicTableAction(
                "DATA",
                "DYNAMICTABLE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                )
            ),
                "CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
        ),
        (  # alter target_lag
            oae.DynamicTableAction(
                "DATA",
                "DYNAMICTABLE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "1 minutes",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                )
            ),
                "ALTER DYNAMIC TABLE DATA.DYNAMICTABLE1 SET TARGET_LAG = '1 minutes';",
        ),
        (  # alter warehouse
            oae.DynamicTableAction(
                "DATA",
                "DYNAMICTABLE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH_1",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                )
            ),
                "ALTER DYNAMIC TABLE DATA.DYNAMICTABLE1 SET WAREHOUSE = COMPUTE_WH_1;",
        ),
        (  # alter retention_time to the same value as set on schema_retention_time
            oae.DynamicTableAction(
                "DATA",
                "DYNAMICTABLE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 1,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                )
            ),
                "ALTER DYNAMIC TABLE DATA.DYNAMICTABLE1 UNSET DATA_RETENTION_TIME_IN_DAYS;",
        ),(  # alter retention_time
            oae.DynamicTableAction(
                "DATA",
                "DYNAMICTABLE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 2,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                )
            ),
                "ALTER DYNAMIC TABLE DATA.DYNAMICTABLE1 SET DATA_RETENTION_TIME_IN_DAYS = 2;",
        ),
        (  # remove comment
            oae.DynamicTableAction(
                "DATA",
                "DYNAMICTABLE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": None,
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                
            ),"ALTER DYNAMIC TABLE DATA.DYNAMICTABLE1 UNSET COMMENT;",
        ),
        (  # alter refresh_mode
            oae.DynamicTableAction(
                "DATA",
                "DYNAMICTABLE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": None,
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "AUTO",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                
            ),"CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
        ),
        (  # alter CLUSTERING_KEY
            oae.DynamicTableAction(
                "DATA",
                "DYNAMICTABLE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": '(COLUMN_1)',
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": None,
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": '(COLUMN_2)',
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": None,
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                
            ),"ALTER DYNAMIC TABLE DATA.DYNAMICTABLE1 CLUSTER BY (COLUMN_2);",
        ),
        (  # add CLUSTERING_KEY
            oae.DynamicTableAction(
                "DATA",
                "DYNAMICTABLE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": None,
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": '(COLUMN_1)',
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": None,
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                
            ),"ALTER DYNAMIC TABLE DATA.DYNAMICTABLE1 CLUSTER BY (COLUMN_1);",
        ),
        (  # drop CLUSTERING_KEY
            oae.DynamicTableAction(
                "DATA",
                "DYNAMICTABLE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": '(COLUMN_1)',
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": None,
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": None,
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                
            ),"ALTER DYNAMIC TABLE DATA.DYNAMICTABLE1 DROP CLUSTERING KEY;",
        ),
        (  # add tag
            oae.DynamicTableAction(
                "DATA",
                "DYNAMICTABLE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "tags" : {},
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "tags" : {"MY_TAG": "MY_TAG_VALUE"},
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
            ),
            "ALTER DYNAMIC TABLE DATA.DYNAMICTABLE1 SET TAG MY_TAG = 'MY_TAG_VALUE';",
        ), (  # remove tag
            oae.DynamicTableAction(
                "DATA",
                "DYNAMICTABLE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "tags" : {"MY_TAG": "MY_TAG_VALUE"},
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "tags" : {},
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
            ),
            "ALTER DYNAMIC TABLE DATA.DYNAMICTABLE1 UNSET TAG MY_TAG;",
        ),
    ],
)
def test_dynamictable_generate_alter_statement(
    dynamic_table_action: oae.DynamicTableAction, expected: str
):
    result = oae.DynamicTableAction._generate_alter_statement(dynamic_table_action)
    assert result == expected




# region dynamic table alter
@pytest.mark.parametrize(
    "object_name, schema_name, object_type, action, current_instance, desired_instance, expected_statement",
    [
        (
            "DYNAMICTABLE1",
            "DATA",
            DbObjectType.DYNAMICTABLE,
            DbActionType.ALTER,
            InstanceDynamicTable(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "DATA",
                    "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                    "OBJECT_NAME": "DYNAMICTABLE1",
                    "TABLE_TYPE": "BASE TABLE",
                    "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                    "CLUSTERING_KEY": None,
                    "RETENTION_TIME": 1,
                    "SCHEMA_RETENTION_TIME": 1,
                    "COMMENT": None,
                    "TARGET_LAG": "1 minutes",
                    "WAREHOUSE": "COMPUTE_WH_1",
                    "REFRESH_MODE": "AUTO",
                    "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                }
            ),
            InstanceDynamicTable(
                {
                    "DATABASE_NAME": "TWZ_META",
                    "SCHEMA_NAME": "DATA",
                    "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                    "OBJECT_NAME": "DYNAMICTABLE1",
                    "TABLE_TYPE": "BASE TABLE",
                    "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                    "CLUSTERING_KEY": None,
                    "RETENTION_TIME": 1,
                    "SCHEMA_RETENTION_TIME": 1,
                    "COMMENT": "TEST COMMENT",
                    "TARGET_LAG": "1 minutes",
                    "WAREHOUSE": "COMPUTE_WH_1",
                    "REFRESH_MODE": "AUTO",
                    "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                }
            ),
            "ALTER DYNAMIC TABLE DATA.DYNAMICTABLE1 SET COMMENT = 'TEST COMMENT';",
        )
    ],
)
def test_DbObjectAction_statement_dynamic_table_alter(
    object_name,
    schema_name,
    object_type,
    action,
    current_instance,
    desired_instance,
    expected_statement,
):
    # arrange
    object_action = oae.DbObjectAction.factory(
        schema_name,
        object_name,
        object_type,
        action,
        current_instance=current_instance,
        desired_instance=desired_instance,
    )

    # act
    statement = object_action._generate_statement()

    # assert
    assert statement.lower() == expected_statement.lower()


# endregion dynamic table alter

# region dynamic table column alter
@pytest.mark.parametrize(
    "dynamic_table_action, expected",
    [
        (  # alter Dynamic Table Column property (ORDINAL_POSITION) for which the Dynamic Table will be re-created
            oae.DynamicTableAction(
                "DATA",
                "DYNAMICTABLE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                )
            ),
                "CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
        ),(  # alter Dynamic Table Column property (DATA_TYPE) for which the Dynamic Table will be re-created
            oae.DynamicTableAction(
                "DATA",
                "DYNAMICTABLE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "NUMBER","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                )
            ),
                "CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
        ),(  # alter Dynamic Table Column property (IS_NULLABLE) for which the Dynamic Table will be re-created
            oae.DynamicTableAction(
                "DATA",
                "DYNAMICTABLE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "NO","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                )
            ),
                "CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
        ),
        (  # alter Dynamic Table Column property (COMMENT) for which the Dynamic Table will be altered
            oae.DynamicTableAction(
                "DATA",
                "DYNAMICTABLE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1", "COMMENT":"","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1", "COMMENT":"MY COMMENT","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                )
            ),
                 "ALTER DYNAMIC TABLE DATA.DYNAMICTABLE1 ALTER COLUMN_1 COMMENT 'MY COMMENT';",
        ),
        (  # alter Dynamic Table Column property (TAG) for which the Dynamic Table will be altered
            oae.DynamicTableAction(
                "DATA",
                "DYNAMICTABLE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 ...;",
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1", "COMMENT":"","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA", "tags" : {}  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                ),
                InstanceDynamicTable(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "DATA",
                        "OBJECT_TYPE": DbObjectType.DYNAMICTABLE,
                        "OBJECT_NAME": "DYNAMICTABLE1",
                        "TABLE_TYPE": "BASE TABLE",
                        "QUERY_TEXT": "SELECT COLUMN_1, COLUMN_2 FROM MISC.MYTABLE;",
                        "CLUSTERING_KEY": None,
                        "RETENTION_TIME": 0,
                        "SCHEMA_RETENTION_TIME": 1,
                        "COMMENT": "TEST COMMENT",
                        "TARGET_LAG": "2 hours",
                        "WAREHOUSE": "COMPUTE_WH",
                        "REFRESH_MODE": "INCREMENTAL",
                        "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_1", "COMMENT":"","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 1,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA", "tags" : {"MY_TAG": "MY_TAG_VALUE"}  },  {"CHARACTER_MAXIMUM_LENGTH": 16777216,"CHARACTER_OCTET_LENGTH": 16777216,"COLUMN_NAME": "COLUMN_2","DATABASE_NAME": "TWZ_META","DATA_TYPE": "TEXT","IS_IDENTITY": "NO","IS_NULLABLE": "YES","IS_SELF_REFERENCING": "NO","ORDINAL_POSITION": 2,"TABLE_NAME": "DYNAMICTABLE1","TABLE_SCHEMA": "DATA"  }],
                    }
                )
            ),
                 "ALTER DYNAMIC TABLE DATA.DYNAMICTABLE1 ALTER COLUMN COLUMN_1 SET TAG MY_TAG = 'MY_TAG_VALUE';",
        )
    ],
)
def test_dynamictable_generate_alter_column_statement(
    dynamic_table_action: oae.DynamicTableAction, expected: str
):
    dynamic_table_action.columns_to_alter = ['COLUMN_1', 'COLUMN_2']
    result = oae.DynamicTableAction._generate_alter_statement(dynamic_table_action)
    assert result == expected
# endregion dynamic table column alter

# region network rule alter
@pytest.mark.parametrize(
    "network_rule_action, expected",
    [
        (  # current == desired (no changes required)
            oae.NetworkRuleAction(
                "MISC",
                "MY_NETWORK_RULE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE NETWORK RULE MISC.MY_NETWORK_RULE1 ...;",
                InstanceNetworkRule(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "MISC",
                        "OBJECT_NAME": "MY_NETWORK_RULE1",
                        "TYPE": "IPV4",
                        "MODE": "INGRESS",
                        "VALUE_LIST": "('0.0.0.0')",
                        "COMMENT": "whitelist"
                        }
                ),
                InstanceNetworkRule(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "MISC",
                        "OBJECT_NAME": "MY_NETWORK_RULE1",
                        "TYPE": "IPV4",
                        "MODE": "INGRESS",
                        "VALUE_LIST": "('0.0.0.0')",
                        "COMMENT": "whitelist"
                    }
                ),
            ),
            "",
        ),
        (  # change type
            oae.NetworkRuleAction(
                "MISC",
                "MY_NETWORK_RULE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE NETWORK RULE MISC.MY_NETWORK_RULE1 ...;",
                InstanceNetworkRule(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "MISC",
                        "OBJECT_NAME": "MY_NETWORK_RULE1",
                        "TYPE": "IPV4",
                        "MODE": "INGRESS",
                        "VALUE_LIST": "('0.0.0.0')",
                        "COMMENT": "whitelist"
                        }
                ),
                InstanceNetworkRule(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "MISC",
                        "OBJECT_NAME": "MY_NETWORK_RULE1",
                        "TYPE": "AZURELINKID",
                        "MODE": "INGRESS",
                        "VALUE_LIST": "('0.0.0.0')",
                        "COMMENT": "whitelist"
                    }
                ),
            ),
            "CREATE OR REPLACE NETWORK RULE MISC.MY_NETWORK_RULE1 ...;",
        ),
        (  # change mode
            oae.NetworkRuleAction(
                "MISC",
                "MY_NETWORK_RULE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE NETWORK RULE MISC.MY_NETWORK_RULE1 ...;",
                InstanceNetworkRule(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "MISC",
                        "OBJECT_NAME": "MY_NETWORK_RULE1",
                        "TYPE": "IPV4",
                        "MODE": "INGRESS",
                        "VALUE_LIST": "('0.0.0.0')",
                        "COMMENT": "whitelist"
                        }
                ),
                InstanceNetworkRule(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "MISC",
                        "OBJECT_NAME": "MY_NETWORK_RULE1",
                        "TYPE": "IPV4",
                        "MODE": "EGRESS",
                        "VALUE_LIST": "('0.0.0.0')",
                        "COMMENT": "whitelist"
                    }
                ),
            ),
            "CREATE OR REPLACE NETWORK RULE MISC.MY_NETWORK_RULE1 ...;",
        ),
        (  # change value list
            oae.NetworkRuleAction(
                "MISC",
                "MY_NETWORK_RULE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE NETWORK RULE MISC.MY_NETWORK_RULE1 ...;",
                InstanceNetworkRule(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "MISC",
                        "OBJECT_NAME": "MY_NETWORK_RULE1",
                        "TYPE": "IPV4",
                        "MODE": "INGRESS",
                        "VALUE_LIST": "'0.0.0.0'",
                        "COMMENT": "whitelist"
                        }
                ),
                InstanceNetworkRule(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "MISC",
                        "OBJECT_NAME": "MY_NETWORK_RULE1",
                        "TYPE": "IPV4",
                        "MODE": "INGRESS",
                        "VALUE_LIST": "0.0.0.1",
                        "COMMENT": "whitelist"
                    }
                ),
            ),
            "ALTER NETWORK RULE MISC.MY_NETWORK_RULE1 SET VALUE_LIST = ('0.0.0.1');",
        ),
        (  # change comment
            oae.NetworkRuleAction(
                "MISC",
                "MY_NETWORK_RULE1",
                DbActionType.ALTER,
                "CREATE OR REPLACE NETWORK RULE MISC.MY_NETWORK_RULE1 ...;",
                InstanceNetworkRule(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "MISC",
                        "OBJECT_NAME": "MY_NETWORK_RULE1",
                        "TYPE": "IPV4",
                        "MODE": "INGRESS",
                        "VALUE_LIST": "('0.0.0.0')",
                        "COMMENT": "whitelist"
                        }
                ),
                InstanceNetworkRule(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "MISC",
                        "OBJECT_NAME": "MY_NETWORK_RULE1",
                        "TYPE": "IPV4",
                        "MODE": "INGRESS",
                        "VALUE_LIST": "('0.0.0.0')",
                        "COMMENT": "blacklist"
                    }
                ),
            ),
            "ALTER NETWORK RULE MISC.MY_NETWORK_RULE1 SET COMMENT = 'blacklist';",
        ),
    ],
)
def test_networkrule_generate_alter_statement(
    network_rule_action: oae.NetworkRuleAction, expected: str
):
    result = oae.NetworkRuleAction._generate_alter_statement(network_rule_action)
    assert result == expected

# region network rule alter
@pytest.mark.parametrize(
    "object_name, schema_name, object_type, action, current_instance, desired_instance, expected_statement",
    [
        (
            "MY_NETWORK_RULE1",
            "MISC",
            DbObjectType.NETWORKRULE,
            DbActionType.ALTER,
            InstanceNetworkRule(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "MISC",
                        "OBJECT_NAME": "MY_NETWORK_RULE1",
                        "TYPE": "IPV4",
                        "MODE": "INGRESS",
                        "VALUE_LIST": "('0.0.0.0')",
                        "COMMENT": "whitelist"
                        }
                ),
                InstanceNetworkRule(
                    {
                        "DATABASE_NAME": "TWZ_META",
                        "SCHEMA_NAME": "MISC",
                        "OBJECT_NAME": "MY_NETWORK_RULE1",
                        "TYPE": "IPV4",
                        "MODE": "INGRESS",
                        "VALUE_LIST": "('0.0.0.0')",
                        "COMMENT": "blacklist"
                    }
                ),
            "ALTER NETWORK RULE MISC.MY_NETWORK_RULE1 SET COMMENT = 'blacklist';",
        )
    ],
)

def test_DbObjectAction_statement_network_rule_alter(
    object_name,
    schema_name,
    object_type,
    action,
    current_instance,
    desired_instance,
    expected_statement,
):
    # arrange
    object_action = oae.DbObjectAction.factory(
        schema_name,
        object_name,
        object_type,
        action,
        current_instance=current_instance,
        desired_instance=desired_instance,
    )

    # act
    statement = object_action._generate_statement()

    # assert
    assert statement.lower() == expected_statement.lower()


# endregion network rule alter