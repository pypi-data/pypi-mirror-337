import acedeploy.core.model_object_action_entities as oae
import pytest
from acedeploy.core.model_instance_objects import (
    InstanceConstraintForeignKey,
    InstanceConstraintPrimaryKey,
    InstanceConstraintUniqueKey,
)
from acedeploy.core.model_sql_entities import DbActionType

from model_object_action_entities_dummy_classes import (
    DummyColumn,
    DummyInstanceTable,
    DummyRowAccessPolicyReference,
    DummyMaskingPolicyReference,
    DummySnowClient,
)


@pytest.mark.parametrize(
    "object_name, schema_name, columns_desired, columns_current, expected_output",
    [
        (
            "mytable",
            "myschema",
            [DummyColumn("col1", ordinal_position=1), DummyColumn("col2", ordinal_position=2)],
            [DummyColumn("col1", ordinal_position=1)],
            (["col2"], [], [], False),
        ),
        (
            "mytable",
            "myschema",
            [DummyColumn("col1", ordinal_position=1)],
            [DummyColumn("col1", ordinal_position=1), DummyColumn("col2", ordinal_position=2)],
            ([], ["col2"], [], False),
        ),
        (
            "mytable",
            "myschema",
            [DummyColumn("col1", is_nullable="YES", ordinal_position=1), DummyColumn("col2", ordinal_position=2)],
            [DummyColumn("col1", is_nullable="NO", ordinal_position=1), DummyColumn("col2", ordinal_position=2)],
            ([], [], ["col1"], False),
        ),
        (
            "mytable",
            "myschema",
            [DummyColumn("col1", ordinal_position=1), DummyColumn("col2", ordinal_position=2)],
            [DummyColumn("col1", ordinal_position=1), DummyColumn("col2", ordinal_position=1)],
            ([], [], [], False),
        ),
        (
            "mytable",
            "myschema",
            [DummyColumn("col1", ordinal_position=1), DummyColumn("col2", ordinal_position=2)],
            [DummyColumn("col2", ordinal_position=1)],
            (["col1"], [], [], True),
        ),
        (
            "mytable",
            "myschema",
            [DummyColumn("col1", ordinal_position=1), DummyColumn("col2", ordinal_position=2), DummyColumn("col3", ordinal_position=3)],
            [DummyColumn("col1", ordinal_position=1), DummyColumn("col3", ordinal_position=2)],
            (["col2"], [], [], True),
        ),
    ],
)
def test_get_column_diff(
    object_name, schema_name, columns_desired, columns_current, expected_output
):
    # arrange
    table_alter_object = oae.TableAction(
        object_name,
        schema_name,
        DbActionType.ALTER,
        DummyInstanceTable(columns_current, ""),
        DummyInstanceTable(columns_desired, ""),
        "",
    )

    # act
    output = table_alter_object._get_column_diff()

    # assert
    assert output == expected_output


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")], None
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1"), DummyColumn(column_name="col2")],
                    None,
                ),
            ),
            "ALTER TABLE MYSCHEMA.MYTABLE DROP COLUMN col2",
        ),
        (
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")], None
                ),
                current_instance=DummyInstanceTable(
                    [
                        DummyColumn(column_name="col1"),
                        DummyColumn(column_name="col2"),
                        DummyColumn(column_name="col3"),
                    ],
                    None,
                ),
            ),
            "ALTER TABLE MYSCHEMA.MYTABLE DROP COLUMN col2; ALTER TABLE MYSCHEMA.MYTABLE DROP COLUMN col3",
        ),
        (
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [
                        DummyColumn(
                            "col1",
                            data_type="NUMBER",
                            numeric_precision=10,
                            numeric_scale=4,
                        )
                    ],
                    None,
                ),
                current_instance=DummyInstanceTable(
                    [
                        DummyColumn(
                            "col1",
                            data_type="NUMBER",
                            numeric_precision=20,
                            numeric_scale=4,
                        )
                    ],
                    None,
                ),
            ),
            "ALTER TABLE MYSCHEMA.MYTABLE ALTER col1 SET DATA TYPE NUMBER(10,4)",
        ),
    ],
)
def test_table_generate_alter_statement_columns(input, expected):
    result = input._generate_alter_statement(None)
    assert result == expected


@pytest.mark.parametrize(
    "input, get_ddl_mock, expected",
    [
        (
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [
                        DummyColumn(
                            "col1",
                            data_type="NUMBER",
                            numeric_precision=10,
                            numeric_scale=4,
                        ),
                        DummyColumn(
                            "col2",
                            data_type="NUMBER",
                            numeric_precision=10,
                            numeric_scale=4,
                        ),
                    ]
                ),
                current_instance=DummyInstanceTable(
                    [
                        DummyColumn(
                            "col1",
                            data_type="NUMBER",
                            numeric_precision=20,
                            numeric_scale=4,
                        )
                    ]
                ),
            ),
            [
                {
                    "COL_DEF": "create or replace TABLE MYTABLE (\n    COL1 NUMBER(10,4),\n    COL2 NUMBER(10,4)\n);"
                }
            ],
            "ALTER TABLE MYSCHEMA.MYTABLE ADD COLUMN COL2 NUMBER(10,4); ALTER TABLE MYSCHEMA.MYTABLE ALTER col1 SET DATA TYPE NUMBER(10,4)",
        )
    ],
)
def test_table_generate_alter_statement_add_columns(input, get_ddl_mock, expected):
    mock_snow_client = DummySnowClient(get_ddl_mock)
    result = input._generate_alter_statement(mock_snow_client)
    assert result == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="A"), DummyColumn(column_name="B")],
                    "LINEAR(A,B)",
                    constraints_foreign_key=[
                        InstanceConstraintForeignKey(
                            [
                                {
                                    "fk_schema_name": "myschema",
                                    "fk_table_name": "mytable",
                                    "fk_name": "SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff9959",
                                    "pk_schema_name": "myschema2",
                                    "pk_table_name": "mytable2",
                                    "pk_name": "MY_CONSTRAINT_2",
                                    "comment": None,
                                    "key_sequence": 1,
                                    "fk_column_name": "A",
                                    "pk_column_name": "X",
                                },
                                {
                                    "fk_schema_name": "myschema",
                                    "fk_table_name": "mytable",
                                    "fk_name": "SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff9959",
                                    "pk_schema_name": "myschema2",
                                    "pk_table_name": "mytable2",
                                    "pk_name": "MY_CONSTRAINT_2",
                                    "comment": None,
                                    "key_sequence": 2,
                                    "fk_column_name": "B",
                                    "pk_column_name": "Y",
                                },
                            ]
                        )
                    ],
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="A"), DummyColumn(column_name="B")],
                    "LINEAR(A,B)",
                    constraints_foreign_key=[
                        InstanceConstraintForeignKey(
                            [
                                {
                                    "fk_schema_name": "myschema",
                                    "fk_table_name": "mytable",
                                    "fk_name": "SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff9959",
                                    "pk_schema_name": "myschema2",
                                    "pk_table_name": "mytable2",
                                    "pk_name": "MY_CONSTRAINT_2",
                                    "comment": None,
                                    "key_sequence": 1,
                                    "fk_column_name": "A",
                                    "pk_column_name": "X",
                                },
                                {
                                    "fk_schema_name": "myschema",
                                    "fk_table_name": "mytable",
                                    "fk_name": "SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff9959",
                                    "pk_schema_name": "myschema2",
                                    "pk_table_name": "mytable2",
                                    "pk_name": "MY_CONSTRAINT_2",
                                    "comment": None,
                                    "key_sequence": 2,
                                    "fk_column_name": "B",
                                    "pk_column_name": "Y",
                                },
                            ]
                        )
                    ],
                ),
            ),
            "",
        )
    ],
)
def test_table_generate_alter_statement_no_action_required(input, expected):
    result = input._generate_alter_statement(None)
    assert result == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")], "LINEAR(X,Y)"
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")], "LINEAR(A,B)"
                ),
            ),
            "ALTER TABLE MYSCHEMA.MYTABLE CLUSTER BY (X,Y)",
        ),
        (
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")], None
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")], "LINEAR(A,B)"
                ),
            ),
            "ALTER TABLE MYSCHEMA.MYTABLE DROP CLUSTERING KEY",
        ),
    ],
)
def test_table_generate_alter_statement_clustering_keys(input, expected):
    result = input._generate_alter_statement(None)
    assert result == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    retention_time=90,
                    schema_retention_time=90,
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    retention_time=90,
                    schema_retention_time=90,
                ),
            ),
            "",
        ),
        (
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    retention_time=1,
                    schema_retention_time=90,
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    retention_time=90,
                    schema_retention_time=90,
                ),
            ),
            "ALTER TABLE MYSCHEMA.MYTABLE SET DATA_RETENTION_TIME_IN_DAYS = 1",
        ),
        (
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    retention_time=90,
                    schema_retention_time=1,
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    retention_time=90,
                    schema_retention_time=90,
                ),
            ),
            "ALTER TABLE MYSCHEMA.MYTABLE SET DATA_RETENTION_TIME_IN_DAYS = 90",
        ),
        (
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    retention_time=90,
                    schema_retention_time=90,
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    retention_time=90,
                    schema_retention_time=1,
                ),
            ),
            "ALTER TABLE MYSCHEMA.MYTABLE UNSET DATA_RETENTION_TIME_IN_DAYS",
        ),
        (
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    retention_time=90,
                    schema_retention_time=90,
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    retention_time=1,
                    schema_retention_time=90,
                ),
            ),
            "ALTER TABLE MYSCHEMA.MYTABLE UNSET DATA_RETENTION_TIME_IN_DAYS",
        ),
        (
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    retention_time=1,
                    schema_retention_time=90,
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    retention_time=1,
                    schema_retention_time=90,
                ),
            ),
            "",
        ),
    ],
)
def test_table_generate_alter_statement_retention_time(input, expected):
    result = input._generate_alter_statement(None)
    assert result == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")], comment="new comment"
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")], comment=None
                ),
            ),
            "ALTER TABLE MYSCHEMA.MYTABLE SET COMMENT = 'new comment'",
        )
    ],
)
def test_table_generate_alter_statement_comment(input, expected):
    result = input._generate_alter_statement(None)
    assert result == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="A"), DummyColumn(column_name="B")],
                    constraints_foreign_key=[
                        InstanceConstraintForeignKey(
                            [
                                {
                                    "fk_schema_name": "myschema",
                                    "fk_table_name": "mytable",
                                    "fk_name": "SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff9959",
                                    "pk_schema_name": "myschema2",
                                    "pk_table_name": "mytable2",
                                    "pk_name": "MY_CONSTRAINT_2",
                                    "comment": None,
                                    "key_sequence": 1,
                                    "fk_column_name": "A",
                                    "pk_column_name": "X",
                                },
                                {
                                    "fk_schema_name": "myschema",
                                    "fk_table_name": "mytable",
                                    "fk_name": "SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff9959",
                                    "pk_schema_name": "myschema2",
                                    "pk_table_name": "mytable2",
                                    "pk_name": "MY_CONSTRAINT_2",
                                    "comment": None,
                                    "key_sequence": 2,
                                    "fk_column_name": "B",
                                    "pk_column_name": "Y",
                                },
                            ]
                        )
                    ],
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="A"), DummyColumn(column_name="B")]
                ),
            ),
            "ALTER TABLE MYSCHEMA.MYTABLE ADD  FOREIGN KEY (A, B) REFERENCES myschema2.mytable2 (X, Y) ",
        ),
        (
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="A"), DummyColumn(column_name="B")]
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="A"), DummyColumn(column_name="B")],
                    constraints_foreign_key=[
                        InstanceConstraintForeignKey(
                            [
                                {
                                    "fk_schema_name": "myschema",
                                    "fk_table_name": "mytable",
                                    "fk_name": "SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff9959",
                                    "pk_schema_name": "myschema2",
                                    "pk_table_name": "mytable2",
                                    "pk_name": "MY_CONSTRAINT_2",
                                    "comment": None,
                                    "key_sequence": 1,
                                    "fk_column_name": "A",
                                    "pk_column_name": "X",
                                },
                                {
                                    "fk_schema_name": "myschema",
                                    "fk_table_name": "mytable",
                                    "fk_name": "SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff9959",
                                    "pk_schema_name": "myschema2",
                                    "pk_table_name": "mytable2",
                                    "pk_name": "MY_CONSTRAINT_2",
                                    "comment": None,
                                    "key_sequence": 2,
                                    "fk_column_name": "B",
                                    "pk_column_name": "Y",
                                },
                            ]
                        )
                    ],
                ),
            ),
            "ALTER TABLE MYSCHEMA.MYTABLE DROP FOREIGN KEY (A, B)",
        ),
    ],
)
def test_table_generate_alter_statement_constraint_foreign_key(input, expected):
    result = input._generate_alter_statement(None)
    assert result == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            oae.TableAction(
                schema="MY_SCHEMA",
                name="MY_TABLE",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="A"), DummyColumn(column_name="B")],
                    constraints_primary_key=[
                        InstanceConstraintPrimaryKey(
                            [
                                {
                                    "schema_name": "MY_SCHEMA",
                                    "table_name": "MY_TABLE",
                                    "constraint_name": "MY_CONSTRAINT",
                                    "comment": None,
                                    "key_sequence": 1,
                                    "column_name": "A",
                                },
                                {
                                    "schema_name": "MY_SCHEMA",
                                    "table_name": "MY_TABLE",
                                    "constraint_name": "MY_CONSTRAINT",
                                    "comment": None,
                                    "key_sequence": 2,
                                    "column_name": "B",
                                },
                            ]
                        )
                    ],
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="A"), DummyColumn(column_name="B")]
                ),
            ),
            "ALTER TABLE MY_SCHEMA.MY_TABLE ADD CONSTRAINT MY_CONSTRAINT PRIMARY KEY (A, B) ",
        ),
        (
            oae.TableAction(
                schema="MY_SCHEMA",
                name="MY_TABLE",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="A"), DummyColumn(column_name="B")]
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="A"), DummyColumn(column_name="B")],
                    constraints_primary_key=[
                        InstanceConstraintPrimaryKey(
                            [
                                {
                                    "schema_name": "MY_SCHEMA",
                                    "table_name": "MY_TABLE",
                                    "constraint_name": "MY_CONSTRAINT",
                                    "comment": None,
                                    "key_sequence": 1,
                                    "column_name": "A",
                                },
                                {
                                    "schema_name": "MY_SCHEMA",
                                    "table_name": "MY_TABLE",
                                    "constraint_name": "MY_CONSTRAINT",
                                    "comment": None,
                                    "key_sequence": 2,
                                    "column_name": "B",
                                },
                            ]
                        )
                    ],
                ),
            ),
            "ALTER TABLE MY_SCHEMA.MY_TABLE DROP PRIMARY KEY",
        ),
    ],
)
def test_table_generate_alter_statement_constraint_primary_key(input, expected):
    result = input._generate_alter_statement(None)
    assert result == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            oae.TableAction(
                schema="MY_SCHEMA",
                name="MY_TABLE",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="A"), DummyColumn(column_name="B")],
                    constraints_unique_key=[
                        InstanceConstraintUniqueKey(
                            [
                                {
                                    "schema_name": "MY_SCHEMA",
                                    "table_name": "MY_TABLE",
                                    "constraint_name": "MY_CONSTRAINT",
                                    "comment": None,
                                    "key_sequence": 1,
                                    "column_name": "A",
                                },
                                {
                                    "schema_name": "MY_SCHEMA",
                                    "table_name": "MY_TABLE",
                                    "constraint_name": "MY_CONSTRAINT",
                                    "comment": None,
                                    "key_sequence": 2,
                                    "column_name": "B",
                                },
                            ]
                        )
                    ],
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="A"), DummyColumn(column_name="B")]
                ),
            ),
            "ALTER TABLE MY_SCHEMA.MY_TABLE ADD CONSTRAINT MY_CONSTRAINT UNIQUE (A, B) ",
        ),
        (
            oae.TableAction(
                schema="MY_SCHEMA",
                name="MY_TABLE",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="A"), DummyColumn(column_name="B")]
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="A"), DummyColumn(column_name="B")],
                    constraints_unique_key=[
                        InstanceConstraintUniqueKey(
                            [
                                {
                                    "schema_name": "MY_SCHEMA",
                                    "table_name": "MY_TABLE",
                                    "constraint_name": "MY_CONSTRAINT",
                                    "comment": None,
                                    "key_sequence": 1,
                                    "column_name": "A",
                                },
                                {
                                    "schema_name": "MY_SCHEMA",
                                    "table_name": "MY_TABLE",
                                    "constraint_name": "MY_CONSTRAINT",
                                    "comment": None,
                                    "key_sequence": 2,
                                    "column_name": "B",
                                },
                            ]
                        )
                    ],
                ),
            ),
            "ALTER TABLE MY_SCHEMA.MY_TABLE DROP UNIQUE (A, B)",
        ),
    ],
)
def test_table_generate_alter_statement_constraint_unique_key(input, expected):
    result = input._generate_alter_statement(None)
    assert result == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            oae.TableAction(
                schema="MY_SCHEMA",
                name="MY_TABLE",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable([DummyColumn(column_name="A")]),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="A"), DummyColumn(column_name="B")],
                    constraints_primary_key=[
                        InstanceConstraintPrimaryKey(
                            [
                                {
                                    "schema_name": "MY_SCHEMA",
                                    "table_name": "MY_TABLE",
                                    "constraint_name": "MY_CONSTRAINT",
                                    "comment": None,
                                    "key_sequence": 1,
                                    "column_name": "A",
                                },
                                {
                                    "schema_name": "MY_SCHEMA",
                                    "table_name": "MY_TABLE",
                                    "constraint_name": "MY_CONSTRAINT",
                                    "comment": None,
                                    "key_sequence": 2,
                                    "column_name": "B",
                                },
                            ]
                        )
                    ],
                ),
            ),
            "ALTER TABLE MY_SCHEMA.MY_TABLE DROP PRIMARY KEY; ALTER TABLE MY_SCHEMA.MY_TABLE DROP COLUMN b",
        ),
        (
            oae.TableAction(
                schema="MY_SCHEMA",
                name="MY_TABLE",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="A")],
                    constraints_primary_key=[
                        InstanceConstraintPrimaryKey(
                            [
                                {
                                    "schema_name": "MY_SCHEMA",
                                    "table_name": "MY_TABLE",
                                    "constraint_name": "MY_CONSTRAINT",
                                    "comment": None,
                                    "key_sequence": 1,
                                    "column_name": "A",
                                }
                            ]
                        )
                    ],
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="A"), DummyColumn(column_name="B")],
                    constraints_primary_key=[
                        InstanceConstraintPrimaryKey(
                            [
                                {
                                    "schema_name": "MY_SCHEMA",
                                    "table_name": "MY_TABLE",
                                    "constraint_name": "MY_CONSTRAINT",
                                    "comment": None,
                                    "key_sequence": 1,
                                    "column_name": "A",
                                },
                                {
                                    "schema_name": "MY_SCHEMA",
                                    "table_name": "MY_TABLE",
                                    "constraint_name": "MY_CONSTRAINT",
                                    "comment": None,
                                    "key_sequence": 2,
                                    "column_name": "B",
                                },
                            ]
                        )
                    ],
                ),
            ),
            "ALTER TABLE MY_SCHEMA.MY_TABLE DROP PRIMARY KEY; ALTER TABLE MY_SCHEMA.MY_TABLE DROP COLUMN b; ALTER TABLE MY_SCHEMA.MY_TABLE ADD CONSTRAINT MY_CONSTRAINT PRIMARY KEY (A) ",
        ),
        (
            oae.TableAction(
                schema="MY_SCHEMA",
                name="MY_TABLE",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable([DummyColumn(column_name="A")]),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="A"), DummyColumn(column_name="B")],
                    constraints_unique_key=[
                        InstanceConstraintUniqueKey(
                            [
                                {
                                    "schema_name": "MY_SCHEMA",
                                    "table_name": "MY_TABLE",
                                    "constraint_name": "MY_CONSTRAINT",
                                    "comment": None,
                                    "key_sequence": 1,
                                    "column_name": "A",
                                },
                                {
                                    "schema_name": "MY_SCHEMA",
                                    "table_name": "MY_TABLE",
                                    "constraint_name": "MY_CONSTRAINT",
                                    "comment": None,
                                    "key_sequence": 2,
                                    "column_name": "B",
                                },
                            ]
                        )
                    ],
                ),
            ),
            "ALTER TABLE MY_SCHEMA.MY_TABLE DROP UNIQUE (A, B); ALTER TABLE MY_SCHEMA.MY_TABLE DROP COLUMN b",
        ),
    ],
)
def test_table_generate_alter_statement_drop_constraints_before_columns(
    input, expected
):
    """
    Constraints must be dropped before columns. Otherwise, the constraint might already be dropped
    because the column it references no longer exists, which would cause an error.
    """
    result = input._generate_alter_statement(None)
    assert result == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    row_access_policy_references=[DummyRowAccessPolicyReference()],
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    row_access_policy_references=[DummyRowAccessPolicyReference()],
                ),
            ),
            "",
        ),
        (
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    row_access_policy_references=[],
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    row_access_policy_references=[DummyRowAccessPolicyReference()],
                ),
            ),
            "ALTER TABLE MYSCHEMA.MYTABLE DROP ALL ROW ACCESS POLICIES",
        ),
        (
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    row_access_policy_references=[DummyRowAccessPolicyReference()],
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    row_access_policy_references=[],
                ),
            ),
            "ALTER TABLE MYSCHEMA.MYTABLE DROP ALL ROW ACCESS POLICIES; ALTER TABLE MYSCHEMA.MYTABLE ADD ROW ACCESS POLICY myschema.myrap ON (A,B)",
        ),
        (
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    row_access_policy_references=[DummyRowAccessPolicyReference(ref_arg_column_names='["X", "Y"]')],
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    row_access_policy_references=[DummyRowAccessPolicyReference(ref_arg_column_names='["A"]')],
                ),
            ),
            "ALTER TABLE MYSCHEMA.MYTABLE DROP ALL ROW ACCESS POLICIES; ALTER TABLE MYSCHEMA.MYTABLE ADD ROW ACCESS POLICY myschema.myrap ON (X,Y)",
        ),
        (
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    row_access_policy_references=[DummyRowAccessPolicyReference(policy_name="pol2")],
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    row_access_policy_references=[DummyRowAccessPolicyReference(policy_name="pol1")],
                ),
            ),
            "ALTER TABLE MYSCHEMA.MYTABLE DROP ALL ROW ACCESS POLICIES; ALTER TABLE MYSCHEMA.MYTABLE ADD ROW ACCESS POLICY myschema.pol2 ON (A,B)",
        ),
    ],
)
def test_table_generate_alter_statement_row_access_policy(input, expected):
    result = input._generate_alter_statement(None)
    assert result == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        ( # no change
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    masking_policy_references=[DummyMaskingPolicyReference(ref_column_name="col1")],
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1")],
                    masking_policy_references=[DummyMaskingPolicyReference(ref_column_name="col1")],
                ),
            ),
            "",
        ),
        ( # remove masking policy from column
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1"), DummyColumn(column_name="col2")],
                    masking_policy_references=[],
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1"), DummyColumn(column_name="col2")],
                    masking_policy_references=[DummyMaskingPolicyReference(ref_column_name="col2")],
                ),
            ),
            "ALTER TABLE MYSCHEMA.MYTABLE ALTER COLUMN col1 UNSET MASKING POLICY; ALTER TABLE MYSCHEMA.MYTABLE ALTER COLUMN col2 UNSET MASKING POLICY",
        ),
        ( # add masking policy to column
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1"), DummyColumn(column_name="col2")],
                    masking_policy_references=[DummyMaskingPolicyReference(ref_column_name="col2")],
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1"), DummyColumn(column_name="col2")],
                    masking_policy_references=[],
                ),
            ),
            "ALTER TABLE MYSCHEMA.MYTABLE ALTER COLUMN col1 UNSET MASKING POLICY; ALTER TABLE MYSCHEMA.MYTABLE ALTER COLUMN col2 UNSET MASKING POLICY; ALTER TABLE MYSCHEMA.MYTABLE ALTER COLUMN col2 SET MASKING POLICY myschema.mymp  FORCE",
        ),
        ( # move masking policy from one column to another column
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1"), DummyColumn(column_name="col2")],
                    masking_policy_references=[DummyMaskingPolicyReference(ref_column_name="col1")],
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1"), DummyColumn(column_name="col2")],
                    masking_policy_references=[DummyMaskingPolicyReference(ref_column_name="col2")],
                ),
            ),
            "ALTER TABLE MYSCHEMA.MYTABLE ALTER COLUMN col1 UNSET MASKING POLICY; ALTER TABLE MYSCHEMA.MYTABLE ALTER COLUMN col2 UNSET MASKING POLICY; ALTER TABLE MYSCHEMA.MYTABLE ALTER COLUMN col1 SET MASKING POLICY myschema.mymp  FORCE",
        ),
    ],
)
def test_table_generate_alter_statement_masking_policy(input, expected):
    result = input._generate_alter_statement(None)
    assert result == expected



@pytest.mark.parametrize(
    "input, expected",
    [
        ( # no change
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1"), DummyColumn(column_name="col2"), DummyColumn(column_name="col3")],
                    masking_policy_references=[DummyMaskingPolicyReference(ref_column_name="col1", ref_arg_column_names='["col2, col3"]')],
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1"), DummyColumn(column_name="col2"), DummyColumn(column_name="col3")],
                    masking_policy_references=[DummyMaskingPolicyReference(ref_column_name="col1", ref_arg_column_names='["col2, col3"]')],
                ),
            ),
            "",
        ),
        ( # remove policy from column
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1"), DummyColumn(column_name="col2"), DummyColumn(column_name="col3")],
                    masking_policy_references=[],
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1"), DummyColumn(column_name="col2"), DummyColumn(column_name="col3")],
                    masking_policy_references=[DummyMaskingPolicyReference(ref_column_name="col1", ref_arg_column_names='["col2, col3"]')],
                ),
            ),
            "ALTER TABLE MYSCHEMA.MYTABLE ALTER COLUMN col1 UNSET MASKING POLICY; ALTER TABLE MYSCHEMA.MYTABLE ALTER COLUMN col2 UNSET MASKING POLICY; ALTER TABLE MYSCHEMA.MYTABLE ALTER COLUMN col3 UNSET MASKING POLICY",
        ),
        ( # add policy to column
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1"), DummyColumn(column_name="col2"), DummyColumn(column_name="col3")],
                    masking_policy_references=[DummyMaskingPolicyReference(ref_column_name="col1", ref_arg_column_names='["col2", "col3"]')],
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1"), DummyColumn(column_name="col2"), DummyColumn(column_name="col3")],
                    masking_policy_references=[],
                ),
            ),
            "ALTER TABLE MYSCHEMA.MYTABLE ALTER COLUMN col1 UNSET MASKING POLICY; ALTER TABLE MYSCHEMA.MYTABLE ALTER COLUMN col2 UNSET MASKING POLICY; ALTER TABLE MYSCHEMA.MYTABLE ALTER COLUMN col3 UNSET MASKING POLICY; ALTER TABLE MYSCHEMA.MYTABLE ALTER COLUMN col1 SET MASKING POLICY myschema.mymp USING (col1,col2,col3) FORCE",
        ),
        ( # move policy from one column to another column
            oae.TableAction(
                schema="myschema",
                name="mytable",
                action=DbActionType.ALTER,
                file_content="",
                desired_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1"), DummyColumn(column_name="col2"), DummyColumn(column_name="col3")],
                    masking_policy_references=[DummyMaskingPolicyReference(ref_column_name="col3", ref_arg_column_names='["col1", "col2"]')],
                ),
                current_instance=DummyInstanceTable(
                    [DummyColumn(column_name="col1"), DummyColumn(column_name="col2"), DummyColumn(column_name="col3")],
                    masking_policy_references=[DummyMaskingPolicyReference(ref_column_name="col1", ref_arg_column_names='["col2", "col3"]')],
                ),
            ),
            "ALTER TABLE MYSCHEMA.MYTABLE ALTER COLUMN col1 UNSET MASKING POLICY; ALTER TABLE MYSCHEMA.MYTABLE ALTER COLUMN col2 UNSET MASKING POLICY; ALTER TABLE MYSCHEMA.MYTABLE ALTER COLUMN col3 UNSET MASKING POLICY; ALTER TABLE MYSCHEMA.MYTABLE ALTER COLUMN col3 SET MASKING POLICY myschema.mymp USING (col3,col1,col2) FORCE",
        ),
    ],
)
def test_table_generate_alter_statement_masking_policy_conditional(input, expected):
    result = input._generate_alter_statement(None)
    assert result == expected



# endregion table alter
