import acedeploy.core.model_instance_objects as mio
import pytest
from pytest_lazyfixture import lazy_fixture

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
    metadata_view,
    metadata_externaltable,
    metadata_dynamictable,
    metadata_networkrule,
)

# TODO: add unit tests for all functions


@pytest.mark.parametrize(
    "signature, expected",
    [
        ("", []),
        ("Name VARCHAR", ["VARCHAR"]),
        ("Name VARCHAR, Name_zwo VARCHAR", ["VARCHAR", "VARCHAR"]),
    ],
)
def test_queryresultdbobjectentry_parameter_parsing_success(signature, expected):
    result = mio.InstanceParameterObject.parse_parameters(signature)
    assert result == expected


@pytest.mark.parametrize(
    "signature, expected_error, expected_error_message",
    [
        ("Name", ValueError, "Parameter token list not valid."),
        (None, ValueError, "Signature can not be of type None."),
    ],
)
def test_queryresultdbobjectentry_parameter_parsing_failed(
    signature, expected_error, expected_error_message
):
    with pytest.raises(expected_error, match=expected_error_message):
        __ = mio.InstanceParameterObject.parse_parameters(signature)


@pytest.mark.parametrize(
    "object_type, metadata_query_result, expected_id, expected_full_name, expected_repr",
    [
        (
            mio.InstanceSchema,
            pytest.lazy_fixture("metadata_schema"),
            "DbObjectType.SCHEMA MY_SCHEMA",
            "MY_SCHEMA",
            "InstanceSchema: DbObjectType.SCHEMA MY_SCHEMA",
        ),
        (
            mio.InstanceFileformat,
            pytest.lazy_fixture("metadata_fileformat"),
            "DbObjectType.FILEFORMAT MY_SCHEMA.MY_OBJECT",
            "MY_SCHEMA.MY_OBJECT",
            "InstanceFileformat: DbObjectType.FILEFORMAT MY_SCHEMA.MY_OBJECT",
        ),
        (
            mio.InstanceStage,
            pytest.lazy_fixture("metadata_stage"),
            "DbObjectType.STAGE MY_SCHEMA.MY_OBJECT",
            "MY_SCHEMA.MY_OBJECT",
            "InstanceStage: DbObjectType.STAGE MY_SCHEMA.MY_OBJECT",
        ),
        (
            mio.InstanceFunction,
            pytest.lazy_fixture("metadata_function"),
            "DbObjectType.FUNCTION MY_SCHEMA.MY_OBJECT (FLOAT, NUMBER)",
            "MY_SCHEMA.MY_OBJECT (FLOAT, NUMBER)",
            "InstanceFunction: DbObjectType.FUNCTION MY_SCHEMA.MY_OBJECT (FLOAT, NUMBER)",
        ),
        (
            mio.InstanceProcedure,
            pytest.lazy_fixture("metadata_procedure"),
            "DbObjectType.PROCEDURE MY_SCHEMA.MY_OBJECT (FLOAT, NUMBER)",
            "MY_SCHEMA.MY_OBJECT (FLOAT, NUMBER)",
            "InstanceProcedure: DbObjectType.PROCEDURE MY_SCHEMA.MY_OBJECT (FLOAT, NUMBER)",
        ),
        (
            mio.InstanceTable,
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
                "COLUMN_DETAILS": [{"CHARACTER_MAXIMUM_LENGTH":11,"CHARACTER_OCTET_LENGTH":44,"COLLATION_NAME":"en-ci","COLUMN_DEFAULT":"\'x\'","COLUMN_NAME":"T4","DATABASE_NAME":"TWZ_META","DATA_TYPE":"TEXT","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","ORDINAL_POSITION":4,"TABLE_NAME":"TABLE2","TABLE_SCHEMA":"DATA"},{"CHARACTER_MAXIMUM_LENGTH":12,"CHARACTER_OCTET_LENGTH":48,"COLLATION_NAME":"en-ci","COLUMN_NAME":"T2","DATABASE_NAME":"TWZ_META","DATA_TYPE":"TEXT","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","ORDINAL_POSITION":2,"TABLE_NAME":"TABLE2","TABLE_SCHEMA":"DATA"},{"CHARACTER_MAXIMUM_LENGTH":11,"CHARACTER_OCTET_LENGTH":44,"COLUMN_NAME":"T1","DATABASE_NAME":"TWZ_META","DATA_TYPE":"TEXT","IS_IDENTITY":"NO","IS_NULLABLE":"YES","IS_SELF_REFERENCING":"NO","ORDINAL_POSITION":1,"TABLE_NAME":"TABLE2","TABLE_SCHEMA":"DATA"},{"CHARACTER_MAXIMUM_LENGTH":12,"CHARACTER_OCTET_LENGTH":48,"COLLATION_NAME":"en-ci","COLUMN_NAME":"T3","DATABASE_NAME":"TWZ_META","DATA_TYPE":"TEXT","IS_IDENTITY":"NO","IS_NULLABLE":"NO","IS_SELF_REFERENCING":"NO","ORDINAL_POSITION":3,"TABLE_NAME":"TABLE2","TABLE_SCHEMA":"DATA"}],
                "constraint_foreign_keys": [],
                "constraint_primary_keys": [],
                "constraint_unique_keys": [],
            },
            "DbObjectType.TABLE DATA.TABLE2",
            "DATA.TABLE2",
            "InstanceTable: DbObjectType.TABLE DATA.TABLE2",
        ),
        (
            mio.InstanceExternalTable,
            pytest.lazy_fixture("metadata_externaltable"),
            "DbObjectType.EXTERNALTABLE MISC.EXTTABLE1",
            "MISC.EXTTABLE1",
            "InstanceExternalTable: DbObjectType.EXTERNALTABLE MISC.EXTTABLE1",
        ),
        (
            mio.InstanceView,
            pytest.lazy_fixture("metadata_view"),
            "DbObjectType.VIEW VIEWS.VIEW1",
            "VIEWS.VIEW1",
            "InstanceView: DbObjectType.VIEW VIEWS.VIEW1",
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
            "DbObjectType.MATERIALIZEDVIEW VIEWS.VIEW1",
            "VIEWS.VIEW1",
            "InstanceMaterializedView: DbObjectType.MATERIALIZEDVIEW VIEWS.VIEW1",
        ),
        (
            mio.InstanceStream,
            pytest.lazy_fixture("metadata_stream"),
            "DbObjectType.STREAM MISC.MYSTREAM",
            "MISC.MYSTREAM",
            "InstanceStream: DbObjectType.STREAM MISC.MYSTREAM",
        ),
        (
            mio.InstanceTask,
            pytest.lazy_fixture("metadata_task"),
            "DbObjectType.TASK MISC.MYTASK",
            "MISC.MYTASK",
            "InstanceTask: DbObjectType.TASK MISC.MYTASK",
        ),
        (
            mio.InstancePipe,
            pytest.lazy_fixture("metadata_pipe"),
            "DbObjectType.PIPE MISC.MYPIPE",
            "MISC.MYPIPE",
            "InstancePipe: DbObjectType.PIPE MISC.MYPIPE",
        ),
        (
            mio.InstanceSequence,
            pytest.lazy_fixture("metadata_sequence"),
            "DbObjectType.SEQUENCE MISC.MYSEQUENCE",
            "MISC.MYSEQUENCE",
            "InstanceSequence: DbObjectType.SEQUENCE MISC.MYSEQUENCE",
        ),
        (
            mio.InstanceMaskingPolicy,
            pytest.lazy_fixture("metadata_maskingpolicy"),
            "DbObjectType.MASKINGPOLICY POLICIES.MYMASKINGPOLICY",
            "POLICIES.MYMASKINGPOLICY",
            "InstanceMaskingPolicy: DbObjectType.MASKINGPOLICY POLICIES.MYMASKINGPOLICY",
        ),
        (
            mio.InstanceRowAccessPolicy,
            pytest.lazy_fixture("metadata_rowaccesspolicy"),
            "DbObjectType.ROWACCESSPOLICY POLICIES.MYROWACCESSPOLICY",
            "POLICIES.MYROWACCESSPOLICY",
            "InstanceRowAccessPolicy: DbObjectType.ROWACCESSPOLICY POLICIES.MYROWACCESSPOLICY",
        ),
        (
            mio.InstanceDynamicTable,
            pytest.lazy_fixture("metadata_dynamictable"),
            "DbObjectType.DYNAMICTABLE DATA.DYNAMICTABLE1",
            "DATA.DYNAMICTABLE1",
            "InstanceDynamicTable: DbObjectType.DYNAMICTABLE DATA.DYNAMICTABLE1",
        ),
        (
            mio.InstanceNetworkRule,
            pytest.lazy_fixture("metadata_networkrule"),
            "DbObjectType.NETWORKRULE MISC.MY_NETWORK_RULE1",
            "MISC.MY_NETWORK_RULE1",
            "InstanceNetworkRule: DbObjectType.NETWORKRULE MISC.MY_NETWORK_RULE1",
        ),
    ],
)
def test_InstanceObject_properties(
    object_type, metadata_query_result, expected_id, expected_full_name, expected_repr
):
    obj = object_type(metadata_query_result)
    assert obj.id == expected_id
    assert obj.full_name == expected_full_name
    assert repr(obj) == expected_repr
    assert str(obj) == expected_repr


@pytest.mark.parametrize(
    "input, expected",
    [
        ("DEMO_DB.PUBLIC.T", "PUBLIC.T"),
        ('"DEMO_DB"."PUBLIC"."T"', '"PUBLIC"."T"'),
        ("PUBLIC.T", "PUBLIC.T"),
        ("VERY.WIERD.NAME.PUBLIC.T", "VERY.WIERD.NAME.PUBLIC.T"),
    ],
)
def test_stream_remove_database_from_table_name(input, expected):
    result = mio.InstanceStream._remove_database_from_table_name(input)
    assert result == expected


def test_AppliedRowAccessPolicy_properties():
    obj = mio.AppliedRowAccessPolicyLegacy(
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
    )
    assert obj.policy_db == "TWZ_TARGET"
    assert obj.policy_schema == "POLICIES"
    assert obj.policy_name == "RAP1"
    assert obj.policy_kind == "ROW_ACCESS_POLICY"
    assert obj.ref_database_name == "TWZ_TARGET"
    assert obj.ref_schema_name == "VIEWS"
    assert obj.ref_entity_name == "VIEW6"
    assert obj.ref_entity_domain == "VIEW"
    assert obj.ref_arg_column_names == ["I", "J"]


def test_AppliedMaskingPolicy_properties():
    obj = mio.AppliedMaskingPolicyLegacy(
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
    )
    assert obj.policy_db == "TWZ_TARGET"
    assert obj.policy_schema == "POLICIES"
    assert obj.policy_name == "MP1"
    assert obj.policy_kind == "MASKING_POLICY"
    assert obj.ref_database_name == "TWZ_TARGET"
    assert obj.ref_schema_name == "VIEWS"
    assert obj.ref_entity_name == "VIEW1"
    assert obj.ref_entity_domain == "VIEW"
    assert obj.ref_column_name == "J"


@pytest.mark.parametrize(
    "input, expected",
    [
        (None, []),
        ("[]", []),
        (
            """[
                "DBNAME.MISC.MY_FIRST_TASK"
            ]""",
            ["MISC.MY_FIRST_TASK"],
        ),
        (
            """[
                "DBNAME.PUBLIC.\\\"WIERD$NAME2(\\\""
            ]""",
            ['PUBLIC."WIERD$NAME2("'],
        ),
    ],
)
def test_parse_predecessors(input, expected):
    result = mio.InstanceTask._parse_predecessors(input, "DBNAME")
    assert result == expected
