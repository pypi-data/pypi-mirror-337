import pytest

import acedeploy.services.policy_service as pos
import acedeploy.core.model_instance_objects as mio


from policy_service_dummy_classes import (
    DummyColumn,
)


@pytest.mark.parametrize(
    "columns, policy_assignments_of_object, always_create, expected_columns_string, expected_columns_string_without_database_reference",
    [
        # Test case 1: empty inputs
        ([], [], False, "", ""),
        # Test case 2: no policy assignments, always create
        (
            [
                DummyColumn(
                    object_schema="public",
                    object_name="my_table",
                    ordinal_position=1,
                    column_name="id",
                    comment="Primary key",
                ),
                DummyColumn(
                    object_schema="public",
                    object_name="my_table",
                    ordinal_position=2,
                    column_name="name",
                    comment="Customer name",
                ),
                DummyColumn(
                    object_schema="public",
                    object_name="my_table",
                    ordinal_position=3,
                    column_name="email",
                    comment="Customer email",
                ),
            ],
            [],
            True,
            "(id COMMENT 'Primary key', name COMMENT 'Customer name', email COMMENT 'Customer email')",
            "(id COMMENT 'Primary key', name COMMENT 'Customer name', email COMMENT 'Customer email')",
        ),  # Test case 3: no policy assignments, don't always create
        (
            [
                DummyColumn(
                    object_schema="public",
                    object_name="my_table",
                    ordinal_position=1,
                    column_name="id",
                    comment="Primary key",
                ),
                DummyColumn(
                    object_schema="public",
                    object_name="my_table",
                    ordinal_position=2,
                    column_name="name",
                    comment="Customer name",
                ),
                DummyColumn(
                    object_schema="public",
                    object_name="my_table",
                    ordinal_position=3,
                    column_name="email",
                    comment="Customer email",
                ),
            ],
            [],
            False,
            "",
            "",
        ),
        # Test case 4: policy assignments on some columns, don't always create
        (
            [
                DummyColumn(
                    object_schema="public",
                    object_name="my_table",
                    ordinal_position=2,
                    column_name="name",
                ),
                DummyColumn(
                    object_schema="public",
                    object_name="my_table",
                    ordinal_position=1,
                    column_name="id",
                ),
                DummyColumn(
                    object_schema="public",
                    object_name="my_table",
                    ordinal_position=3,
                    column_name="email",
                ),
            ],
            [
                {
                    "assignment_type": "view_columns",
                    "assignment": "public.my_table.name",
                    "policy_database": "my_db",
                    "policy_schema": "security",
                    "policy": "mask_name",
                    "argument_columns": ["public.my_table.id"],
                },
                {
                    "assignment_type": "view_columns",
                    "assignment": "public.my_table.email",
                    "policy_database": "my_db",
                    "policy_schema": "security",
                    "policy": "mask_email",
                    "argument_columns": None,
                },
            ],
            False,
            "(id , name WITH MASKING POLICY my_db.security.mask_name USING (name, public.my_table.id) , email WITH MASKING POLICY my_db.security.mask_email  )",
            "(id , name WITH MASKING POLICY security.mask_name USING (name, public.my_table.id) , email WITH MASKING POLICY security.mask_email  )",
        ),
        # Test case 5: policy assignments on all columns, don't always create
        (
            [
                DummyColumn(
                    object_schema="public",
                    object_name="my_table",
                    ordinal_position=1,
                    column_name="id",
                    comment="Primary key",
                ),
                DummyColumn(
                    object_schema="public",
                    object_name="my_table",
                    ordinal_position=2,
                    column_name="name",
                ),
                DummyColumn(
                    object_schema="public",
                    object_name="my_table",
                    ordinal_position=3,
                    column_name="email",
                ),
            ],
            [
                {
                    "assignment_type": "view_columns",
                    "assignment": "public.my_table.id",
                    "policy_database": "my_db",
                    "policy_schema": "security",
                    "policy": "mask_id",
                    "argument_columns": None,
                },
                {
                    "assignment_type": "view_columns",
                    "assignment": "public.my_table.name",
                    "policy_database": "my_db",
                    "policy_schema": "security",
                    "policy": "mask_name",
                    "argument_columns": ["public.my_table.id"],
                },
                {
                    "assignment_type": "view_columns",
                    "assignment": "public.my_table.email",
                    "policy_database": "my_db",
                    "policy_schema": "security",
                    "policy": "mask_email",
                    "argument_columns": None,
                },
            ],
            False,
            "(id WITH MASKING POLICY my_db.security.mask_id  COMMENT 'Primary key', name WITH MASKING POLICY my_db.security.mask_name USING (name, public.my_table.id) , email WITH MASKING POLICY my_db.security.mask_email  )",
            "(id WITH MASKING POLICY security.mask_id  COMMENT 'Primary key', name WITH MASKING POLICY security.mask_name USING (name, public.my_table.id) , email WITH MASKING POLICY security.mask_email  )",
        ),
    ],
)
def test_create_columns_string_of_view_with_policy_assignments(
    columns,
    policy_assignments_of_object,
    always_create,
    expected_columns_string,
    expected_columns_string_without_database_reference,
):
    actual_columns_string, actual_columns_string_without_database_reference = (
        pos.create_columns_string_of_view_with_policy_assignments(
            columns, policy_assignments_of_object, always_create
        )
    )
    assert actual_columns_string == expected_columns_string
    assert (
        actual_columns_string_without_database_reference
        == expected_columns_string_without_database_reference
    )


@pytest.mark.parametrize(
    "object_statement, column, expected",
    [
        ("", "ID", None),
        (
            "CREATE OR REPLACE VIEW MY_SCHEMA.VIEW1 (ID, NAME, AGE) AS SELECT ID, NAME, AGE FROM MY_SCHEMA.TABLE2;",
            "ID",
            "(ID, NAME, AGE)",
        ),
        (
            "CREATE OR REPLACE VIEW MY_SCHEMA.VIEW2 (ID COMMENT 'columns string (ID, NAME, AGE)', NAME, AGE) AS SELECT ID, NAME, AGE FROM MY_SCHEMA.TABLE2;",
            "ID",
            "(ID COMMENT 'columns string (ID, NAME, AGE)', NAME, AGE)",
        ),
        (
            "CREATE OR REPLACE VIEW MY_SCHEMA.VIEW3 (ID COMMENT '()()(())))', NAME, AGE) AS SELECT ID, NAME, AGE FROM MY_SCHEMA.TABLE2;",
            "ID",
            "(ID COMMENT '()()(())))', NAME, AGE)",
        ),
        (
            "CREATE OR REPLACE VIEW MY_SCHEMA.VIEW4 (\n\n    ID ,\n NAME COMMENT '()()((ID))))', AGE\n) AS SELECT ID, NAME, AGE FROM MY_SCHEMA.TABLE2;",
            "ID",
            "(\n\n    ID ,\n NAME COMMENT '()()((ID))))', AGE\n)",
        ),
        (
            "CREATE OR REPLACE VIEW MY_SCHEMA.VIEW5 (ID, NAME, AGE) AS SELECT ID, NAME, AGE FROM MY_SCHEMA.TABLE2;",
            "ID",
            "(ID, NAME, AGE)",
        ),
        (
            "CREATE OR REPLACE VIEW MY_SCHEMA.VIEW6 (ID, ADDRESS) AS SELECT ID, ADDRESS FROM MY_SCHEMA.TABLE3;",
            "ADDRESS",
            None,
        ),
        (
            "CREATE OR REPLACE VIEW MY_SCHEMA.VIEW7 AS SELECT COLUMN1, COLUMN2, COLUMN3 FROM MY_SCHEMA.TABLE4;",
            "",
            None,
        ),
        (
            "CREATE OR REPLACE VIEW MY_SCHEMA.VIEW8 AS SELECT COLUMN1, COLUMN2, COLUMN3 FROM MY_SCHEMA.TABLE4;",
            "COLUMN1",
            None,
        ),
        (
            "CREATE OR REPLACE VIEW MY_SCHEMA.VIEW9 (ID INT WITH TAG (COLUMN_CATEGORY='ID'), NAME VARCHAR, AGE INT) AS SELECT ID, NAME, AGE FROM MY_SCHEMA.TABLE2;",
            "ID",
            "(ID INT WITH TAG (COLUMN_CATEGORY='ID'), NAME VARCHAR, AGE INT)",
        ),
        (
            "CREATE OR REPLACE VIEW MY_SCHEMA.VIEW9 (id INT WITH TAG (COLUMN_CATEGORY='ID'), NAME VARCHAR, AGE INT) AS SELECT ID, NAME, AGE FROM MY_SCHEMA.TABLE2;",
            "ID",
            "(id INT WITH TAG (COLUMN_CATEGORY='ID'), NAME VARCHAR, AGE INT)",
        ),
        ("", "", None),
    ],
)
def test_extract_columns_string(object_statement, column, expected):
    if not column:
        with pytest.raises(ValueError):
            pos.extract_columns_string(object_statement, column)
    else:
        result = pos.extract_columns_string(object_statement, column)
        assert result == expected


@pytest.mark.parametrize(
    "regex_object, columns_definition, expected",
    [
        (
            r"\s+with\s+projection\s+policy\s+|\s+projection\s+policy\s+|\s+with\s+tag\s*\(|\s+tag\s*\(|\s+comment\s*\'",
            "COUNTRY with projection policy dklstag.kdlf WITH TAG (dktagsl.kldsf = 'COMMENT') COMMENT  'tests2'",
            ('COUNTRY', " with projection policy dklstag.kdlf WITH TAG (dktagsl.kldsf = 'COMMENT') COMMENT  'tests2'")
        ),
        (
            r"\s+with\s+projection\s+policy\s+|\s+projection\s+policy\s+|\s+with\s+tag\s*\(|\s+tag\s*\(|\s+comment\s*\'",
            "COUNTRY dklstag.kdlf WITH TAG (dktagsl.kldsf = 'COMMENT') COMMENT  'tests2'",
            ('COUNTRY dklstag.kdlf', " WITH TAG (dktagsl.kldsf = 'COMMENT') COMMENT  'tests2'")
        ),
        (
            r"\s+with\s+projection\s+policy\s+|\s+projection\s+policy\s+|\s+with\s+tag\s*\(|\s+tag\s*\(|\s+comment\s*\'",
            "COUNTRY (dktagsl.kldsf = 'COMMENT') COMMENT  'tests2'",
            ("COUNTRY (dktagsl.kldsf = 'COMMENT')", " COMMENT  'tests2'")
        ),
        (
            r"\s+with\s+projection\s+policy\s+|\s+projection\s+policy\s+|\s+with\s+tag\s*\(|\s+tag\s*\(|\s+comment\s*\'",
            "COUNTRY ' COMMENT'tests2' ' COMMENT  'tests2'",
            ("COUNTRY ' COMMENT'tests2' '", " COMMENT  'tests2'")
        ),
        (
            r"\s+with\s+projection\s+policy\s+|\s+projection\s+policy\s+|\s+with\s+tag\s*\(|\s+tag\s*\(|\s+comment\s*\'",
            "COUNTRY ( COMMENT'tests2' ) COMMENT  'tests2'",
            ("COUNTRY ( COMMENT'tests2' )", " COMMENT  'tests2'")
        ),
        (
            r"\s+with\s+projection\s+policy\s+|\s+projection\s+policy\s+|\s+with\s+tag\s*\(|\s+tag\s*\(|\s+comment\s*\'",
            "COUNTRY ( comment 'tests2') comment  'tests2'",
            ("COUNTRY ( comment 'tests2')", " comment  'tests2'")
        ),
        (
            r"\s+with\s+projection\s+policy\s+|\s+projection\s+policy\s+|\s+with\s+tag\s*\(|\s+tag\s*\(|\s+comment\s*\'",
            "COUNTRY ' ( comment'tests2' ) ' ( comment'tests2' ) comment  'tests2'",
            ("COUNTRY ' ( comment'tests2' ) ' ( comment'tests2' )", " comment  'tests2'")
        ),
        (
            r"\s+with\s+projection\s+policy\s+|\s+projection\s+policy\s+|\s+with\s+tag\s*\(|\s+tag\s*\(|\s+comment\s*\'",
            "COUNTRY ( comment'tests2' )' comment'tests2' ' comment  'tests2'",
            ("COUNTRY ( comment'tests2' )' comment'tests2' '", " comment  'tests2'")
        ),
        (
            r"\s+with\s+projection\s+policy\s+|\s+projection\s+policy\s+|\s+with\s+tag\s*\(|\s+tag\s*\(|\s+comment\s*\'",
            "COUNTRY ( comment'tests2' )' ()()( comment'tests2' ' comment  'tests2'",
            ("COUNTRY ( comment'tests2' )' ()()( comment'tests2' '", " comment  'tests2'")
        ),
        (
            r"\s+with\s+projection\s+policy\s+|\s+projection\s+policy\s+|\s+with\s+tag\s*\(|\s+tag\s*\(|\s+comment\s*\'",
            "COUNTRY ( comment 'tests2') ()()( comment'tests2')  comment  'tests2'",
            ("COUNTRY ( comment 'tests2') ()()( comment'tests2')", "  comment  'tests2'")
        ),
        (
            r"\s+with\s+projection\s+policy\s+|\s+projection\s+policy\s+|\s+with\s+tag\s*\(|\s+tag\s*\(|\s+comment\s*\'",
            r"COUNTRY ' \' COMMENT\'tests2 ' COMMENT'tests2 \' test' ",
            ("COUNTRY ' \\' COMMENT\\'tests2 '", " COMMENT'tests2 \\' test' ")
        ),
        (
            r"\s+with\s+projection\s+policy\s+|\s+projection\s+policy\s+|\s+with\s+tag\s*\(|\s+tag\s*\(|\s+comment\s*\'",
            r"COUNTRY INT WITH TAG (SCHEMA.MY_TAG = 'TAG_COMMENT') COMMENT  'tests2 WITH TAG ' ",
            ('COUNTRY INT', " WITH TAG (SCHEMA.MY_TAG = 'TAG_COMMENT') COMMENT  'tests2 WITH TAG ' ")
        ),
        (
            r"\s+with\s+projection\s+policy\s+|\s+projection\s+policy\s+|\s+with\s+tag\s*\(|\s+tag\s*\(|\s+comment\s*\'",
            "COUNTRY VARCHAR  comment  'tests2 comment'",
            ('COUNTRY VARCHAR', "  comment  'tests2 comment'")
        ),
        (
            r"\s+with\s+projection\s+policy\s+|\s+projection\s+policy\s+|\s+with\s+tag\s*\(|\s+tag\s*\(|\s+comment\s*\'",
            "COUNTRY VARCHAR WITH TAG (TAGS_SCHEMA.MY_TAG = 'TAG_VALUE') comment  ' WITH TAG '",
            ('COUNTRY VARCHAR', " WITH TAG (TAGS_SCHEMA.MY_TAG = 'TAG_VALUE') comment  ' WITH TAG '")
        ),
        (
            r"\s+with\s+projection\s+policy\s+|\s+projection\s+policy\s+|\s+with\s+tag\s*\(|\s+tag\s*\(|\s+comment\s*\'",
            "country comment 'test'",
            ('country', " comment 'test'")
        ),
    ],
)
def test_split_string_by_regex_match(regex_object, columns_definition, expected):

    result = pos.split_string_by_regex_match(regex_object, columns_definition)
    assert result == expected


@pytest.mark.parametrize(
    "object_type, object_statement, expected",
    [
        (
            pos.PolicyAssignmentObjectTypes.VIEW,
            """CREATE OR REPLACE VIEW MY_SCHEMA.MY_VIEW AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW MY_SCHEMA.MY_VIEW   AS SELECT 1 I;""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.VIEW,
            """CREATE OR REPLACE VIEW MY_DB.MY_SCHEMA.MY_VIEW AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW MY_DB.MY_SCHEMA.MY_VIEW   AS SELECT 1 I;""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.VIEW,
            """CREATE OR REPLACE VIEW "MY_SCHEMA"."MY_VIEW" AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW "MY_SCHEMA"."MY_VIEW"   AS SELECT 1 I;""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.VIEW,
            """CREATE OR REPLACE VIEW "MY_DB"."MY_SCHEMA"."MY_VIEW" AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW "MY_DB"."MY_SCHEMA"."MY_VIEW"   AS SELECT 1 I;""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.VIEW,
            """CREATE OR REPLACE VIEW MY_SCHEMA."MY_VIEW" AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW MY_SCHEMA."MY_VIEW"   AS SELECT 1 I;""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.VIEW,
            """CREATE OR REPLACE VIEW MY_DB."MY_SCHEMA"."MY_VIEW" AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW MY_DB."MY_SCHEMA"."MY_VIEW"   AS SELECT 1 I;""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.VIEW,
            """CREATE OR REPLACE VIEW MY_DB .MY_SCHEMA .MY_VIEW (I INT);""",
            """CREATE OR REPLACE VIEW MY_DB .MY_SCHEMA .MY_VIEW   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.VIEW,
            """CREATE OR REPLACE VIEW MY_DB. MY_SCHEMA. MY_VIEW (I INT);""",
            """CREATE OR REPLACE VIEW MY_DB. MY_SCHEMA. MY_VIEW   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.VIEW,
            """CREATE OR REPLACE VIEW "MY_DB" ."MY_SCHEMA" ."MY_VIEW" (I INT);""",
            """CREATE OR REPLACE VIEW "MY_DB" ."MY_SCHEMA" ."MY_VIEW"   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.VIEW,
            """CREATE OR REPLACE VIEW "MY_DB". "MY_SCHEMA". "MY_VIEW" (I INT);""",
            """CREATE OR REPLACE VIEW "MY_DB". "MY_SCHEMA". "MY_VIEW"   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.VIEW,
            """CREATE OR REPLACE VIEW "MY_VIEW" (I INT);""",
            """CREATE OR REPLACE VIEW "MY_VIEW"   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.VIEW,
            """CREATE OR REPLACE VIEW MY_VIEW (I INT);""",
            """CREATE OR REPLACE VIEW MY_VIEW   (I INT);""",
        ),
        
        (
            pos.PolicyAssignmentObjectTypes.TABLE,
            """CREATE OR REPLACE TABLE MY_SCHEMA.MY_TABLE (I INT);""",
            """CREATE OR REPLACE TABLE MY_SCHEMA.MY_TABLE   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.TABLE,
            """CREATE OR REPLACE TABLE MY_DB.MY_SCHEMA.MY_TABLE (I INT);""",
            """CREATE OR REPLACE TABLE MY_DB.MY_SCHEMA.MY_TABLE   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.TABLE,
            """CREATE OR REPLACE TABLE "MY_SCHEMA"."MY_TABLE" (I INT);""",
            """CREATE OR REPLACE TABLE "MY_SCHEMA"."MY_TABLE"   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.TABLE,
            """CREATE OR REPLACE TABLE "MY_DB"."MY_SCHEMA"."MY_TABLE" (I INT);""",
            """CREATE OR REPLACE TABLE "MY_DB"."MY_SCHEMA"."MY_TABLE"   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.TABLE,
            """CREATE OR REPLACE TABLE MY_SCHEMA."MY_TABLE" (I INT);""",
            """CREATE OR REPLACE TABLE MY_SCHEMA."MY_TABLE"   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.TABLE,
            """CREATE OR REPLACE TABLE MY_DB."MY_SCHEMA"."MY_TABLE" (I INT);""",
            """CREATE OR REPLACE TABLE MY_DB."MY_SCHEMA"."MY_TABLE"   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.TABLE,
            """CREATE OR REPLACE TABLE MY_DB .MY_SCHEMA .MY_TABLE (I INT);""",
            """CREATE OR REPLACE TABLE MY_DB .MY_SCHEMA .MY_TABLE   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.TABLE,
            """CREATE OR REPLACE TABLE MY_DB. MY_SCHEMA. MY_TABLE (I INT);""",
            """CREATE OR REPLACE TABLE MY_DB. MY_SCHEMA. MY_TABLE   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.TABLE,
            """CREATE OR REPLACE TABLE "MY_DB" ."MY_SCHEMA" ."MY_TABLE" (I INT);""",
            """CREATE OR REPLACE TABLE "MY_DB" ."MY_SCHEMA" ."MY_TABLE"   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.TABLE,
            """CREATE OR REPLACE TABLE "MY_DB". "MY_SCHEMA". "MY_TABLE" (I INT);""",
            """CREATE OR REPLACE TABLE "MY_DB". "MY_SCHEMA". "MY_TABLE"   (I INT);""",
        ),

        (
            pos.PolicyAssignmentObjectTypes.DYNAMICTABLE,
            """CREATE OR REPLACE DYNAMIC TABLE MY_SCHEMA.MY_TABLE (I INT);""",
            """CREATE OR REPLACE DYNAMIC TABLE MY_SCHEMA.MY_TABLE   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.DYNAMICTABLE,
            """CREATE OR REPLACE DYNAMIC TABLE MY_DB.MY_SCHEMA.MY_TABLE (I INT);""",
            """CREATE OR REPLACE DYNAMIC TABLE MY_DB.MY_SCHEMA.MY_TABLE   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.DYNAMICTABLE,
            """CREATE OR REPLACE DYNAMIC TABLE "MY_SCHEMA"."MY_TABLE" (I INT);""",
            """CREATE OR REPLACE DYNAMIC TABLE "MY_SCHEMA"."MY_TABLE"   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.DYNAMICTABLE,
            """CREATE OR REPLACE DYNAMIC TABLE "MY_DB"."MY_SCHEMA"."MY_TABLE" (I INT);""",
            """CREATE OR REPLACE DYNAMIC TABLE "MY_DB"."MY_SCHEMA"."MY_TABLE"   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.DYNAMICTABLE,
            """CREATE OR REPLACE DYNAMIC TABLE MY_SCHEMA."MY_TABLE" (I INT);""",
            """CREATE OR REPLACE DYNAMIC TABLE MY_SCHEMA."MY_TABLE"   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.DYNAMICTABLE,
            """CREATE OR REPLACE DYNAMIC TABLE MY_DB."MY_SCHEMA"."MY_TABLE" (I INT);""",
            """CREATE OR REPLACE DYNAMIC TABLE MY_DB."MY_SCHEMA"."MY_TABLE"   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.DYNAMICTABLE,
            """CREATE OR REPLACE DYNAMIC TABLE MY_DB .MY_SCHEMA .MY_TABLE (I INT);""",
            """CREATE OR REPLACE DYNAMIC TABLE MY_DB .MY_SCHEMA .MY_TABLE   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.DYNAMICTABLE,
            """CREATE OR REPLACE DYNAMIC TABLE MY_DB. MY_SCHEMA. MY_TABLE (I INT);""",
            """CREATE OR REPLACE DYNAMIC TABLE MY_DB. MY_SCHEMA. MY_TABLE   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.DYNAMICTABLE,
            """CREATE OR REPLACE DYNAMIC TABLE "MY_DB" ."MY_SCHEMA" ."MY_TABLE" (I INT);""",
            """CREATE OR REPLACE DYNAMIC TABLE "MY_DB" ."MY_SCHEMA" ."MY_TABLE"   (I INT);""",
        ),
        (
            pos.PolicyAssignmentObjectTypes.DYNAMICTABLE,
            """CREATE OR REPLACE DYNAMIC TABLE "MY_DB". "MY_SCHEMA". "MY_TABLE" (I INT);""",
            """CREATE OR REPLACE DYNAMIC TABLE "MY_DB". "MY_SCHEMA". "MY_TABLE"   (I INT);""",
        ),
    ],
)
def test_add_string_to_object_ddl_empty_input_string(object_type, object_statement, expected):
    input_string = ""
    result = pos.add_string_to_object_ddl(object_type, object_statement, input_string)
    assert result == expected


@pytest.mark.parametrize(
    "object_type, object_statement",
    [
        (
            pos.PolicyAssignmentObjectTypes.VIEW,
            """CREATE OR REPLACE TABLE MY_SCHEMA.MY_TABLE AS SELECT 1 I;""",
        ),
    ],
)
def test_add_string_to_object_ddl_raises_error(object_type, object_statement,):
    input_string = ""
    with pytest.raises(ValueError):
        __ = pos.add_string_to_object_ddl(object_type, object_statement, input_string)


@pytest.mark.parametrize(
    "view_definition, expected",
    [
        (
            """CREATE OR REPLACE VIEW MY_SCHEMA.MY_VIEW AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW MY_SCHEMA.MY_VIEW AS SELECT 1 I;""",
        ),
        (
            """CREATE OR REPLACE VIEW "MY_SCHEMA"."MY_VIEW" AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW "MY_SCHEMA"."MY_VIEW" AS SELECT 1 I;""",
        ),
        (
            """CREATE OR REPLACE VIEW MY_SCHEMA . MY_VIEW AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW MY_SCHEMA . MY_VIEW AS SELECT 1 I;""",
        ),
        (
            """CREATE OR REPLACE VIEW "MY_SCHEMA" . "MY_VIEW" AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW "MY_SCHEMA" . "MY_VIEW" AS SELECT 1 I;""",
        ),
        (
            """CREATE OR REPLACE VIEW MY_DB.MY_SCHEMA.MY_VIEW AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW MY_SCHEMA.MY_VIEW AS SELECT 1 I;""",
        ),
        (
            """CREATE OR REPLACE VIEW "MY_DB"."MY_SCHEMA"."MY_VIEW" AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW "MY_SCHEMA"."MY_VIEW" AS SELECT 1 I;""",
        ),
        (
            """CREATE OR REPLACE VIEW MY_DB . MY_SCHEMA . MY_VIEW AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW  MY_SCHEMA . MY_VIEW AS SELECT 1 I;""",
        ),
        (
            """CREATE OR REPLACE VIEW "MY_DB" . "MY_SCHEMA" . "MY_VIEW" AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW  "MY_SCHEMA" . "MY_VIEW" AS SELECT 1 I;""",
        ),
    ],
)
def test_remove_database_name_from_view_statement(view_definition, expected):
    result = pos.remove_database_name_from_view_statement(view_definition)
    assert result == expected