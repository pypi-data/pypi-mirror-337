from unittest.mock import patch

import pytest
from acedeploy.core.model_prepostdeploymentsteps import (
    PreOrPostDeploymenStep,
    PreOrPostDeploymentScriptTarget,
    PreOrPostDeploymentScriptType,
    PreOrPostDeploymentScriptsExecutionOptions,
)


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            """
            INSERT INTO myschema.table VALUES (1, 2, 3);
            INSERT INTO myschema.table2 VALUES (a,b,c);
            """,
            False,
        ),
        (
            """
            CREATE OR REPLACE TABLE sch.tab(id1 INT, id2 INT);
            INSERT INTO sch.tab VALUES (1, 2);
            """,
            False,
        ),
        (
            """
            CREATE OR REPLACE TABLE db.sch.tab(id1 INT, id2 INT);
            INSERT INTO db.sch.tab VALUES (1, 2);
            """,
            True,
        ),  # refernces database in db.sch.tab
        (
            """
            USE WAREHOUSE WH_XL;
            """,
            True,
        ),  # keyworkd USE
        (
            """
            ALTER TABLE myschema.table DROP COLUMN x;
            """,
            False,
        ),
        (
            """
            USE DATABASE DB;
            """,
            True,
        ),  # keyword USE and keyword DATABASE
        (
            """
            -- some commands here
            USE DB;
            -- some more here
            """,  # keyword USE
            True,
        ),
        (
            """
            DROP DATABASE DB;
            """,
            True,
        ),  # keyword DATABASE
        (
            """
            drop DATABASE db;
            """,
            True,
        ),  # keyword DATABASE
        (
            """
            DROP database db;
            """,
            True,
        ),  # keyword DATABASE
        (
            """
            CREATE OR REPLACE PROCEDURE stproc1()
            returns string not null
            language javascript
            as
            $$
            var statement = snowflake.createStatement(...);
            ...
            $$
            ;
            """,
            True,
        ),  # keyword PROCEDURE
        (
            """
            create procedure stproc1()
            returns string not null
            language javascript
            as
            $$
            var statement = snowflake.createStatement(...);
            ...
            $$
            ;
            """,
            True,
        ),  # keyword PROCEDURE
    ],
)
def test_pre_or_postdeployment_contains_forbidden_command(input, expected):
    # arrange
    filter_list = (
        r"\bDATABASE\b",
        r"\bSCHEMA\b",
        r"\bUSE\b",
        r"\bCALL\b",
        r"\bSTAGE\b",
        r"\bGRANT\b",
        r"\bREVOKE\b",
        r"\bPROCEDURE\b",
        r"\b\w+\.\w+\.\w+\b",
    )
    content = input

    # act
    result = PreOrPostDeploymenStep._contains_forbidden_command(content, filter_list)

    # assert
    assert bool(result) == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            """
            CREATE OR REPLACE TABLE sch.tab(t1 VARCHAR(10), t2 VARCHAR(10));
            INSERT INTO sch.tab VALUES ('www.example.com', 'MY_DB.MY_SCHEMA.MYTABLE');
            """,
            False,
        ),
        (
            """
            -- USE DATABASE MY_DB;
            CREATE OR REPLACE TABLE sch.tab(id1 INT, id2 INT);
            INSERT INTO sch.tab VALUES (1, 2);
            """,
            False,
        ),
        (
            """
            /* some comment
            with url www.example.com
            */
            CREATE OR REPLACE TABLE sch.tab(id1 INT, id2 INT);
            INSERT INTO sch.tab VALUES (1, 2);
            """,
            False,
        ),
        (
            """
            // some comment
            // with url www.example.com
            //
            CREATE OR REPLACE TABLE sch.tab(id1 INT, id2 INT);
            INSERT INTO sch.tab VALUES (1, 2);
            """,
            False,
        ),
    ],
)
def test_pre_or_postdeployment_contains_forbidden_command_remove_comments(
    input, expected
):
    # arrange
    filter_list = (
        r"\bDATABASE\b",
        r"\bSCHEMA\b",
        r"\bUSE\b",
        r"\bCALL\b",
        r"\bSTAGE\b",
        r"\bGRANT\b",
        r"\bREVOKE\b",
        r"\b\w+\.\w+\.\w+\b",
    )
    content = input

    # act
    result = PreOrPostDeploymenStep._contains_forbidden_command(content, filter_list)

    # assert
    assert bool(result) == expected


def test_PreOrPostDeploymenStep_init():
    with patch("aceutils.file_util.load") as mock_load:
        mock_load.return_value = "dummy_content"
        pps = PreOrPostDeploymenStep("/path/to/my/file.sql")
    assert pps.git_change_type is None
    assert pps.type == PreOrPostDeploymentScriptType.SQL
    assert pps.content == "dummy_content"
    assert pps.execute_step is None


def test_PreOrPostDeploymenStep_init_error_python_not_allowed():
    with pytest.raises(Exception):
        with patch("aceutils.file_util.load") as mock_load:
            mock_load.return_value = "dummy_content"
            __ = PreOrPostDeploymenStep("/path/to/my/file.py")


def test_PreOrPostDeploymenStep_init_error_unapproved_command():
    filter_list = (r"\bDATABASE\b",)
    with pytest.raises(Exception):
        with patch("aceutils.file_util.load") as mock_load:
            mock_load.return_value = "DROP DATABASE DUMMY;"
            __ = PreOrPostDeploymenStep(
                "/path/to/my/file.sql", regex_filter_list=filter_list
            )


@pytest.mark.parametrize(
    "file_content, string_replace_dict, expected_content",
    [
        (
            """
        ALTER TABLE S.T DROP COLUMN %%var1%%;
        """,
            {"var1": "MY_COL"},
            """
        ALTER TABLE S.T DROP COLUMN MY_COL;
        """,
        ),
        (
            """
        ALTER TABLE S.T DROP COLUMN %%var2%%;
        """,
            {"var1": "MY_COL"},
            """
        ALTER TABLE S.T DROP COLUMN %%var2%%;
        """,
        ),
        (
            """
        ALTER TABLE S.T DROP COLUMN %%var2%% ADD COLUMN %%var1%%;
        """,
            {"var1": "MY_COL", "var2": "MY_COL2"},
            """
        ALTER TABLE S.T DROP COLUMN MY_COL2 ADD COLUMN MY_COL;
        """,
        ),
    ],
)
def test_PreOrPostDeploymenStep_init_string_replace(
    file_content, string_replace_dict, expected_content
):
    with patch("aceutils.file_util.load") as mock_load:
        mock_load.return_value = file_content
        pps = PreOrPostDeploymenStep(
            "/path/to/my/file.sql", string_replace_dict=string_replace_dict
        )
    assert pps.content.strip() == expected_content.strip()


@pytest.mark.parametrize(
    "file_content, expected",
    [
        (
            """
        ALTER TABLE S.T DROP COLUMN X;
        """,
            """
        ALTER TABLE S.T DROP COLUMN X;
        """,
        ),
        (
            """
        ALTER TABLE S.T DROP COLUMN X;
        -- comment
        """,
            """
        ALTER TABLE S.T DROP COLUMN X;
        """,
        ),
        (
            """
        ALTER TABLE S.T DROP COLUMN X; -- comment
        ALTER TABLE S.T DROP COLUMN Y; -- comment
        """,
            """
        ALTER TABLE S.T DROP COLUMN X; -- comment
        ALTER TABLE S.T DROP COLUMN Y;
        """,
        ),
    ],
)
def test_load_sql_file(file_content, expected):
    with patch("aceutils.file_util.load") as mock_load:
        mock_load.return_value = file_content
        result = PreOrPostDeploymenStep._load_sql_file("/dummy/path/file.sql")
    assert result.strip() == expected.strip()


@pytest.mark.parametrize(
    "script_path, expected",
    [
        ("path/to/my/file.SQL", PreOrPostDeploymentScriptType.SQL),
        ("path/to/my/file.sql", PreOrPostDeploymentScriptType.SQL),
        ("path/to/my/file.PY", PreOrPostDeploymentScriptType.PYTHON),
        ("path/to/my/file.py", PreOrPostDeploymentScriptType.PYTHON),
    ],
)
def test_get_type_from_path(script_path, expected):
    result = PreOrPostDeploymentScriptType.get_type_from_path(script_path)
    assert result == expected


@pytest.mark.parametrize(
    "script_path, error_type",
    [
        ("path/to/my/file.txt", NotImplementedError),
        ("", ValueError),
        (None, ValueError),
    ],
)
def test_get_type_from_path_error(script_path, error_type):
    with pytest.raises(error_type):
        __ = PreOrPostDeploymentScriptType.get_type_from_path(script_path)


@pytest.mark.parametrize(
    "target, expected",
    [
        (PreOrPostDeploymentScriptTarget.TARGET, PreOrPostDeploymentScriptTarget.TARGET),
        (PreOrPostDeploymentScriptTarget.META, PreOrPostDeploymentScriptTarget.META),
        (None, None),
    ],
)
def test_set_target(
    target, expected
):
    with patch("aceutils.file_util.load") as mock_load:
        mock_load.return_value = "dummy_content"
        step = PreOrPostDeploymenStep(path="dummy.sql")
    step.set_target(
        target=target,
    )
    assert step.target == expected


@pytest.mark.parametrize(
    "git_change_type, pre_and_postdeployment_execution, step_condition, expected",
    [
        (None, PreOrPostDeploymentScriptsExecutionOptions.NONE, "always", False),
        (None, PreOrPostDeploymentScriptsExecutionOptions.NONE, "onChange", False),
        (None, PreOrPostDeploymentScriptsExecutionOptions.NONE, "never", False),
        (None, PreOrPostDeploymentScriptsExecutionOptions.ALL, "always", True),
        (None, PreOrPostDeploymentScriptsExecutionOptions.GIT, "always", True),
        ("A", PreOrPostDeploymentScriptsExecutionOptions.GIT, "always", True),
        ("R", PreOrPostDeploymentScriptsExecutionOptions.GIT, "always", True),
        ("M", PreOrPostDeploymentScriptsExecutionOptions.GIT, "always", True),
        (None, PreOrPostDeploymentScriptsExecutionOptions.GIT, "onChange", False),
        ("A", PreOrPostDeploymentScriptsExecutionOptions.GIT, "onChange", True),
        ("R", PreOrPostDeploymentScriptsExecutionOptions.GIT, "onChange", True),
        ("M", PreOrPostDeploymentScriptsExecutionOptions.GIT, "onChange", True),
        ("D", PreOrPostDeploymentScriptsExecutionOptions.GIT, "onChange", False),
        (None, PreOrPostDeploymentScriptsExecutionOptions.GIT, "never", False),
        ("A", PreOrPostDeploymentScriptsExecutionOptions.GIT, "never", False),
    ],
)
def test_set_execute_step(
    git_change_type, pre_and_postdeployment_execution, step_condition, expected
):
    with patch("aceutils.file_util.load") as mock_load:
        mock_load.return_value = "dummy_content"
        step = PreOrPostDeploymenStep(path="dummy.sql", git_change_type=git_change_type)
    step.set_execute_step(
        pre_and_postdeployment_execution=pre_and_postdeployment_execution,
        step_condition=step_condition,
    )
    assert step.execute_step == expected


@pytest.mark.parametrize(
    "git_change_type, pre_and_postdeployment_execution, step_condition, error_type",
    [
        (None, PreOrPostDeploymentScriptsExecutionOptions.ALL, "onChange", ValueError),
    ],
)
def test_set_execute_step_error(
    git_change_type, pre_and_postdeployment_execution, step_condition, error_type
):
    with patch("aceutils.file_util.load") as mock_load:
        mock_load.return_value = "dummy_content"
        step = PreOrPostDeploymenStep(path="dummy.sql", git_change_type=git_change_type)
    with pytest.raises(error_type):
        step.set_execute_step(
            pre_and_postdeployment_execution=pre_and_postdeployment_execution,
            step_condition=step_condition,
        )
