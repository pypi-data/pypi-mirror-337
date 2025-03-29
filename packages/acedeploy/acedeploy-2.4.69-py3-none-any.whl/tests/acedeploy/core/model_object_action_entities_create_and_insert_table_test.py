from typing import List

import acedeploy.core.model_object_action_entities as oae
import pytest
from unittest.mock import MagicMock

from model_object_action_entities_dummy_classes import DummyColumn

@pytest.mark.parametrize(
    "new_table_name, ddl, expected",
    [
        (
            "MY_SCHEMA.NEW_NAME",
            """CREATE TABLE OLD_NAME (ID INT);""",
            """CREATE TABLE MY_SCHEMA.NEW_NAME (ID INT);""",
        ),
        (
            "MY_SCHEMA.NEW_NAME",
            """create table old_name (id int);""",
            """CREATE TABLE MY_SCHEMA.NEW_NAME (id int);""",
        ),
        (
            "MY_SCHEMA.NEW_NAME",
            """CREATE OR REPLACE TABLE OLD_NAME (ID INT);""",
            """CREATE TABLE MY_SCHEMA.NEW_NAME (ID INT);""",
        ),
        (
            "MY_SCHEMA.NEW_NAME",
            """CREATE OR REPLACE TABLE OLD_NAME (
                    ID INT,
                    OLD_NAME STR
                );""",
            """CREATE TABLE MY_SCHEMA.NEW_NAME (
                    ID INT,
                    OLD_NAME STR
                );""",
        ),
    ]
)
def test__update_table_name(
    new_table_name, ddl, expected
):
    output = oae.TableAction._update_table_name(
        ddl, new_table_name
    )
    assert output == expected


@pytest.mark.parametrize(
    "ddl, expected",
    [
        ( # no policy
            """
            CREATE TABLE MY_SCHEMA.MY_TABLE (
                ID INT
            );
            """,
            """
            CREATE TABLE MY_SCHEMA.MY_TABLE (
                ID INT
            );
            """,
        ),
        ( # one policy
            """
            CREATE TABLE MY_SCHEMA.MY_TABLE (
                ID INT WITH MASKING POLICY MY_DB1.CORE.MP1
            );
            """,
            """
            CREATE TABLE MY_SCHEMA.MY_TABLE (
                ID INT WITH MASKING POLICY CORE.MP1
            );
            """,
        ),
        ( # multiple policies
            """
            CREATE TABLE MY_SCHEMA.MY_TABLE (
                VAL1 INT WITH MASKING POLICY MY_DB1.CORE.MP1,
                VAL2 INT WITH MASKING POLICY MY_DB1.CORE.MP2,
                VAL3 INT WITH MASKING POLICY MY_DB1.CORE.MP3,
                VAL4 INT WITH MASKING POLICY MY_DB1.CORE.MP4,
                VAL5 INT WITH MASKING POLICY MY_DB1.CORE.MP5
            );
            """,
            """
            CREATE TABLE MY_SCHEMA.MY_TABLE (
                VAL1 INT WITH MASKING POLICY CORE.MP1,
                VAL2 INT WITH MASKING POLICY CORE.MP2,
                VAL3 INT WITH MASKING POLICY CORE.MP3,
                VAL4 INT WITH MASKING POLICY CORE.MP4,
                VAL5 INT WITH MASKING POLICY CORE.MP5
            );
            """,
        ),
        ( # database name in comment
            """
            CREATE TABLE MY_SCHEMA.MY_TABLE (
                ID INT WITH MASKING POLICY MY_DB1.CORE.MP1 COMMENT 'this column should have MASKING POLICY MY_DB1.CORE.MP1 applied',
                ID2 INT CORE.MP1 COMMENT 'this column should not have MASKING POLICY MY_DB1.CORE.MP1 applied'
            );
            """,
            """
            CREATE TABLE MY_SCHEMA.MY_TABLE (
                ID INT WITH MASKING POLICY CORE.MP1 COMMENT 'this column should have MASKING POLICY MY_DB1.CORE.MP1 applied',
                ID2 INT CORE.MP1 COMMENT 'this column should not have MASKING POLICY MY_DB1.CORE.MP1 applied'
            );
            """,
        ),
    ]
)
def test__remove_masking_policy_db_references(
    ddl, expected
):
    output = oae.TableAction._remove_masking_policy_db_references(ddl)
    assert output == expected


@pytest.mark.parametrize(
    "ddl, expected",
    [
        ( # no policy
            """
            CREATE TABLE MY_SCHEMA.MY_TABLE (
                ID INT
            );
            """,
            """
            CREATE TABLE MY_SCHEMA.MY_TABLE (
                ID INT
            );
            """,
        ),
        ( # one policy
            """
            CREATE TABLE MY_SCHEMA.MY_TABLE (
                ID INT
            ) WITH ROW ACCESS POLICY MY_DB.CORE.RAP1 ON (C1);
            """,
            """
            CREATE TABLE MY_SCHEMA.MY_TABLE (
                ID INT
            ) WITH ROW ACCESS POLICY CORE.RAP1 ON (C1);
            """,
        ),
        ( # wierd comment
            """
            CREATE TABLE MY_SCHEMA.MY_TABLE (
                ID INT
            ) COMMENT 'this table must use ROW ACCESS POLICY MY_DB.CORE.RAP1' WITH ROW ACCESS POLICY MY_DB.CORE.RAP1 ON (C1);
            """,
            """
            CREATE TABLE MY_SCHEMA.MY_TABLE (
                ID INT
            ) COMMENT 'this table must use ROW ACCESS POLICY MY_DB.CORE.RAP1' WITH ROW ACCESS POLICY CORE.RAP1 ON (C1);
            """,
        ),
    ]
)
def test__remove_row_access_policy_db_references(
    ddl, expected
):
    output = oae.TableAction._remove_row_access_policy_db_references(ddl)
    assert output == expected


@pytest.mark.parametrize(
    "identity_start, identity_increment, mock_minmax_value, line, expected",
    [
        ( # no autoincrement
            None,
            None,
            None,
            "ID INT",
            "ID INT",
        ),
        ( # autoincrement positive
            10,
            1,
            100,
            "ID INT autoincrement start 10 increment 1",
            "ID INT autoincrement start 101 increment 1",
        ),
        ( # autoincrement negative
            1000,
            -1,
            90,
            "ID INT autoincrement start 10 increment -1",
            "ID INT autoincrement start 89 increment -1",
        ),
        ( # no max value (empty column)
            10,
            1,
            None,
            "ID INT autoincrement start 10 increment 1",
            "ID INT autoincrement start 10 increment 1",
        ),
    ]
)
def test__generate_column_autoincrement(
    identity_start, identity_increment, mock_minmax_value, line, expected
):
    def mock_get_minmax_column_value(*args, **kwargs):
        return mock_minmax_value
    oae.TableAction._get_max_column_value = MagicMock(side_effect=mock_get_minmax_column_value)
    oae.TableAction._get_min_column_value = MagicMock(side_effect=mock_get_minmax_column_value)
    snow_client_target = None # not needed due to mocks
    table_name = None # not needed due to mocks
    col = DummyColumn(
        column_name="dummy",
        identity_start=identity_start,
        identity_increment=identity_increment,
    )

    output = oae.TableAction._generate_column_autoincrement(snow_client_target, table_name, col, line)
    assert output == expected


@pytest.mark.parametrize(
    "current_cols, desired_cols, source_table, target_table, expected",
    [
        (
            ["a", "b", "c", "d"],
            ["a", "c", "b", "e"],
            "T_SOURCE",
            "T_TARGET",
            """
            INSERT INTO T_TARGET (
                a, b, c
            ) SELECT
                a, b, c
            FROM
                T_SOURCE
            """,
        ),
    ]
)
def test__generate_insert_statement(
    current_cols, desired_cols, source_table, target_table, expected
):
    output = oae.TableAction._generate_insert_statement(current_cols, desired_cols, source_table, target_table)
    assert output.strip() == expected.strip()