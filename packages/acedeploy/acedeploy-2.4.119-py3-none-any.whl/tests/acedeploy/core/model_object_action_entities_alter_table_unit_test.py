from typing import List

import acedeploy.core.model_object_action_entities as oae
import pytest
from acedeploy.core.model_instance_objects import (
    ConstraintColumn,
    ConstraintColumnForeignKey,
    InstanceConstraintForeignKey,
    InstanceConstraintPrimaryKey,
    RowAccessPolicyReference,
    MaskingPolicyReference,
)
from acedeploy.core.model_sql_entities import DbActionType, DbObjectType

from model_object_action_entities_dummy_classes import DummyColumn, DummySnowClient

# region columns


@pytest.mark.parametrize(
    "table_name, column_current, column_desired, expected_output",
    [
        (
            "my_table",
            DummyColumn("col1", comment="comment1"),
            DummyColumn("col1", comment="comment2"),
            ["ALTER TABLE my_table ALTER col1 COMMENT 'comment2'"],
        ),
        (
            "my_table",
            DummyColumn("col1", is_nullable="YES"),
            DummyColumn("col1", is_nullable="NO"),
            ["ALTER TABLE my_table ALTER col1 SET NOT NULL"],
        ),
        (
            "my_table",
            DummyColumn("col1", is_nullable="NO"),
            DummyColumn("col1", is_nullable="YES"),
            ["ALTER TABLE my_table ALTER col1 DROP NOT NULL"],
        ),
        (
            "my_table",
            DummyColumn("col1", column_default="my_default"),
            DummyColumn("col1"),
            ["ALTER TABLE my_table ALTER col1 DROP DEFAULT"],
        ),
        (
            "my_table",
            DummyColumn("col1", column_default=100),
            DummyColumn("col1"),
            ["ALTER TABLE my_table ALTER col1 DROP DEFAULT"],
        ),
        (
            "my_table",
            DummyColumn("col1", data_type="TEXT", character_maximum_length=10),
            DummyColumn("col1", data_type="TEXT", character_maximum_length=20),
            ["ALTER TABLE my_table ALTER col1 SET DATA TYPE VARCHAR(20)"],
        ),
        (
            "my_table",
            DummyColumn(
                "col1",
                data_type="TEXT",
                character_maximum_length=10,
                collation_name="en-ci",
            ),
            DummyColumn(
                "col1",
                data_type="TEXT",
                character_maximum_length=20,
                collation_name="en-ci",
            ),
            [
                "ALTER TABLE my_table ALTER col1 SET DATA TYPE VARCHAR(20) COLLATE 'en-ci'"
            ],
        ),
        (
            "my_table",
            DummyColumn(
                "col1", data_type="NUMBER", numeric_precision=10, numeric_scale=0
            ),
            DummyColumn(
                "col1", data_type="NUMBER", numeric_precision=20, numeric_scale=0
            ),
            ["ALTER TABLE my_table ALTER col1 SET DATA TYPE NUMBER(20,0)"],
        ),
        (
            "my_table",
            DummyColumn(
                "col1", data_type="NUMBER", numeric_precision=20, numeric_scale=0
            ),
            DummyColumn(
                "col1", data_type="NUMBER", numeric_precision=10, numeric_scale=0
            ),
            ["ALTER TABLE my_table ALTER col1 SET DATA TYPE NUMBER(10,0)"],
        ),
        (
            "my_table",
            DummyColumn(
                "col1", data_type="NUMBER", numeric_precision=10, numeric_scale=4
            ),
            DummyColumn(
                "col1", data_type="NUMBER", numeric_precision=20, numeric_scale=4
            ),
            ["ALTER TABLE my_table ALTER col1 SET DATA TYPE NUMBER(20,4)"],
        ),
        (
            "my_table",
            DummyColumn(
                "col1", data_type="NUMBER", numeric_precision=20, numeric_scale=4
            ),
            DummyColumn(
                "col1", data_type="NUMBER", numeric_precision=10, numeric_scale=4
            ),
            ["ALTER TABLE my_table ALTER col1 SET DATA TYPE NUMBER(10,4)"],
        ),
        (
            "my_table",
            DummyColumn("col1", column_default="SCHEMA.MY_SEQUENCE1.NEXTVAL"),
            DummyColumn("col1", column_default="SCHEMA.MY_SEQUENCE2.NEXTVAL"),
            ["ALTER TABLE my_table ALTER col1 SET DEFAULT SCHEMA.MY_SEQUENCE2.NEXTVAL"],
        ),
    ],
)
def test_generate_column_alter_statements(
    table_name, column_current, column_desired, expected_output
):
    # act
    output = oae.TableAction._generate_column_alter_statements(
        table_name, column_current, column_desired
    )

    # assert
    assert output == expected_output


@pytest.mark.parametrize(
    "table_name, column_current, column_desired, error_type",
    [
        (
            "my_table",
            DummyColumn("col1"),
            DummyColumn("col1", column_default="my_default"),
            ValueError,
        ),  # defaults cannot be added
        (
            "my_table",
            DummyColumn("col1"),
            DummyColumn("col1", column_default=100),
            ValueError,
        ),  # defaults cannot be added
        (
            "my_table",
            DummyColumn("col1", data_type="TEXT", character_maximum_length=20),
            DummyColumn("col1", data_type="TEXT", character_maximum_length=10),
            ValueError,
        ),  # varchar length cannot be reduced
        (
            "my_table",
            DummyColumn(
                "col1",
                data_type="TEXT",
                character_maximum_length=20,
                collation_name="en-ci",
            ),
            DummyColumn(
                "col1",
                data_type="TEXT",
                character_maximum_length=10,
                collation_name="en-ci",
            ),
            ValueError,
        ),  # varchar length cannot be reduced
        (
            "my_table",
            DummyColumn("col1", data_type="TEXT", character_maximum_length=20),
            DummyColumn(
                "col1",
                data_type="TEXT",
                character_maximum_length=20,
                collation_name="en-ci",
            ),
            ValueError,
        ),  # collation cannot be added
        (
            "my_table",
            DummyColumn(
                "col1",
                data_type="TEXT",
                character_maximum_length=20,
                collation_name="en-ci",
            ),
            DummyColumn("col1", data_type="TEXT", character_maximum_length=20),
            ValueError,
        ),  # collation cannot be removed
        (
            "my_table",
            DummyColumn(
                "col1",
                data_type="TEXT",
                character_maximum_length=20,
                collation_name="en-ci",
            ),
            DummyColumn(
                "col1",
                data_type="TEXT",
                character_maximum_length=20,
                collation_name="de-ci",
            ),
            ValueError,
        ),  # collation cannot be changed
        (
            "my_table",
            DummyColumn(
                "col1", data_type="NUMBER", numeric_precision=10, numeric_scale=4
            ),
            DummyColumn(
                "col1", data_type="NUMBER", numeric_precision=10, numeric_scale=0
            ),
            ValueError,
        ),  # numeric scale cannot be changed
        (
            "my_table",
            DummyColumn(
                "col1", data_type="NUMBER", numeric_precision=10, numeric_scale=0
            ),
            DummyColumn(
                "col1", data_type="NUMBER", numeric_precision=10, numeric_scale=4
            ),
            ValueError,
        ),  # numeric scale cannot be changed
        (
            "my_table",
            DummyColumn(
                "col1", data_type="NUMBER", numeric_precision=10, numeric_scale=4
            ),
            DummyColumn(
                "col1", data_type="NUMBER", numeric_precision=20, numeric_scale=0
            ),
            ValueError,
        ),  # numeric scale cannot be changed
        (
            "my_table",
            DummyColumn(
                "col1", data_type="NUMBER", numeric_precision=20, numeric_scale=0
            ),
            DummyColumn(
                "col1", data_type="NUMBER", numeric_precision=10, numeric_scale=4
            ),
            ValueError,
        ),  # numeric scale cannot be changed
    ],
)
def test_error_generate_column_alter_statements(
    table_name, column_current, column_desired, error_type
):
    with pytest.raises(error_type):
        _ = oae.TableAction._generate_column_alter_statements(
            table_name, column_current, column_desired
        )


@pytest.mark.parametrize(
    "input, get_ddl_mock, expected",
    [
        (
            oae.TableAction(
                schema="myschema", name="mytable", action=DbActionType.ALTER
            ),
            [
                {
                    "COL_DEF": """
            create or replace TABLE MYTABLE (
                COL1 NUMBER(10,4),
                COL2 NUMBER(10,4)
            );
        """.strip()
                }
            ],
            {"col1": "COL1 NUMBER(10,4)", "col2": "COL2 NUMBER(10,4)"},
        ),
        (
            oae.TableAction(
                schema="myschema", name="mytable", action=DbActionType.ALTER
            ),
            [
                {
                    "COL_DEF": """
            create or replace TABLE MYTABLE (
                COL1 NUMBER(10,4) DEFAULT MY_SEQUENCE.NEXTVAL,
                COL2 NUMBER(10,4)
            );
        """.strip()
                }
            ],
            {
                "col1": "COL1 NUMBER(10,4) DEFAULT MY_SEQUENCE.NEXTVAL",
                "col2": "COL2 NUMBER(10,4)",
            },
        ),
        (
            oae.TableAction(
                schema="myschema", name="mytable", action=DbActionType.ALTER
            ),
            [
                {
                    "COL_DEF": """
            create or replace TABLE MYTABLE (
                COL1 NUMBER(10,4) NOT NULL,
                COL2 NUMBER(10,4) DEFAULT NULL
            );
        """.strip()
                }
            ],
            {
                "col1": "COL1 NUMBER(10,4) NOT NULL",
                "col2": "COL2 NUMBER(10,4) DEFAULT NULL",
            },
        ),
        (
            oae.TableAction(
                schema="myschema", name="mytable", action=DbActionType.ALTER
            ),
            [
                {
                    "COL_DEF": """
            create or replace TABLE MYTABLE (
                COL1 NUMBER(10,4),
                COL2 NUMBER(10,4) DEFAULT NULL,
                CONSTRAINT MY_CONSTRAINT UNIQUE (COL1)
            );
        """.strip()
                }
            ],
            {"col1": "COL1 NUMBER(10,4)", "col2": "COL2 NUMBER(10,4) DEFAULT NULL"},
        ),
        (
            oae.TableAction(
                schema="myschema", name="mytable", action=DbActionType.ALTER
            ),
            [
                {
                    "COL_DEF": """
            create or replace TABLE MYTABLE (
                COL1 NUMBER(10,4),
                COL2 NUMBER(10,4) DEFAULT NULL,
                CONSTRAINT MY_CONSTRAINT1 UNIQUE (COL1),
                CONSTRAINT MY_CONSTRAINT2 FOREIGN KEY (COL2) REFERENCES MYTABLE2 (A)
            );
        """.strip()
                }
            ],
            {"col1": "COL1 NUMBER(10,4)", "col2": "COL2 NUMBER(10,4) DEFAULT NULL"},
        ),
        (
            oae.TableAction(
                schema="myschema", name="mytable", action=DbActionType.ALTER
            ),
            [
                {
                    "COL_DEF": """
            create or replace TABLE MYTABLE (
                COL1 NUMBER(10,4) DEFAULT 'DEFAULTVALUE',
                COL2 NUMBER(10,4)
            );
        """.strip()
                }
            ],
            {
                "col1": "COL1 NUMBER(10,4) DEFAULT 'DEFAULTVALUE'",
                "col2": "COL2 NUMBER(10,4)",
            },
        ),
        (
            oae.TableAction(
                schema="myschema", name="mytable", action=DbActionType.ALTER
            ),
            [
                {
                    "COL_DEF": """
            create or replace TABLE MYTABLE (
                COL1 NUMBER(10,4) DEFAULT 'defaultvalue',
                COL2 NUMBER(10,4)
            );
        """.strip()
                }
            ],
            {
                "col1": "COL1 NUMBER(10,4) DEFAULT 'defaultvalue'",
                "col2": "COL2 NUMBER(10,4)",
            },
        ),
    ],
)
def test_get_column_definitions(input, get_ddl_mock, expected):
    mock_snow_client = DummySnowClient(get_ddl_mock)
    result = input._get_column_definitions(mock_snow_client)
    # only keys in the expected dict are tested: result contains additional entries, that can be ignored
    for key in expected:
        assert result[key] == expected[key]


# endregion columns


# region policies


@pytest.mark.parametrize(
    "object_type, object_full_name, desired_policy_references, expected",
    [
        (
            DbObjectType.TABLE,
            "my_schema.my_table",
            [
                RowAccessPolicyReference(
                    {
                        "POLICY_DB": "pol_db",
                        "POLICY_SCHEMA": "pol_schema",
                        "POLICY_NAME": "pol_name",
                        "POLICY_KIND": "ROW_ACCESS_POLICY",
                        "REF_DATABASE_NAME": "my_db",
                        "REF_SCHEMA_NAME": "my_schema",
                        "REF_ENTITY_NAME": "my_table",
                        "REF_ENTITY_DOMAIN": "TABLE",
                        "REF_COLUMN_NAME": "",
                        "REF_ARG_COLUMN_NAMES": '["A", "B", "C"]',
                        "TAG_DATABASE": "",
                        "TAG_SCHEMA": "",
                        "TAG_NAME": "",
                        "POLICY_STATUS": "",
                    }
                )
            ],
            [
                "ALTER TABLE my_schema.my_table DROP ALL ROW ACCESS POLICIES",
                "ALTER TABLE my_schema.my_table ADD ROW ACCESS POLICY pol_schema.pol_name ON (A,B,C)"
            ],
        ),
    ],
)
def test_generate_alter_row_access_policy_assignment_statement(object_type, object_full_name, desired_policy_references, expected):
    result = oae.TableAction._generate_alter_row_access_policy_assignment_statement(object_type, object_full_name, desired_policy_references)
    assert result == expected


@pytest.mark.parametrize(
    "object_type, object_full_name, desired_policy_references, desired_column_names, expected",
    [
        (
            DbObjectType.TABLE,
            "my_schema.my_table",
            [
                MaskingPolicyReference(
                    {
                        "POLICY_DB": "pol_db",
                        "POLICY_SCHEMA": "pol_schema",
                        "POLICY_NAME": "pol_name",
                        "POLICY_KIND": "ROW_ACCESS_POLICY",
                        "REF_DATABASE_NAME": "my_db",
                        "REF_SCHEMA_NAME": "my_schema",
                        "REF_ENTITY_NAME": "my_table",
                        "REF_ENTITY_DOMAIN": "TABLE",
                        "REF_COLUMN_NAME": "A",
                        "REF_ARG_COLUMN_NAMES": '["B", "C"]',
                        "TAG_DATABASE": "",
                        "TAG_SCHEMA": "",
                        "TAG_NAME": "",
                        "POLICY_STATUS": "",
                    }
                )
            ],
            ["A", "B", "C"],
            [
                "ALTER TABLE my_schema.my_table ALTER COLUMN A UNSET MASKING POLICY",
                "ALTER TABLE my_schema.my_table ALTER COLUMN B UNSET MASKING POLICY",
                "ALTER TABLE my_schema.my_table ALTER COLUMN C UNSET MASKING POLICY",
                "ALTER TABLE my_schema.my_table ALTER COLUMN A SET MASKING POLICY pol_schema.pol_name USING (A,B,C) FORCE"
            ],
        ),
    ],
)
def test_generate_alter_masking_policy_assignment_statement(object_type, object_full_name, desired_policy_references, desired_column_names, expected):
    result = oae.TableAction._generate_alter_masking_policy_assignment_statement(object_type, object_full_name, desired_policy_references, desired_column_names)
    assert result == expected


# endregion policies


# region clustering key alter


@pytest.mark.parametrize(
    "table_name, input, expected",
    [
        ("my_table", None, "ALTER TABLE my_table DROP CLUSTERING KEY"),
        (
            "my_table",
            "LINEAR(MANDANT_ID,KJMO)",
            "ALTER TABLE my_table CLUSTER BY (MANDANT_ID,KJMO)",
        ),
        (
            "my_table",
            "LINEAR (MANDANT_ID,KJMO)",
            "ALTER TABLE my_table CLUSTER BY (MANDANT_ID,KJMO)",
        ),
        (
            "my_table",
            "(MANDANT_ID,KJMO)",
            "ALTER TABLE my_table CLUSTER BY (MANDANT_ID,KJMO)",
        ),
        (
            "my_table",
            "(MANDANT_ID, KJMO)",
            "ALTER TABLE my_table CLUSTER BY (MANDANT_ID, KJMO)",
        ),
        (
            "my_table",
            "( MANDANT_ID, KJMO )",
            "ALTER TABLE my_table CLUSTER BY ( MANDANT_ID, KJMO )",
        ),
        (
            "my_table",
            "(\nMANDANT_ID,\nKJMO\n)",
            "ALTER TABLE my_table CLUSTER BY (\nMANDANT_ID,\nKJMO\n)",
        ),
        (
            "my_table",
            "(\tMANDANT_ID,\tKJMO\t)",
            "ALTER TABLE my_table CLUSTER BY (\tMANDANT_ID,\tKJMO\t)",
        ),
    ],
)
def test_generate_clustering_statement(table_name, input, expected):
    result = oae.TableAction._generate_clustering_statement(table_name, input)
    assert result == expected


# endregion clustering key alter


# region retention time


@pytest.mark.parametrize(
    "table_name, retention_time, schema_retention_time, expected",
    [
        ("my_table", 1, 1, "ALTER TABLE my_table UNSET DATA_RETENTION_TIME_IN_DAYS"),
        ("my_table", 1, 90, "ALTER TABLE my_table SET DATA_RETENTION_TIME_IN_DAYS = 1"),
        (
            "my_table",
            90,
            1,
            "ALTER TABLE my_table SET DATA_RETENTION_TIME_IN_DAYS = 90",
        ),
        ("my_table", 90, 90, "ALTER TABLE my_table UNSET DATA_RETENTION_TIME_IN_DAYS"),
    ],
)
def test_generate_retention_time_statement(
    table_name, retention_time, schema_retention_time, expected
):
    result = oae.TableAction._generate_retention_time_statement(
        table_name, retention_time, schema_retention_time
    )
    assert result == expected


# endregion  retention time

# region retention time


@pytest.mark.parametrize(
    "table_name, input, expected",
    [
        ("my_table", None, "ALTER TABLE my_table UNSET COMMENT"),
        (
            "my_table",
            "test comment",
            "ALTER TABLE my_table SET COMMENT = 'test comment'",
        ),
        ("my_table", "", "ALTER TABLE my_table SET COMMENT = ''"),
    ],
)
def test_generate_comment_statement(table_name, input, expected):
    result = oae.TableAction._generate_comment_statement(table_name, input)
    assert result == expected


# endregion  retention time


# region table constraint alter


def test_generate_drop_foreign_key_statement():
    table_name = "MY_SCHEMA.MY_TABLE"
    columns = [
        ConstraintColumnForeignKey(1, "A", "X"),
        ConstraintColumnForeignKey(2, "B", "Y"),
    ]
    result = oae.TableAction._generate_drop_foreign_key_statement(table_name, columns)
    assert result == "ALTER TABLE MY_SCHEMA.MY_TABLE DROP FOREIGN KEY (A, B)"


def test_generate_drop_primary_key_statement():
    table_name = "MY_SCHEMA.MY_TABLE"
    result = oae.TableAction._generate_drop_primary_key_statement(table_name)
    assert result == "ALTER TABLE MY_SCHEMA.MY_TABLE DROP PRIMARY KEY"


def test_generate_drop_unique_key_statement():
    table_name = "MY_SCHEMA.MY_TABLE"
    columns = [ConstraintColumn(1, "A"), ConstraintColumn(2, "B")]
    result = oae.TableAction._generate_drop_unique_key_statement(table_name, columns)
    assert result == "ALTER TABLE MY_SCHEMA.MY_TABLE DROP UNIQUE (A, B)"


def test_generate_create_foreign_key_statement_with_name():
    table_name = "MY_SCHEMA.MY_TABLE"
    constraint_instance = InstanceConstraintForeignKey(
        [
            {
                "fk_schema_name": "MY_SCHEMA",
                "fk_table_name": "MY_TABLE",
                "fk_name": "MY_CONSTRAINT",
                "pk_schema_name": "MY_SCHEMA_2",
                "pk_table_name": "MY_TABLE_2",
                "pk_name": "MY_CONSTRAINT_2",
                "comment": None,
                "key_sequence": 1,
                "fk_column_name": "A",
                "pk_column_name": "X",
            },
            {
                "fk_schema_name": "MY_SCHEMA",
                "fk_table_name": "MY_TABLE",
                "fk_name": "MY_CONSTRAINT",
                "pk_schema_name": "MY_SCHEMA_2",
                "pk_table_name": "MY_TABLE_2",
                "pk_name": "MY_CONSTRAINT_2",
                "comment": None,
                "key_sequence": 2,
                "fk_column_name": "B",
                "pk_column_name": "Y",
            },
        ]
    )
    result = oae.TableAction._generate_create_foreign_key_statement(
        table_name, constraint_instance
    )
    assert (
        result
        == "ALTER TABLE MY_SCHEMA.MY_TABLE ADD CONSTRAINT MY_CONSTRAINT FOREIGN KEY (A, B) REFERENCES MY_SCHEMA_2.MY_TABLE_2 (X, Y) "
    )


def test_generate_create_foreign_key_statement_without_name():
    table_name = "MY_SCHEMA.MY_TABLE"
    constraint_instance = InstanceConstraintForeignKey(
        [
            {
                "fk_schema_name": "MY_SCHEMA",
                "fk_table_name": "MY_TABLE",
                "fk_name": "SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff9959",
                "pk_schema_name": "MY_SCHEMA_2",
                "pk_table_name": "MY_TABLE_2",
                "pk_name": "MY_CONSTRAINT_2",
                "comment": None,
                "key_sequence": 1,
                "fk_column_name": "A",
                "pk_column_name": "X",
            },
            {
                "fk_schema_name": "MY_SCHEMA",
                "fk_table_name": "MY_TABLE",
                "fk_name": "SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff9959",
                "pk_schema_name": "MY_SCHEMA_2",
                "pk_table_name": "MY_TABLE_2",
                "pk_name": "MY_CONSTRAINT_2",
                "comment": None,
                "key_sequence": 2,
                "fk_column_name": "B",
                "pk_column_name": "Y",
            },
        ]
    )
    result = oae.TableAction._generate_create_foreign_key_statement(
        table_name, constraint_instance
    )
    assert (
        result
        == "ALTER TABLE MY_SCHEMA.MY_TABLE ADD  FOREIGN KEY (A, B) REFERENCES MY_SCHEMA_2.MY_TABLE_2 (X, Y) "
    )


def test_generate_create_foreign_key_statement_with_comment():
    table_name = "MY_SCHEMA.MY_TABLE"
    constraint_instance = InstanceConstraintForeignKey(
        [
            {
                "fk_schema_name": "MY_SCHEMA",
                "fk_table_name": "MY_TABLE",
                "fk_name": "SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff9959",
                "pk_schema_name": "MY_SCHEMA_2",
                "pk_table_name": "MY_TABLE_2",
                "pk_name": "MY_CONSTRAINT_2",
                "comment": "test comment",
                "key_sequence": 1,
                "fk_column_name": "A",
                "pk_column_name": "X",
            },
            {
                "fk_schema_name": "MY_SCHEMA",
                "fk_table_name": "MY_TABLE",
                "fk_name": "SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff9959",
                "pk_schema_name": "MY_SCHEMA_2",
                "pk_table_name": "MY_TABLE_2",
                "pk_name": "MY_CONSTRAINT_2",
                "comment": "test comment",
                "key_sequence": 2,
                "fk_column_name": "B",
                "pk_column_name": "Y",
            },
        ]
    )
    result = oae.TableAction._generate_create_foreign_key_statement(
        table_name, constraint_instance
    )
    assert (
        result
        == "ALTER TABLE MY_SCHEMA.MY_TABLE ADD  FOREIGN KEY (A, B) REFERENCES MY_SCHEMA_2.MY_TABLE_2 (X, Y) COMMENT 'test comment'"
    )


def test_generate_create_primary_key_statement_with_name():
    table_name = "MY_SCHEMA.MY_TABLE"
    constraint_instance = InstanceConstraintPrimaryKey(
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
    result = oae.TableAction._generate_create_primary_key_statement(
        table_name, constraint_instance
    )
    assert (
        result
        == "ALTER TABLE MY_SCHEMA.MY_TABLE ADD CONSTRAINT MY_CONSTRAINT PRIMARY KEY (A, B) "
    )


def test_generate_create_primary_key_statement_without_name():
    table_name = "MY_SCHEMA.MY_TABLE"
    constraint_instance = InstanceConstraintPrimaryKey(
        [
            {
                "schema_name": "MY_SCHEMA",
                "table_name": "MY_TABLE",
                "constraint_name": "SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff9959",
                "comment": None,
                "key_sequence": 1,
                "column_name": "A",
            },
            {
                "schema_name": "MY_SCHEMA",
                "table_name": "MY_TABLE",
                "constraint_name": "SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff9959",
                "comment": None,
                "key_sequence": 2,
                "column_name": "B",
            },
        ]
    )
    result = oae.TableAction._generate_create_primary_key_statement(
        table_name, constraint_instance
    )
    assert result == "ALTER TABLE MY_SCHEMA.MY_TABLE ADD  PRIMARY KEY (A, B) "


def test_generate_create_primary_key_statement_with_comment():
    table_name = "MY_SCHEMA.MY_TABLE"
    constraint_instance = InstanceConstraintPrimaryKey(
        [
            {
                "schema_name": "MY_SCHEMA",
                "table_name": "MY_TABLE",
                "constraint_name": "SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff9959",
                "comment": "test comment",
                "key_sequence": 1,
                "column_name": "A",
            },
            {
                "schema_name": "MY_SCHEMA",
                "table_name": "MY_TABLE",
                "constraint_name": "SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff9959",
                "comment": "test comment",
                "key_sequence": 2,
                "column_name": "B",
            },
        ]
    )
    result = oae.TableAction._generate_create_primary_key_statement(
        table_name, constraint_instance
    )
    assert (
        result
        == "ALTER TABLE MY_SCHEMA.MY_TABLE ADD  PRIMARY KEY (A, B) COMMENT 'test comment'"
    )


def test_generate_create_unique_key_statement_with_name():
    table_name = "MY_SCHEMA.MY_TABLE"
    constraint_instance = InstanceConstraintPrimaryKey(
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
    result = oae.TableAction._generate_create_unique_key_statement(
        table_name, constraint_instance
    )
    assert (
        result
        == "ALTER TABLE MY_SCHEMA.MY_TABLE ADD CONSTRAINT MY_CONSTRAINT UNIQUE (A, B) "
    )


def test_generate_create_unique_key_statement_without_name():
    table_name = "MY_SCHEMA.MY_TABLE"
    constraint_instance = InstanceConstraintPrimaryKey(
        [
            {
                "schema_name": "MY_SCHEMA",
                "table_name": "MY_TABLE",
                "constraint_name": "SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff9959",
                "comment": None,
                "key_sequence": 1,
                "column_name": "A",
            },
            {
                "schema_name": "MY_SCHEMA",
                "table_name": "MY_TABLE",
                "constraint_name": "SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff9959",
                "comment": None,
                "key_sequence": 2,
                "column_name": "B",
            },
        ]
    )
    result = oae.TableAction._generate_create_unique_key_statement(
        table_name, constraint_instance
    )
    assert result == "ALTER TABLE MY_SCHEMA.MY_TABLE ADD  UNIQUE (A, B) "


def test_generate_create_unique_key_statement_with_comment():
    table_name = "MY_SCHEMA.MY_TABLE"
    constraint_instance = InstanceConstraintPrimaryKey(
        [
            {
                "schema_name": "MY_SCHEMA",
                "table_name": "MY_TABLE",
                "constraint_name": "SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff9959",
                "comment": "test comment",
                "key_sequence": 1,
                "column_name": "A",
            },
            {
                "schema_name": "MY_SCHEMA",
                "table_name": "MY_TABLE",
                "constraint_name": "SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff9959",
                "comment": "test comment",
                "key_sequence": 2,
                "column_name": "B",
            },
        ]
    )
    result = oae.TableAction._generate_create_unique_key_statement(
        table_name, constraint_instance
    )
    assert (
        result
        == "ALTER TABLE MY_SCHEMA.MY_TABLE ADD  UNIQUE (A, B) COMMENT 'test comment'"
    )


# endregion table constraint alter
