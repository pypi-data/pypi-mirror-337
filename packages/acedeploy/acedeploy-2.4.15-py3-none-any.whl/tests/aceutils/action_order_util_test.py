import os

import acedeploy.core.model_object_action_entities as moa
import aceutils.action_order_util as aou
import pytest
from acedeploy.core.model_sql_entities import DbActionType
from acedeploy.services.solution_service import SolutionClient
from acedeploy.services.dependency_parser import DependencyParser


def a_before_b(l, a, b):
    return l.index(a) < l.index(b)


def a_before_b_str_rep(l, a, b):
    return a_before_b([str(e) for e in l], str(a), str(b))


@pytest.fixture
def demo_solution_client_1():
    solution_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "action_order_test_solution", "1")
    )
    solution_client = SolutionClient(solution_path)
    solution_client.load_solution()
    return solution_client


@pytest.fixture
def demo_solution_client_2():
    solution_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "action_order_test_solution", "2")
    )
    solution_client = SolutionClient(solution_path)
    solution_client.load_solution()
    return solution_client


def test_order_action_list_target_deployment_partial_1(demo_solution_client_1):
    # arange
    dependency_client = DependencyParser(demo_solution_client_1)
    dependency_client.build_full_dependency_graph()
    action_dict = {
        "view": moa.ViewAction(
            "VIEWS", "VIEW1", DbActionType.ALTER, file_content="dummy"
        ),
        "task": moa.TaskAction(
            "MISC", "MY_SECOND_TASK", DbActionType.ALTER, file_content="dummy"
        ),
    }
    action_list = [a for a in action_dict.values()]

    # act
    ordered_actions = aou.order_action_list(
        action_list, dependency_client, is_meta_deployment=False
    )

    # assert
    expected_ordered_actions = [
        [],
        [],
        [[action_dict["view"]]],
        [[action_dict["task"]]],
        [],
    ]
    # check if all actions exist at their respective level.
    # do not check if actions within a list are in the correct order.
    ordered_actions_strs = [
        frozenset([frozenset([str(o) for o in l1]) for l1 in l2])
        for l2 in ordered_actions
    ]
    expected_actions_strs = [
        frozenset([frozenset([str(o) for o in l1]) for l1 in l2])
        for l2 in expected_ordered_actions
    ]
    assert ordered_actions_strs == expected_actions_strs


def test_order_action_list_target_deployment_partial_2(demo_solution_client_1):
    # arange
    dependency_client = DependencyParser(demo_solution_client_1)
    dependency_client.build_full_dependency_graph()
    action_dict = {
        "table1": moa.TableAction(
            "DATA", "TABLE1", DbActionType.ALTER, file_content="dummy"
        ),
        "view1": moa.ViewAction(
            "VIEWS", "VIEW1", DbActionType.ALTER, file_content="dummy"
        ),
        "view2": moa.ViewAction(
            "VIEWS", "VIEW2", DbActionType.ALTER, file_content="dummy"
        ),
        "mat_view1": moa.MaterializedViewAction(
            "VIEWS", "MAT_VIEW1", DbActionType.ALTER, file_content="dummy"
        ),
        "fileformat": moa.FileformatAction(
            "MISC", "MY_CSV_FORMAT", DbActionType.ALTER, file_content="dummy"
        ),
        "function": moa.FunctionAction(
            "PROCFUNC", "AREA", DbActionType.ALTER, ["FLOAT"], file_content="dummy"
        ),
        "procedure": moa.ProcedureAction(
            "PROCFUNC", "MYPROC", DbActionType.ALTER, [], file_content="dummy"
        ),
        "stage": moa.StageAction(
            "MISC", "MY_EXTERNAL_STAGE", DbActionType.ALTER, file_content="dummy"
        ),
        "stream": moa.StreamAction(
            "MISC", "MYSTREAM", DbActionType.ALTER, file_content="dummy"
        ),
        "schema_misc": moa.SchemaAction(
            "MISC", "MISC", DbActionType.ADD, file_content="dummy"
        ),
        "drop_table": moa.TableAction("DUMMY", "DROPME", DbActionType.DROP),
        "drop_view": moa.ViewAction("DUMMY", "DROPME", DbActionType.DROP),
        "drop_mat_view": moa.MaterializedViewAction(
            "DUMMY", "DROPME", DbActionType.DROP
        ),
        "drop_fileformat": moa.FileformatAction("DUMMY", "DROPME", DbActionType.DROP),
        "drop_function": moa.FunctionAction("DUMMY", "DROPME", DbActionType.DROP, ""),
        "drop_procedure": moa.ProcedureAction("DUMMY", "DROPME", DbActionType.DROP, ""),
        "drop_stage": moa.StageAction("DUMMY", "DROPME", DbActionType.DROP),
        "drop_stream": moa.StreamAction("DUMMY", "DROPME", DbActionType.DROP),
        "task2": moa.TaskAction(
            "MISC", "MY_SECOND_TASK", DbActionType.ALTER, file_content="dummy"
        ),
        "task1": moa.TaskAction(
            "MISC", "MY_FIRST_TASK", DbActionType.ALTER, file_content="dummy"
        ),
        "pipe": moa.PipeAction(
            "MISC", "MY_PIPE", DbActionType.ALTER, file_content="dummy"
        ),
        "sequence": moa.SequenceAction(
            "MISC", "MY_SEQUENCE", DbActionType.ALTER, file_content="dummy"
        ),
        "maskingpolicy": moa.MaskingPolicyAction(
            "POLICIES", "MY_MASKING_POLICY", DbActionType.ALTER, file_content="dummy"
        ),
        "rowaccesspolicy": moa.RowAccessPolicyAction(
            "POLICIES", "MY_ROW_ACCESS_POLICY", DbActionType.ALTER, file_content="dummy"
        ),
    }
    action_list = [a for a in action_dict.values()]

    # act
    ordered_actions = aou.order_action_list(
        action_list, dependency_client, is_meta_deployment=False
    )

    # assert
    expected_ordered_actions = [
        [[action_dict["schema_misc"]]],
        [],
        [
            [
                action_dict["fileformat"],
                action_dict["stage"],
                action_dict["table1"],
                action_dict["pipe"],
                action_dict["stream"],
                action_dict["view1"],
                action_dict["mat_view1"],
            ],
            [action_dict["procedure"]],
            [action_dict["maskingpolicy"]],
            [action_dict["function"]],
            [action_dict["rowaccesspolicy"]],
            [action_dict["sequence"]],
            [action_dict["view2"]],
        ],
        [[action_dict["task1"], action_dict["task2"]]],
        [
            [action_dict["drop_table"]],
            [action_dict["drop_view"]],
            [action_dict["drop_mat_view"]],
            [action_dict["drop_fileformat"]],
            [action_dict["drop_function"]],
            [action_dict["drop_procedure"]],
            [action_dict["drop_stage"]],
            [action_dict["drop_stream"]],
        ],
    ]

    # check if all actions exist at their respective level.
    # do not check if actions within a list are in the correct order.
    ordered_actions_strs = [
        frozenset([frozenset([str(o) for o in l1]) for l1 in l2])
        for l2 in ordered_actions
    ]
    expected_actions_strs = [
        frozenset([frozenset([str(o) for o in l1]) for l1 in l2])
        for l2 in expected_ordered_actions
    ]
    assert ordered_actions_strs == expected_actions_strs

    # check object order within a list (only where required); compare string representations instead of objects
    # first, get the list which need to be checked: look for any item that we know to be in that list
    l1 = [a for a in ordered_actions[2] if action_dict["fileformat"] in a][0]
    # in that list, we can now check for the required order
    assert a_before_b_str_rep(l1, action_dict["fileformat"], action_dict["stage"])
    assert a_before_b_str_rep(l1, action_dict["stage"], action_dict["pipe"])
    assert a_before_b_str_rep(l1, action_dict["table1"], action_dict["stream"])
    assert a_before_b_str_rep(l1, action_dict["table1"], action_dict["view1"])
    assert a_before_b_str_rep(l1, action_dict["table1"], action_dict["mat_view1"])

    # first, get the list which need to be checked: look for any item that we know to be in that list
    l2 = [a for a in ordered_actions[3] if action_dict["task1"] in a][0]
    # in that list, we can now check for the required order
    assert a_before_b_str_rep(l2, action_dict["task1"], action_dict["task2"])


def test_order_action_list_meta_deployment_partial_1(demo_solution_client_1):
    # arange
    dependency_client = DependencyParser(demo_solution_client_1)
    dependency_client.build_full_dependency_graph()
    action_dict = {
        "view": moa.ViewAction(
            "VIEWS", "VIEW1", DbActionType.ALTER, file_content="dummy"
        ),
        "task": moa.TaskAction(
            "MISC", "MY_SECOND_TASK", DbActionType.ALTER, file_content="dummy"
        ),
    }
    action_list = [a for a in action_dict.values()]

    # act
    ordered_actions = aou.order_action_list(
        action_list, dependency_client, is_meta_deployment=True
    )

    # check object order within a list (only where required); compare string representations instead of objects
    # first, get the list which need to be checked: look for any item that we know to be in that list
    l1 = [a for a in ordered_actions[2] if action_dict["view"] in a][0]
    # in that list, we can now check for the required order
    assert a_before_b_str_rep(
        l1,
        moa.TableAction("DATA", "TABLE1", DbActionType.ALTER, file_content="dummy"),
        action_dict["view"],
    )
    assert a_before_b_str_rep(
        l1,
        action_dict["view"],
        moa.ViewAction("VIEWS", "VIEW3", DbActionType.ALTER, file_content="dummy"),
    )
    # first, get the list which need to be checked: look for any item that we know to be in that list
    l2 = [a for a in ordered_actions[3] if action_dict["task"] in a][0]
    # in that list, we can now check for the required order
    assert a_before_b_str_rep(
        l2,
        moa.TaskAction(
            "MISC", "MY_FIRST_TASK", DbActionType.ALTER, file_content="dummy"
        ),
        action_dict["task"],
    )
    assert a_before_b_str_rep(
        l2,
        action_dict["task"],
        moa.TaskAction(
            "MISC", "MY_THIRD_TASK", DbActionType.ALTER, file_content="dummy"
        ),
    )
    assert a_before_b_str_rep(
        l2,
        moa.TaskAction(
            "MISC", "MY_FIRST_TASK", DbActionType.ALTER, file_content="dummy"
        ),
        moa.TaskAction(
            "MISC", "MY_THIRD_TASK", DbActionType.ALTER, file_content="dummy"
        ),
    )


def test_order_action_list_meta_deployment_partial_2(demo_solution_client_1):
    # arange
    dependency_client = DependencyParser(demo_solution_client_1)
    dependency_client.build_full_dependency_graph()
    action_dict = {
        "table1": moa.TableAction(
            "DATA", "TABLE1", DbActionType.ALTER, file_content="dummy"
        ),
        "view1": moa.ViewAction(
            "VIEWS", "VIEW1", DbActionType.ALTER, file_content="dummy"
        ),
        "view2": moa.ViewAction(
            "VIEWS", "VIEW2", DbActionType.ALTER, file_content="dummy"
        ),
        "mat_view1": moa.MaterializedViewAction(
            "VIEWS", "MAT_VIEW1", DbActionType.ALTER, file_content="dummy"
        ),
        "fileformat": moa.FileformatAction(
            "MISC", "MY_CSV_FORMAT", DbActionType.ALTER, file_content="dummy"
        ),
        "function": moa.FunctionAction(
            "PROCFUNC", "AREA", DbActionType.ALTER, ["FLOAT"], file_content="dummy"
        ),
        "procedure": moa.ProcedureAction(
            "PROCFUNC", "MYPROC", DbActionType.ALTER, [], file_content="dummy"
        ),
        "stage": moa.StageAction(
            "MISC", "MY_EXTERNAL_STAGE", DbActionType.ALTER, file_content="dummy"
        ),
        "stream": moa.StreamAction(
            "MISC", "MYSTREAM", DbActionType.ALTER, file_content="dummy"
        ),
        "schema": moa.SchemaAction(
            "MISC", "MISC", DbActionType.ADD, file_content="dummy"
        ),
        "task2": moa.TaskAction(
            "MISC", "MY_SECOND_TASK", DbActionType.ALTER, file_content="dummy"
        ),
        "pipe": moa.PipeAction(
            "MISC", "MY_PIPE", DbActionType.ALTER, file_content="dummy"
        ),
    }
    action_list = [a for a in action_dict.values()]

    # act
    ordered_actions = aou.order_action_list(
        action_list, dependency_client, is_meta_deployment=True
    )

    # assert
    expected_ordered_actions = [
        [[action_dict["schema"]]],
        [],
        [
            [
                action_dict["fileformat"],
                action_dict["stage"],
                action_dict["view2"],
                action_dict["table1"],
                action_dict["pipe"],
                action_dict["stream"],
                moa.FunctionAction(
                    "PROCFUNC",
                    "SUM_SMALLER_THAN",
                    DbActionType.ALTER,
                    file_content="dummy",
                    parameters=["NUMBER"],
                ),
                moa.ViewAction(
                    "VIEWS", "VIEW4", DbActionType.ALTER, file_content="dummy"
                ),
                action_dict["view1"],
                moa.ViewAction(
                    "VIEWS", "VIEW3", DbActionType.ALTER, file_content="dummy"
                ),
                action_dict["mat_view1"],
            ],
            [action_dict["function"]],
            [action_dict["procedure"]],
        ],
        [
            [
                moa.TaskAction(
                    "MISC", "MY_FIRST_TASK", DbActionType.ALTER, file_content="dummy"
                ),
                action_dict["task2"],
                moa.TaskAction(
                    "MISC", "MY_THIRD_TASK", DbActionType.ALTER, file_content="dummy"
                ),
            ]
        ],
        [],
    ]

    # check if all actions exist at their respective level.
    # do not check if actions within a list are in the correct order.
    ordered_actions_strs = [
        frozenset([frozenset([str(o) for o in l1]) for l1 in l2])
        for l2 in ordered_actions
    ]
    expected_actions_strs = [
        frozenset([frozenset([str(o) for o in l1]) for l1 in l2])
        for l2 in expected_ordered_actions
    ]
    assert ordered_actions_strs == expected_actions_strs

    # check object order within a list (only where required); compare string representations instead of objects
    # first, get the list which need to be checked: look for any item that we know to be in that list
    l1 = [a for a in ordered_actions[2] if action_dict["fileformat"] in a][0]
    # in that list, we can now check for the required order
    assert a_before_b_str_rep(l1, action_dict["fileformat"], action_dict["stage"])
    assert a_before_b_str_rep(l1, action_dict["stage"], action_dict["pipe"])
    assert a_before_b_str_rep(l1, action_dict["table1"], action_dict["stream"])
    assert a_before_b_str_rep(l1, action_dict["table1"], action_dict["view1"])
    assert a_before_b_str_rep(l1, action_dict["table1"], action_dict["mat_view1"])
    assert a_before_b_str_rep(
        l1,
        action_dict["table1"],
        moa.FunctionAction(
            "PROCFUNC",
            "SUM_SMALLER_THAN",
            DbActionType.ALTER,
            file_content="dummy",
            parameters=["NUMBER"],
        ),
    )
    assert a_before_b_str_rep(
        l1,
        action_dict["view1"],
        moa.ViewAction("VIEWS", "VIEW3", DbActionType.ALTER, file_content="dummy"),
    )
    assert a_before_b_str_rep(
        l1,
        action_dict["view2"],
        moa.ViewAction("VIEWS", "VIEW4", DbActionType.ALTER, file_content="dummy"),
    )
    assert a_before_b_str_rep(
        l1,
        moa.FunctionAction(
            "PROCFUNC",
            "SUM_SMALLER_THAN",
            DbActionType.ALTER,
            file_content="dummy",
            parameters=["NUMBER"],
        ),
        moa.ViewAction("VIEWS", "VIEW4", DbActionType.ALTER, file_content="dummy"),
    )

    # first, get the list which need to be checked: look for any item that we know to be in that list
    l2 = [a for a in ordered_actions[3] if action_dict["task2"] in a][0]
    # in that list, we can now check for the required order
    assert a_before_b_str_rep(
        l2,
        moa.TaskAction(
            "MISC", "MY_FIRST_TASK", DbActionType.ALTER, file_content="dummy"
        ),
        action_dict["task2"],
    )
    assert a_before_b_str_rep(
        l2,
        action_dict["task2"],
        moa.TaskAction(
            "MISC", "MY_THIRD_TASK", DbActionType.ALTER, file_content="dummy"
        ),
    )
    assert a_before_b_str_rep(
        l2,
        moa.TaskAction(
            "MISC", "MY_FIRST_TASK", DbActionType.ALTER, file_content="dummy"
        ),
        moa.TaskAction(
            "MISC", "MY_THIRD_TASK", DbActionType.ALTER, file_content="dummy"
        ),
    )


def test_order_action_list_meta_with_more_than_two_types(demo_solution_client_2):
    # this test tests against the following scenario:
    # there was a bug where dependencies were not fully resolved under these conditions:
    # object of type A references object of type B which references object of type C
    # only object of type A was altered in git
    # meta deployment failed, as dependency of B on C was not resolved

    # arange
    dependency_client = DependencyParser(demo_solution_client_2)
    dependency_client.build_full_dependency_graph()
    action_dict = {
        "rap": moa.RowAccessPolicyAction(
            "POLICIES", "MY_ROW_ACCESS_POLICY", DbActionType.ALTER, file_content="dummy"
        )
    }
    action_list = [a for a in action_dict.values()]

    # act
    ordered_actions = aou.order_action_list(
        action_list, dependency_client, is_meta_deployment=True
    )

    assert a_before_b_str_rep(
        ordered_actions[2][0],
        moa.TableAction(
            "POLICIES", "MY_POLICY_TABLE", DbActionType.ALTER, file_content="dummy"
        ),
        moa.ViewAction(
            "POLICIES", "MY_POLICY_VIEW", DbActionType.ALTER, file_content="dummy"
        ),
    )
    assert a_before_b_str_rep(
        ordered_actions[2][0],
        moa.TableAction(
            "POLICIES", "MY_POLICY_TABLE", DbActionType.ALTER, file_content="dummy"
        ),
        action_dict["rap"],
    )
    assert a_before_b_str_rep(
        ordered_actions[2][0],
        moa.ViewAction(
            "POLICIES", "MY_POLICY_VIEW", DbActionType.ALTER, file_content="dummy"
        ),
        action_dict["rap"],
    )
