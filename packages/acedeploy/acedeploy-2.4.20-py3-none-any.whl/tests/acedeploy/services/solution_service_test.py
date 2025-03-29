from unittest.mock import patch
from acedeploy.core.model_configuration import PreOrPostdeploymentConfigList

import acedeploy.core.model_instance_objects as mio
import acedeploy.core.model_solution_entities as mse
import acedeploy.services.solution_service as sos
import pytest
from acedeploy.core.model_sql_entities import DbObjectType


def test_solution_service_init_legacy():
    s = sos.SolutionClient(
        project_folder="some/folder",
        predeployment_folders=["f/pre"],
        postdeployment_folders=["f/post"],
        prepostdeployment_filter_list=["DATABASE"],
        config_schema_list={"blacklist": ["PUBLIC"]},
        disabled_object_types=[DbObjectType.EXTERNALTABLE],
    )
    assert s.pre_and_postdeployment_folders == ["f/pre", "f/post"]
    assert s.predeployment_settings == PreOrPostdeploymentConfigList.from_dict(
        [{"path": "f/pre", "type": "folder", "condition": "onChange", "target": "targetDatabase"}], ""
    )
    assert s.postdeployment_settings == PreOrPostdeploymentConfigList.from_dict(
        [{"path": "f/post", "type": "folder", "condition": "onChange", "target": "targetDatabase"}], ""
    )
    assert s.project_folder == "some/folder"
    assert s.config_schema_list == {"blacklist": ["PUBLIC"]}
    assert s.all_objects == []
    assert s.predeployment_steps == []
    assert s.postdeployment_steps == []
    assert s.disabled_object_types == [DbObjectType.EXTERNALTABLE]


def test_solution_service_init():
    s = sos.SolutionClient(
        project_folder="some/folder",
        predeployment_settings=PreOrPostdeploymentConfigList.from_dict(
            [{"path": "f/pre", "type": "folder", "condition": "onChange"}], ""
        ),
        postdeployment_settings=PreOrPostdeploymentConfigList.from_dict(
            [
                {"path": "f/post", "type": "folder", "condition": "onChange"},
                {"path": "f/post2", "type": "folder", "condition": "always", "target": "metaDatabase"}
            ], ""
        ),
        prepostdeployment_filter_list=["DATABASE"],
        config_schema_list={"blacklist": ["PUBLIC"]},
    )
    assert s.pre_and_postdeployment_folders == ["f/pre", "f/post", "f/post2"]
    assert s.predeployment_settings == PreOrPostdeploymentConfigList.from_dict(
        [{"path": "f/pre", "type": "folder", "condition": "onChange", "target": "targetDatabase"}], ""
    )
    assert s.postdeployment_settings == PreOrPostdeploymentConfigList.from_dict(
        [
            {"path": "f/post", "type": "folder", "condition": "onChange", "target": "targetDatabase"},
            {"path": "f/post2", "type": "folder", "condition": "always", "target": "metaDatabase"}
        ], ""
    )
    assert s.project_folder == "some/folder"
    assert s.config_schema_list == {"blacklist": ["PUBLIC"]}
    assert s.all_objects == []
    assert s.predeployment_steps == []
    assert s.postdeployment_steps == []
    assert s.disabled_object_types == []


def test_solution_service_error():
    with pytest.raises(ValueError):
        __ = sos.SolutionClient(
            project_folder="some/folder",
            predeployment_folders=["f/pre"],
            postdeployment_folders=["f/post"],
            predeployment_settings=PreOrPostdeploymentConfigList.from_dict(
                [{"path": "f/pre", "type": "folder", "condition": "onChange"}], ""
            ),
            postdeployment_settings=PreOrPostdeploymentConfigList.from_dict(
                [{"path": "f/post", "type": "folder", "condition": "onChange"}], ""
            ),
            prepostdeployment_filter_list=["DATABASE"],
            config_schema_list={"blacklist": ["PUBLIC"]},
        )


@pytest.fixture
def test_object_set():
    objects = [
        mse.SolutionTable(
            "/my/file/path/myschema.mytable.sql",
            "CREATE OR REPLACE TABLE MYSCHEMA.MYTABLE ()",
        ),
        mse.SolutionView(
            "/my/file/path/myschema.myview.sql",
            "CREATE OR REPLACE VIEW MYSCHEMA.MYVIEW ()",
        ),
        mse.SolutionMaterializedView(
            "/my/file/path/myschema.mymatview.sql",
            "CREATE OR REPLACE MATERIALIZED VIEW MYSCHEMA.MYMATVIEW ()",
        ),
        mse.SolutionFunction(
            "/my/file/path/myschema.myfunction.sql",
            "CREATE OR REPLACE FUNCTION MYSCHEMA.MYFUNCTION (V VARCHAR)",
        ),
        mse.SolutionProcedure(
            "/my/file/path/myschema.myprocedure.sql",
            "CREATE OR REPLACE PROCEDURE MYSCHEMA.MYPROCEDURE (V VARCHAR)",
        ),
        mse.SolutionFileformat(
            "/my/file/path/myschema.myfileformat.sql",
            "CREATE OR REPLACE FILE FORMAT MYSCHEMA.MYFILEFORMAT ()",
        ),
        mse.SolutionExternalTable(
            "/my/file/path/myschema.myexttable.sql",
            "CREATE OR REPLACE EXTERNAL TABLE MYSCHEMA.MYEXTTABLE ()",
        ),
        mse.SolutionStage(
            "/my/file/path/myschema.mystage.sql",
            "CREATE OR REPLACE STAGE MYSCHEMA.MYSTAGE ()",
        ),
        mse.SolutionStream(
            "/my/file/path/myschema.mystream.sql",
            "CREATE OR REPLACE STREAM MYSCHEMA.MYSTREAM ()",
        ),
        mse.SolutionTask(
            "/my/file/path/myschema.mytask.sql",
            "CREATE OR REPLACE TASK MYSCHEMA.MYTASK ()",
        ),
        mse.SolutionPipe(
            "/my/file/path/myschema.mypipe.sql",
            "CREATE OR REPLACE PIPE MYSCHEMA.MYPIPE ()",
        ),
        mse.SolutionDynamicTable(
            "/my/file/path/myschema.mydynamictable.sql",
            "CREATE OR REPLACE DYNAMIC TABLE MYSCHEMA.MYDYNAMICTABLE ()",
        ),
        mse.SolutionNetworkRule(
            "/my/file/path/myschema.mynetworkrule.sql",
            "CREATE OR REPLACE NETWORK RULE MYSCHEMA.MYNETWORKRULE ()",
        ),
        mse.SolutionSchema(
            "/my/file/path/myschema.sql",
            "CREATE OR REPLACE SCHEMA MYSCHEMA",
        ),
    ]
    return objects


def test_get_object_by_id(test_object_set):
    solution_service = sos.SolutionClient("dummy_folder")
    solution_service.all_objects = test_object_set
    solution_service._populate_all_objects_dict_by_id()

    for o in test_object_set:
        assert solution_service.get_object_by_id(o.id) == o
    assert (
        solution_service.get_object_by_id('DbObjectType.VIEW "MYSCHEMA"."MYVIEW"')
        == test_object_set[1]
    )
    assert solution_service.get_object_by_id("DbObjectType.VIEW MYSCHEMA.WRONG") is None
    assert solution_service.get_object_by_id("DbObjectType.VIEW WRONG.MYVIEW") is None


def test_get_object_by_full_name(test_object_set):
    solution_service = sos.SolutionClient("dummy_folder")
    solution_service.all_objects = test_object_set
    solution_service._populate_all_objects_dict_by_full_name()

    for o in test_object_set:
        assert solution_service.get_object_by_full_name(o.full_name) == o
    assert (
        solution_service.get_object_by_full_name('"MYSCHEMA"."MYVIEW"')
        == test_object_set[1]
    )
    assert solution_service.get_object_by_full_name("MYSCHEMA.WRONG") is None
    assert solution_service.get_object_by_full_name("WRONG.MYVIEW") is None


def test_get_object_by_full_name_include_schema_false(test_object_set):
    solution_service = sos.SolutionClient("dummy_folder")
    solution_service.all_objects = test_object_set
    solution_service._populate_all_objects_dict_by_full_name()

    for o in test_object_set:
        if o.object_type != DbObjectType.SCHEMA:
            assert solution_service.get_object_by_full_name(o.full_name, False) == o
        else:
            assert solution_service.get_object_by_full_name(o.full_name, False) is None
    assert (
        solution_service.get_object_by_full_name('"MYSCHEMA"."MYVIEW"', False)
        == test_object_set[1]
    )
    assert solution_service.get_object_by_full_name("MYSCHEMA.WRONG", False) is None
    assert solution_service.get_object_by_full_name("WRONG.MYVIEW", False) is None


def test_get_object_by_object(test_object_set):
    solution_service = sos.SolutionClient("dummy_folder")
    solution_service.all_objects = test_object_set
    solution_service._populate_all_objects_dict_by_id()

    for o in test_object_set:
        assert solution_service.get_object_by_object(o) == o

    o1 = mse.SolutionTable(
        "/my/file/path/myschema.mytable_new.sql",
        "CREATE OR REPLACE TABLE MYSCHEMA.MYTABLE_NEW ()",
    )
    assert solution_service.get_object_by_object(o1) is None

    o2 = mio.InstanceFunction(
        {
            "DATABASE_NAME": "DUMMY_DB",
            "SCHEMA_NAME": "MYSCHEMA",
            "OBJECT_NAME": "MYFUNCTION",
            "SIGNATURE": "(V VARCHAR)",
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
    )

    assert solution_service.get_object_by_object(o2) == test_object_set[3]
    o2 = mio.InstanceFunction(
        {
            "DATABASE_NAME": "DUMMY_DB",
            "SCHEMA_NAME": "MYSCHEMA",
            "OBJECT_NAME": "MYFUNCTION",
            "SIGNATURE": "(V INT)",
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
    )
    assert solution_service.get_object_by_object(o2) is None  # wrong signature
    o2 = mio.InstanceFunction(
        {
            "DATABASE_NAME": "DUMMY_DB",
            "SCHEMA_NAME": "MYSCHEMA",
            "OBJECT_NAME": "WRONG",
            "SIGNATURE": "(V VARCHAR)",
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
    )
    assert solution_service.get_object_by_object(o2) is None  # wrong object_name


def test_get_parameterobject_by_name_without_params(test_object_set):
    solution_service = sos.SolutionClient("dummy_folder")
    solution_service.all_objects = test_object_set
    solution_service._populate_parameterobjects_dict_by_name_without_parameters()

    assert (
        solution_service.get_parameterobject_by_name_without_params(
            "MYSCHEMA.MYFUNCTION"
        )
        == test_object_set[3]
    )
    assert (
        solution_service.get_parameterobject_by_name_without_params(
            '"MYSCHEMA"."MYFUNCTION"'
        )
        == test_object_set[3]
    )
    assert (
        solution_service.get_parameterobject_by_name_without_params(
            "MYSCHEMA.WRONGFUNCTION"
        )
        is None
    )


def test_validate_object_ids_unique(test_object_set):
    solution_service = sos.SolutionClient("dummy_folder")
    solution_service.all_objects = test_object_set
    # check if no error is raised with the following line
    solution_service._validate_object_ids_unique()

    # add a duplicate object so the function should raise an error
    solution_service.all_objects.append(test_object_set[0])
    with pytest.raises(ValueError):
        solution_service._validate_object_ids_unique()


class DummySolutionObject(mse.SolutionObject):
    def __init__(self, object_type, schema, name, content="", parameters=[]):
        self.schema = schema
        self.name = name
        self.object_type = object_type
        self.content = content
        self.parameters = parameters
        self.path = "dummy"
        self.git_change_type = None

    def __str__(self):
        return f"DummySolutionObject: {self.id}"

    def __repr__(self):
        return f"DummySolutionObject: {self.id}"


@pytest.mark.parametrize(
    "solution_objects, schema_list, expected",
    [
        ([], {"whitelist": []}, []),
        ([], {"blacklist": []}, []),
        (
            [
                DummySolutionObject(
                    object_type=DbObjectType.VIEW, schema="my_schema", name="my_object"
                )
            ],
            {"whitelist": []},
            [
                DummySolutionObject(
                    object_type=DbObjectType.VIEW, schema="my_schema", name="my_object"
                )
            ],
        ),
        (
            [
                DummySolutionObject(
                    object_type=DbObjectType.VIEW, schema="my_schema", name="my_object"
                )
            ],
            {"blacklist": []},
            [],
        ),
        (
            [
                DummySolutionObject(
                    object_type=DbObjectType.VIEW, schema="my_schema", name="my_object"
                )
            ],
            {"whitelist": ["MY_SCHEMA"]},
            [],
        ),
        (
            [
                DummySolutionObject(
                    object_type=DbObjectType.VIEW, schema="my_schema", name="my_object"
                )
            ],
            {"blacklist": ["MY_SCHEMA"]},
            [
                DummySolutionObject(
                    object_type=DbObjectType.VIEW, schema="my_schema", name="my_object"
                )
            ],
        ),
        (
            [
                DummySolutionObject(
                    object_type=DbObjectType.VIEW, schema="my_schema", name="my_object"
                ),
                DummySolutionObject(
                    object_type=DbObjectType.VIEW,
                    schema="my_second_schema",
                    name="my_object",
                ),
            ],
            {"whitelist": ["MY_SCHEMA", "MY_SECOND_SCHEMA"]},
            [],
        ),
        (
            [
                DummySolutionObject(
                    object_type=DbObjectType.VIEW, schema="my_schema", name="my_object"
                ),
                DummySolutionObject(
                    object_type=DbObjectType.VIEW,
                    schema="my_second_schema",
                    name="my_object",
                ),
            ],
            {"blacklist": ["MY_SCHEMA"]},
            [
                DummySolutionObject(
                    object_type=DbObjectType.VIEW, schema="my_schema", name="my_object"
                )
            ],
        ),
    ],
)
def test_get_solution_objects_not_in_schema_list(
    solution_objects, schema_list, expected
):
    result = sos.SolutionClient._get_solution_objects_not_in_schema_list(
        solution_objects, schema_list
    )
    assert str(set(result)) == str(set(expected))
