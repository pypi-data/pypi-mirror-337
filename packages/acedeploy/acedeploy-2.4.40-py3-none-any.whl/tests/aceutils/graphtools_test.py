import re

import aceutils.graphtools as gt
import networkx as nx
import pytest


def a_before_b(l, a, b):
    return l.index(a) < l.index(b)


class DummyDiGraph(nx.DiGraph):
    def __init__(self, *args, edges_list=[], nodes_list=[], **kwargs):
        super().__init__(*args, **kwargs)
        self.add_edges_from(edges_list)
        self.add_nodes_from(nodes_list)

    def __eq__(self, other):
        return set(list(self.nodes)) == set(list(other.nodes)) and set(
            list(self.edges)
        ) == set(list(other.edges))


@pytest.mark.parametrize(
    "input_edges, expected_edges, expected_nodes_with_no_edges",
    [
        # no loops
        ([], [], []),
        ([(0, 1)], [(0, 1)], []),
        ([(0, 1), (1, 2)], [(0, 1), (1, 2)], []),
        ([(0, 1), (1, 2), (3, 4)], [(0, 1), (1, 2), (3, 4)], []),
        # loops
        ([(0, 0)], [], [0]),
        ([(0, 0), (1, 2)], [(1, 2)], [0]),
        ([(0, 0), (1, 0)], [(1, 0)], []),
        ([(0, 0), (1, 1)], [], [0, 1]),
        ([(0, 0), (1, 1), (1, 0)], [(1, 0)], []),
    ],
)
def test_remove_self_loops(input_edges, expected_edges, expected_nodes_with_no_edges):
    input_graph = DummyDiGraph(edges_list=input_edges)
    result = gt.remove_self_loops(input_graph)
    expected_graph = DummyDiGraph(
        edges_list=expected_edges, nodes_list=expected_nodes_with_no_edges
    )
    assert result == expected_graph


@pytest.mark.parametrize(
    "input_edges, expected_edges_list",
    [
        ([], []),
        ([(0, 1)], [[(0, 1)]]),
        ([(0, 1), (1, 2)], [[(0, 1), (1, 2)]]),
        ([(0, 1), (1, 2), (3, 4)], [[(0, 1), (1, 2)], [(3, 4)]]),
    ],
)
def test_split_graph_into_subgraphs(input_edges, expected_edges_list):
    input_graph = DummyDiGraph(edges_list=input_edges)
    result = gt.split_graph_into_subgraphs(input_graph)
    expected_graphs = [DummyDiGraph(edges_list=e) for e in expected_edges_list]
    assert result == expected_graphs


@pytest.mark.parametrize(
    "input_edges, starting_node, expected_nodes",
    [
        ([(0, 1)], 1, [1]),
        ([(0, 1)], 0, [0, 1]),
        ([(0, 1), (1, 2)], 0, [0, 1, 2]),
        ([(0, 1), (1, 2), (1, 3)], 0, [0, 1, 2, 3]),
        ([(0, 1), (1, 2), (1, 3)], 1, [1, 2, 3]),
        ([(0, 1), (1, 2), (1, 3)], 2, [2]),
        ([(0, 1), (1, 2), (1, 3), (2, 3)], 2, [2, 3]),
        ([(0, 1), (1, 2), (1, 3), (2, 4)], 2, [2, 4]),
        ([(0, 1), (1, 2), (1, 3), (4, 5)], 2, [2]),
    ],
)
def test_get_all_successor_nodes_and_graph(input_edges, starting_node, expected_nodes):
    input_graph = DummyDiGraph(edges_list=input_edges)
    result = gt.get_all_successor_nodes(input_graph, starting_node)
    assert isinstance(result, set)
    assert set(result) == set(expected_nodes)


@pytest.mark.parametrize(
    "input_edges, starting_node, expected_edges_list, expected_nodes_with_no_edges",
    [
        ([(0, 1)], 1, [], [1]),
        ([(0, 1)], 0, [(0, 1)], []),
        ([(0, 1), (1, 2)], 0, [(0, 1), (1, 2)], []),
        ([(0, 1), (1, 2), (1, 3)], 0, [(0, 1), (1, 2), (1, 3)], []),
        ([(0, 1), (1, 2), (1, 3)], 1, [(1, 2), (1, 3)], []),
        ([(0, 1), (1, 2), (1, 3)], 2, [], [2]),
        ([(0, 1), (1, 2), (1, 3), (2, 3)], 2, [(2, 3)], []),
        ([(0, 1), (1, 2), (1, 3), (2, 4)], 2, [(2, 4)], []),
        ([(0, 1), (1, 2), (1, 3), (4, 5)], 2, [], [2]),
    ],
)
def test_get_successor_graph(
    input_edges, starting_node, expected_edges_list, expected_nodes_with_no_edges
):
    input_graph = DummyDiGraph(edges_list=input_edges)
    expected_graph = DummyDiGraph(
        edges_list=expected_edges_list, nodes_list=expected_nodes_with_no_edges
    )
    result = gt.get_successor_graph(input_graph, starting_node)
    assert result == expected_graph


@pytest.mark.parametrize(
    "input_edges, starting_node, expected_nodes",
    [
        ([(0, 1)], 1, [1, 0]),
        ([(0, 1)], 0, [0]),
        ([(0, 1), (1, 2)], 0, [0]),
        ([(0, 1), (1, 2), (1, 3)], 0, [0]),
        ([(0, 1), (1, 2), (1, 3)], 1, [1, 0]),
        ([(0, 1), (1, 2), (1, 3)], 2, [2, 1, 0]),
        ([(0, 1), (1, 2), (1, 3), (2, 3)], 2, [2, 1, 0]),
        ([(0, 1), (1, 2), (1, 3), (2, 4)], 2, [2, 1, 0]),
        ([(0, 1), (1, 2), (1, 3), (4, 5)], 2, [2, 1, 0]),
        ([(0, 1), (1, 2), (1, 3), (4, 5)], 5, [5, 4]),
        ([(0, 1), (1, 2), (1, 3), (2, 4)], 3, [3, 1, 0]),
    ],
)
def test_get_all_predecessor_nodes(input_edges, starting_node, expected_nodes):
    input_graph = DummyDiGraph(edges_list=input_edges)
    result = gt.get_all_predecessor_nodes(input_graph, starting_node)
    assert isinstance(result, set)
    assert set(result) == set(expected_nodes)


@pytest.mark.parametrize(
    "input_edges, starting_node, expected_edges_list, expected_nodes_with_no_edges",
    [
        ([(0, 1)], 1, [(0, 1)], []),
        ([(0, 1)], 0, [], [0]),
        ([(0, 1), (1, 2)], 0, [], [0]),
        ([(0, 1), (1, 2), (1, 3)], 0, [], [0]),
        ([(0, 1), (1, 2), (1, 3)], 1, [(0, 1)], []),
        ([(0, 1), (1, 2), (1, 3)], 2, [(1, 2), (0, 1)], []),
        ([(0, 1), (1, 2), (1, 3), (2, 3)], 2, [(1, 2), (0, 1)], []),
        ([(0, 1), (1, 2), (1, 3), (2, 4)], 2, [(0, 1), (1, 2)], []),
        ([(0, 1), (1, 2), (1, 3), (4, 5)], 2, [(0, 1), (1, 2)], []),
        ([(0, 1), (1, 2), (1, 3), (4, 5)], 5, [(4, 5)], []),
        ([(0, 1), (1, 2), (1, 3), (2, 4)], 3, [(0, 1), (1, 3)], []),
    ],
)
def test_get_predecessor_graph(
    input_edges, starting_node, expected_edges_list, expected_nodes_with_no_edges
):
    input_graph = DummyDiGraph(edges_list=input_edges)
    expected_graph = DummyDiGraph(
        edges_list=expected_edges_list, nodes_list=expected_nodes_with_no_edges
    )
    result = gt.get_predecessor_graph(input_graph, starting_node)
    assert result == expected_graph


@pytest.mark.parametrize(
    "input_edges, expected_a_before_b_tuples",
    [
        ([(0, 1)], [(0, 1)]),
        ([(0, 1), (0, 2)], [(0, 1), (0, 2)]),
        ([(0, 2), (0, 1)], [(0, 1), (0, 2)]),
        ([(0, 1), (1, 2)], [(0, 1), (1, 2), (0, 2)]),
        ([(0, 1), (1, 2), (3, 4)], [(0, 1), (1, 2), (0, 2), (3, 4)]),
        (
            [(0, 1), (1, 2), (3, 4), (1, 3)],
            [(0, 1), (1, 2), (0, 2), (1, 3), (0, 3), (3, 4)],
        ),
    ],
)
def test_get_ordered_objects(input_edges, expected_a_before_b_tuples):
    input_graph = DummyDiGraph(edges_list=input_edges)
    result = gt.get_ordered_objects(input_graph)
    for expected_a_before_b in expected_a_before_b_tuples:
        assert a_before_b(result, expected_a_before_b[0], expected_a_before_b[1])


@pytest.mark.parametrize(
    "input_edges, node_list, expected_edges_list, expected_nodes_with_no_edges",
    [
        ([(0, 1)], [], [], []),
        ([(0, 1)], [1], [], [1]),
        ([(0, 1)], [0], [], [0]),
        ([(0, 1)], [0, 1], [(0, 1)], []),
        ([(0, 1)], [1, 0], [(0, 1)], []),
        ([(0, 1), (1, 2)], [0, 2], [], [0, 2]),
        ([(0, 1), (1, 2)], [1, 2], [(1, 2)], []),
        ([(0, 1), (1, 2), (1, 3)], [0, 1, 2, 3], [(0, 1), (1, 2), (1, 3)], []),
        ([(0, 1), (1, 2), (1, 3)], [0, 1, 3], [(0, 1), (1, 3)], []),
        ([(0, 1), (1, 2), (1, 3), (2, 3)], [0, 2], [], [0, 2]),
    ],
)
def test_filter_graph_given_only(
    input_edges, node_list, expected_edges_list, expected_nodes_with_no_edges
):
    input_graph = DummyDiGraph(edges_list=input_edges)
    expected_graph = DummyDiGraph(
        edges_list=expected_edges_list, nodes_list=expected_nodes_with_no_edges
    )
    result = gt.filter_graph(input_graph, node_list, "given_nodes_only")
    assert result == expected_graph


@pytest.mark.parametrize(
    "input_edges, node_list, expected_edges_list, expected_nodes_with_no_edges",
    [
        ([(0, 1)], [], [], []),
        ([(0, 1)], [1], [(0, 1)], []),
        ([(0, 1)], [0], [], [0]),
        ([(0, 1)], [0, 1], [(0, 1)], []),
        ([(0, 1)], [1, 0], [(0, 1)], []),
        ([(0, 1), (1, 2)], [0, 2], [(0, 1), (1, 2)], []),
        ([(0, 1), (1, 2)], [1, 2], [(0, 1), (1, 2)], []),
        ([(0, 1), (1, 2), (1, 3)], [0, 1, 2, 3], [(0, 1), (1, 2), (1, 3)], []),
        ([(0, 1), (1, 2), (1, 3)], [2], [(0, 1), (1, 2)], []),
        ([(0, 1), (1, 2), (1, 3), (2, 3)], [0, 2], [(0, 1), (1, 2)], []),
        ([(0, 1), (1, 2), (1, 3), (2, 3), (4, 5)], [0, 2], [(0, 1), (1, 2)], []),
        ([(0, 1), (1, 2), (1, 3), (2, 3), (4, 5)], [0, 2, 4], [(0, 1), (1, 2)], [4]),
    ],
)
def test_filter_graph_include_predecessors(
    input_edges, node_list, expected_edges_list, expected_nodes_with_no_edges
):
    input_graph = DummyDiGraph(edges_list=input_edges)
    expected_graph = DummyDiGraph(
        edges_list=expected_edges_list, nodes_list=expected_nodes_with_no_edges
    )
    result = gt.filter_graph(input_graph, node_list, "include_predecessors")
    assert result == expected_graph


@pytest.mark.parametrize(
    "input_edges, node_list, expected_edges_list, expected_nodes_with_no_edges",
    [
        ([(0, 1)], [], [], []),
        ([(0, 1)], [1], [], [1]),
        ([(0, 1)], [0], [(0, 1)], []),
        ([(0, 1)], [0, 1], [(0, 1)], []),
        ([(0, 1)], [1, 0], [(0, 1)], []),
        ([(0, 1), (1, 2)], [0, 1], [(0, 1), (1, 2)], []),
        ([(0, 1), (1, 2)], [1, 2], [(1, 2)], []),
        ([(0, 1), (1, 2), (1, 3)], [0, 1, 2, 3], [(0, 1), (1, 2), (1, 3)], []),
        ([(0, 1), (1, 2), (1, 3)], [2], [], [2]),
        ([(0, 1), (1, 2), (1, 3), (2, 3)], [1, 3], [(1, 2), (1, 3), (2, 3)], []),
        (
            [(0, 1), (1, 2), (1, 3), (2, 3), (4, 5)],
            [1, 3],
            [(1, 2), (1, 3), (2, 3)],
            [],
        ),
        (
            [(0, 1), (1, 2), (1, 3), (2, 3), (4, 5)],
            [1, 3, 4],
            [(1, 2), (1, 3), (2, 3), (4, 5)],
            [],
        ),
    ],
)
def test_filter_graph_include_successors(
    input_edges, node_list, expected_edges_list, expected_nodes_with_no_edges
):
    input_graph = DummyDiGraph(edges_list=input_edges)
    expected_graph = DummyDiGraph(
        edges_list=expected_edges_list, nodes_list=expected_nodes_with_no_edges
    )
    result = gt.filter_graph(input_graph, node_list, "include_successors")
    assert result == expected_graph


@pytest.mark.parametrize(
    "input_edges, node_list, expected_edges_list, expected_nodes_with_no_edges",
    [
        ([(0, 1)], [], [], []),
        ([(0, 1)], [1], [(0, 1)], []),
        ([(0, 1)], [0], [(0, 1)], []),
        ([(0, 1)], [0, 1], [(0, 1)], []),
        ([(0, 1)], [1, 0], [(0, 1)], []),
        ([(0, 1), (1, 2)], [0, 1], [(0, 1), (1, 2)], []),
        ([(0, 1), (1, 2)], [1, 2], [(0, 1), (1, 2)], []),
        ([(0, 1), (1, 2), (1, 3)], [0, 1, 2, 3], [(0, 1), (1, 2), (1, 3)], []),
        ([(0, 1), (1, 2), (1, 3)], [2], [(0, 1), (1, 2)], []),
        ([(0, 1), (1, 2), (1, 3), (2, 3)], [2], [(0, 1), (1, 2), (2, 3)], []),
        ([(0, 1), (1, 2), (1, 3), (4, 5)], [2], [(0, 1), (1, 2)], []),
        ([(0, 1), (1, 2), (1, 3), (3, 4)], [2], [(0, 1), (1, 2)], []),
        (
            [(0, 1), (1, 2), (1, 3), (2, 3)],
            [1, 3],
            [(0, 1), (1, 2), (1, 3), (2, 3)],
            [],
        ),
        (
            [(0, 1), (1, 2), (1, 3), (2, 3), (4, 5)],
            [1, 3],
            [(0, 1), (1, 2), (1, 3), (2, 3)],
            [],
        ),
        (
            [(0, 1), (1, 2), (1, 3), (2, 3), (4, 5)],
            [1, 3, 4],
            [(0, 1), (1, 2), (1, 3), (2, 3), (4, 5)],
            [],
        ),
    ],
)
def test_filter_graph_include_both(
    input_edges, node_list, expected_edges_list, expected_nodes_with_no_edges
):
    input_graph = DummyDiGraph(edges_list=input_edges)
    expected_graph = DummyDiGraph(
        edges_list=expected_edges_list, nodes_list=expected_nodes_with_no_edges
    )
    result = gt.filter_graph(input_graph, node_list, "include_both")
    assert result == expected_graph


def test_filter_graph_produces_error():
    input_graph = DummyDiGraph(edges_list=[(0, 1)])
    node_list = [0, 1]
    expected_error_message = "Given mode [ 'wrong_keyword' ] not supported. Supported modes are 'given_nodes_only', 'include_predecessors', 'include_successors', 'include_both'."
    with pytest.raises(ValueError, match=re.escape(expected_error_message)):
        _ = gt.filter_graph(input_graph, node_list, "wrong_keyword")
