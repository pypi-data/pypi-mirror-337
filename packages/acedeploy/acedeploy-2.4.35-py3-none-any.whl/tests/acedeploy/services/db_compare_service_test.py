from typing import List, Union

import acedeploy.core.model_instance_objects as mio
import acedeploy.services.db_compare_service as dcs
import acedeploy.services.metadata_service as mds
import pytest
from acedeploy.core.model_object_action_entities import DbObjectAction
from acedeploy.core.model_solution_entities import SolutionObject
from acedeploy.core.model_sql_entities import DbActionType, DbObjectType
from acedeploy.services.solution_service import SolutionClient

# TODO: add tests which directly call each function
# Extend test set to use all possible types


class DummyMetadataService(mds.MetadataService):
    def __init__(self, instance_objects: List[mio.InstanceObject]):
        self.all_objects = instance_objects
        self._populate_all_objects_dict_by_id()


class DummyInstanceObject(mio.InstanceObject):
    def __init__(self, schema, name, object_type, parameters=[]):
        self.schema = schema
        self.name = name
        self.object_type = object_type
        self.parameters = parameters

    def __str__(self):
        return f"DummyInstanceObject: {self.id}"

    def __repr__(self):
        return f"DummyInstanceObject: {self.id}"


class DummySolutionClient(SolutionClient):
    def __init__(self, all_objects: List[SolutionObject]):
        self.project_folder = "dummy/folder"
        self.all_objects = all_objects
        self.postdeployment_steps = []
        self.predeployment_steps = []
        self._populate_all_objects_dict_by_full_name()
        self._populate_all_objects_dict_by_id()
        self._populate_parameterobjects_dict_by_name_without_parameters()


class DummySolutionObject(SolutionObject):
    def __init__(self, object_type, schema, name, content, parameters=[]):
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


class DummyDbObjectAction(DbObjectAction):
    def __init__(
        self,
        schema: str,
        name: str,
        file_content: str,
        object_type: DbObjectType,
        action: DbActionType,
    ):
        self.schema = schema
        self.name = name
        self.file_content = file_content
        self.object_type = object_type
        self.action = action

    def _generate_statement(self):
        return "dummy statement"

    def __str__(self):
        return f"DummyDbObjectAction: {self.id}"

    def __repr__(self):
        return f"DummyDbObjectAction: {self.id}"

    def __eq__(self, other):
        return (
            self.schema,
            self.name,
            self.file_content,
            self.object_type,
            self.action,
        ) == (
            other.schema,
            other.name,
            other.file_content,
            other.object_type,
            other.action,
        )


# TODO: also need to test other object types
# for these tests we use materialized views, because they must be recreated from solution object (as they cannot be created from desired instance object, as this is missing the view definition)
@pytest.fixture
def base_solution_client():
    all_objects = [
        DummySolutionObject(
            DbObjectType.TABLE,
            "CORE",
            "TABLE0",
            "CREATE TABLE CORE.TABLE0 (col1 INT, col2 VARCHAR(10));",
        ),
        DummySolutionObject(
            DbObjectType.TABLE,
            "CORE",
            "TABLE1",
            "CREATE TABLE CORE.TABLE1 (col1 INT, col2 VARCHAR(10));",
        ),
        DummySolutionObject(
            DbObjectType.MATERIALIZEDVIEW,
            "CORE",
            "VIEW2",
            "CREATE VIEW CORE.VIEW2 AS SELECT col1 FROM CORE.TABLE0;",
        ),
        DummySolutionObject(
            DbObjectType.MATERIALIZEDVIEW,
            "CORE",
            "VIEW3",
            "CREATE VIEW CORE.VIEW3 AS SELECT col1 FROM CORE.TABLE1;",
        ),
        DummySolutionObject(
            DbObjectType.MATERIALIZEDVIEW,
            "CORE",
            "VIEW4",
            "CREATE VIEW CORE.VIEW4 AS SELECT col2 AS a FROM CORE.VIEW2 JOIN SELECT col2 AS b FROM CORE.VIEW3 ON a=b;",
        ),
        DummySolutionObject(
            DbObjectType.TABLE,
            "CORE",
            "TABLE5",
            "CREATE TABLE CORE.TABLE5 (col1 INT, col2 VARCHAR(10));",
        ),
        DummySolutionObject(
            DbObjectType.MATERIALIZEDVIEW,
            "CORE",
            "VIEW6",
            "CREATE VIEW CORE.VIEW6 AS SELECT col1 FROM CORE.TABLE5;",
        ),
        DummySolutionObject(
            DbObjectType.TABLE,
            "CORE",
            "TABLE7",
            "CREATE TABLE CORE.TABLE7 (col1 INT, col2 VARCHAR(10));",
        ),
        DummySolutionObject(
            DbObjectType.MATERIALIZEDVIEW,
            "CORE",
            "VIEW8",
            "CREATE VIEW CORE.VIEW8 AS SELECT col1 FROM CORE.VIEW3;",
        ),
    ]
    return DummySolutionClient(all_objects)


@pytest.fixture
def base_desired_state():
    objects = [
        DummyInstanceObject("CORE", "VIEW2", DbObjectType.MATERIALIZEDVIEW),
        DummyInstanceObject("CORE", "VIEW8", DbObjectType.MATERIALIZEDVIEW),
    ]
    return DummyMetadataService(objects)


@pytest.fixture
def base_current_state():
    objects = [
        DummyInstanceObject("CORE", "VIEW3", DbObjectType.MATERIALIZEDVIEW),
        DummyInstanceObject("CORE", "VIEW8", DbObjectType.MATERIALIZEDVIEW),
        DummyInstanceObject("CORE", "VIEW_DROP_ME", DbObjectType.MATERIALIZEDVIEW),
    ]
    return DummyMetadataService(objects)


@pytest.fixture
def base_add_action_list():
    return [
        DummyDbObjectAction(
            "CORE",
            "VIEW2",
            "CREATE VIEW CORE.VIEW2 AS SELECT col1 FROM CORE.TABLE0;",
            DbObjectType.MATERIALIZEDVIEW,
            DbActionType.ADD,
        )
    ]


@pytest.fixture
def base_drop_action_list():
    return [
        DummyDbObjectAction(
            "CORE",
            "VIEW_DROP_ME",
            None,
            DbObjectType.MATERIALIZEDVIEW,
            DbActionType.DROP,
        )
    ]


@pytest.fixture
def base_alter_action_list():
    return [
        DummyDbObjectAction(
            "CORE",
            "VIEW8",
            "CREATE VIEW CORE.VIEW8 AS SELECT col1 FROM CORE.VIEW3;",
            DbObjectType.MATERIALIZEDVIEW,
            DbActionType.ALTER,
        )
    ]


def test_DbCompareClient_init(
    base_desired_state, base_current_state, base_solution_client
):
    db_compare_client = dcs.DbCompareClient(
        base_desired_state, base_current_state, base_solution_client
    )
    assert db_compare_client._desired_state == base_desired_state
    assert db_compare_client._current_state == base_current_state
    assert db_compare_client._solution_client == base_solution_client
    assert db_compare_client.action_list == []


def test_DbCompareClient_init_error(base_desired_state, base_current_state):
    empty_solution_client = DummySolutionClient([])
    with pytest.raises(ValueError):
        __ = dcs.DbCompareClient(
            base_desired_state, base_current_state, empty_solution_client
        )


def test_get_add_actions(
    base_desired_state, base_current_state, base_solution_client, base_add_action_list
):
    db_compare_client = dcs.DbCompareClient(
        base_desired_state, base_current_state, base_solution_client
    )
    db_compare_client.get_add_actions()
    assert sorted(db_compare_client.action_list) == sorted(base_add_action_list)


def test_get_drop_actions_from_solution(
    base_desired_state, base_current_state, base_solution_client, base_drop_action_list
):
    db_compare_client = dcs.DbCompareClient(
        base_desired_state, base_current_state, base_solution_client
    )
    db_compare_client.get_drop_actions_from_solution()
    assert sorted(db_compare_client.action_list) == sorted(base_drop_action_list)


def test_get_drop_actions_from_git_error(
    base_desired_state, base_current_state, base_solution_client
):
    db_compare_client = dcs.DbCompareClient(
        base_desired_state, base_current_state, base_solution_client
    )
    with pytest.raises(NotImplementedError):
        db_compare_client.get_drop_actions_from_git()


def test_get_alter_actions(
    base_desired_state, base_current_state, base_solution_client, base_alter_action_list
):
    db_compare_client = dcs.DbCompareClient(
        base_desired_state, base_current_state, base_solution_client
    )
    db_compare_client.get_alter_actions()
    assert sorted(db_compare_client.action_list) == sorted(base_alter_action_list)
