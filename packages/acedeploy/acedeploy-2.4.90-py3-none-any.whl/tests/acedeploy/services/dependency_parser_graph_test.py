from typing import List, Union

import acedeploy.core.model_solution_entities as mse
import networkx as nx
import pytest
from acedeploy.core.model_sql_entities import DbObjectType
from acedeploy.services.dependency_parser import DependencyParser
from acedeploy.services.solution_service import SolutionClient


def a_before_b(l, a, b):
    return l.index(a) < l.index(b)


class DummySolutionClient(SolutionClient):
    def __init__(
        self, all_objects: List[Union[mse.SolutionObject, mse.SolutionSchema]]
    ):
        self.project_folder = "dummy/folder"
        self.all_objects = all_objects
        self._populate_all_objects_dict_by_full_name()
        self._populate_all_objects_dict_by_id()
        self._populate_parameterobjects_dict_by_name_without_parameters()
        self.postdeployment_steps = []
        self.predeployment_steps = []


class DummySolutionObject(mse.SolutionObject):
    def __init__(self, object_type, schema, name, content, parameters=[]):
        self.schema = schema
        self.name = name
        self.object_type = object_type
        self.content = content
        self.parameters = []
        self.path = "dummy"
        self.git_change_type = None

    def __str__(self):
        return f"DummySolutionObject: {self.id}"

    def __repr__(self):
        return f"DummySolutionObject: {self.id}"

class DummySolutionSchema(mse.SolutionSchema):
    def __init__(self, object_type, schema, name, content):
        self.schema = schema
        self.name = name
        self.object_type = object_type
        self.content = content
        self.path = "dummy"
        self.git_change_type = None

    def __str__(self):
        return f"DummySolutionObject: {self.id}"

    def __repr__(self):
        return f"DummySolutionObject: {self.id}"


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
            DbObjectType.VIEW,
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
            DbObjectType.VIEW,
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
            DbObjectType.VIEW,
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
            DbObjectType.VIEW,
            "CORE",
            "VIEW8",
            "CREATE VIEW CORE.VIEW8 AS SELECT col1 FROM CORE.VIEW3;",
        ),
    ]
    return DummySolutionClient(all_objects)


@pytest.fixture
def base_solution_client_edges(base_solution_client):
    objects = base_solution_client.all_objects
    return (
        (objects[0], objects[2]),
        (objects[1], objects[3]),
        (objects[2], objects[4]),
        (objects[3], objects[4]),
        (objects[5], objects[6]),
        (objects[3], objects[8]),
    )


@pytest.fixture
def base_solution_client_subgraphs(base_solution_client):
    objects = base_solution_client.all_objects
    g1 = nx.DiGraph()
    g1.add_edges_from(
        [
            (objects[0], objects[2]),
            (objects[1], objects[3]),
            (objects[2], objects[4]),
            (objects[3], objects[4]),
            (objects[3], objects[8]),
        ]
    )
    g2 = nx.DiGraph()
    g2.add_edges_from([(objects[5], objects[6])])
    g3 = nx.DiGraph()
    g3.add_nodes_from([objects[7]])
    return [g1, g2, g3]


def test_build_full_dependency_graph(base_solution_client, base_solution_client_edges):
    dep_client = DependencyParser(base_solution_client)
    dep_client.build_full_dependency_graph(
        (
            DbObjectType.TABLE,
            DbObjectType.VIEW,
            DbObjectType.MATERIALIZEDVIEW,
            DbObjectType.FUNCTION,
        )
    )
    assert set(dep_client._dependency_graph.nodes()) == set(
        base_solution_client.all_objects
    ), "Test if all objects appear as nodes"
    assert set(dep_client._dependency_graph.edges()) == set(base_solution_client_edges)


def test_get_dependencies(base_solution_client, base_solution_client_edges):
    dep_client = DependencyParser(base_solution_client)
    dep_client.function_name_list = [
        f"{o.schema}.{o.name}"
        for o in base_solution_client.all_objects
        if o.object_type == DbObjectType.FUNCTION
    ]
    for obj in base_solution_client.all_objects:
        expected_dependencies = [
            o[0] for o in base_solution_client_edges if o[1] == obj
        ]
        assert set(dep_client._get_dependencies(obj)) == set(expected_dependencies)


def test_get_dependencies_no_refs_on_schema():
    # we had some issues when a CTE had the name of a schema.
    # in those cases, the schema would appear as a dependency of a view.
    # that caused the schema to be deployed twice.
    # this test makes sure that these kind of views do not list schemas as a dependency.
    base_solution_client2 = DummySolutionClient(
        [
            DummySolutionObject(
                DbObjectType.VIEW,
                "CORE",
                "VIEW9",
                "CREATE VIEW CORE.VIEW9 AS WITH CORE AS (SELECT 1 A) SELECT * FROM CORE;",
            ),
            DummySolutionSchema(
                DbObjectType.SCHEMA,
                "CORE",
                "CORE",
                "CREATE SCHEMA CORE;",
            ),
        ]
    )
    dep_client2 = DependencyParser(base_solution_client2)
    dep_client2.function_name_list = [
        f"{o.schema}.{o.name}"
        for o in base_solution_client2.all_objects
        if o.object_type == DbObjectType.FUNCTION
    ]
    for obj in base_solution_client2.all_objects:
        assert dep_client2._get_dependencies(obj) == []

class DummyDependencyParser(DependencyParser):
    def __init__(self, solution_client, edges):
        super().__init__(solution_client)
        self._dependency_graph = nx.DiGraph()
        self._dependency_graph.add_edges_from(edges)
        self._dependency_graph.add_nodes_from(solution_client.all_objects)


@pytest.mark.parametrize(
    "object_indices, mode, expected_object_indices",
    [
        ([], "target_deployment", []),
        ([0], "target_deployment", [0]),
        ([0, 1, 2, 3, 4, 5, 6], "target_deployment", [0, 1, 2, 3, 4, 5, 6]),
        ([2, 5], "target_deployment", [2, 5]),
        ([], "meta_deployment", []),
        ([0], "meta_deployment", [0, 1, 2, 3, 4]),
        ([1], "meta_deployment", [0, 1, 2, 3, 4, 8]),
        ([2], "meta_deployment", [0, 1, 2, 3, 4]),
        ([3], "meta_deployment", [0, 1, 2, 3, 4, 8]),
        ([4], "meta_deployment", [0, 1, 2, 3, 4]),
        ([5], "meta_deployment", [5, 6]),
        ([6], "meta_deployment", [5, 6]),
        ([7], "meta_deployment", [7]),
        ([8], "meta_deployment", [1, 3, 8]),
        ([0, 2], "meta_deployment", [0, 1, 2, 3, 4]),
        ([2, 7], "meta_deployment", [0, 1, 2, 3, 4, 7]),
        ([2, 8], "meta_deployment", [0, 1, 2, 3, 4, 8]),
        ([2, 5], "meta_deployment", [0, 1, 2, 3, 4, 5, 6]),
    ],
)
def test_filter_graph_by_object_ids(
    object_indices,
    mode,
    expected_object_indices,
    base_solution_client,
    base_solution_client_edges,
):
    object_ids = [base_solution_client.all_objects[i].id for i in object_indices]
    expected = [base_solution_client.all_objects[i] for i in expected_object_indices]
    dep_client = DummyDependencyParser(base_solution_client, base_solution_client_edges)
    dep_client.filter_graph_by_object_ids(object_ids, mode=mode)
    assert set(dep_client._dependency_graph.nodes()) == set(expected)


def test_filter_graph_by_object_ids_error(
    base_solution_client, base_solution_client_edges
):
    object_ids = []
    dep_client = DummyDependencyParser(base_solution_client, base_solution_client_edges)
    with pytest.raises(ValueError):
        dep_client.filter_graph_by_object_ids(object_ids, mode="wrong_mode")


def test_build_subgraphs(
    base_solution_client, base_solution_client_edges, base_solution_client_subgraphs
):
    dep_client = DummyDependencyParser(base_solution_client, base_solution_client_edges)
    dep_client.build_subgraphs()
    for result_subgraph, expected_subgraph in zip(
        dep_client._dependency_subgraphs, base_solution_client_subgraphs
    ):
        assert set(result_subgraph.nodes()) == set(expected_subgraph.nodes())
        assert set(result_subgraph.edges()) == set(expected_subgraph.edges())


def test_get_ordered_objects(
    base_solution_client, base_solution_client_edges, base_solution_client_subgraphs
):
    o = base_solution_client.all_objects
    expected_a_before_b_tuples = [
        (o[0], o[2]),
        (o[1], o[3]),
        (o[2], o[4]),
        (o[0], o[4]),
        (o[3], o[4]),
        (o[1], o[4]),
        (o[5], o[6]),
        (o[3], o[8]),
        (o[1], o[8]),
    ]
    dep_client = DummyDependencyParser(base_solution_client, base_solution_client_edges)
    dep_client._dependency_subgraphs = base_solution_client_subgraphs
    result = dep_client.get_ordered_objects()
    for sublist in result:
        for expected_a_before_b_tuple in expected_a_before_b_tuples:
            a = expected_a_before_b_tuple[0]
            b = expected_a_before_b_tuple[1]
            if a in sublist and b in sublist:
                assert a_before_b(sublist, a, b)
