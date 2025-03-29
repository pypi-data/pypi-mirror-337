import re
from unittest.mock import patch

import acedeploy.core.model_solution_entities as mse
import pytest
from acedeploy.core.model_sql_entities import DbFunctionType, DbObjectType


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            """
CREATE OR REPLACE VIEW V1;
CREATE OR REPLACE VIEW V2;
""",
            True,
        ),
        (
            """
CREATE OR REPLACE VIEW V1;
""",
            False,
        ),
        (
            """
CREATE OR REPLACE VIEW V1
""",
            False,
        ),
        (
            """
CREATE OR REPLACE VIEW V1;
CREATE OR REPLACE VIEW V2;
CREATE OR REPLACE VIEW V3;
""",
            True,
        ),
        (
            """
CREATE OR REPLACE VIEW V1
AS SELECT 'test' VARCHAR(10);
""",
            False,
        ),
        (
            """
CREATE OR REPLACE VIEW V1
AS SELECT 'test;test' VARCHAR(10);
""",
            False,
        ),
        (
            """
CREATE OR REPLACE VIEW V1
AS SELECT 'test' VARCHAR(10);
CREATE OR REPLACE VIEW V2
AS SELECT 'test' VARCHAR(10);
""",
            True,
        ),
        (
            """
CREATE OR REPLACE VIEW V1
AS SELECT 'test;
test;' VARCHAR(10);
CREATE OR REPLACE VIEW V2
AS SELECT 'test;
test;' VARCHAR(10);
""",
            True,
        ),
        (
            """
CREATE OR REPLACE VIEW V1
AS SELECT 'test
test' VARCHAR(10);
CREATE OR REPLACE VIEW V2
AS SELECT 'test
test' VARCHAR(10);
""",
            True,
        ),
        (
            """
CREATE OR REPLACE VIEW V1
AS SELECT 'test;test' VARCHAR(10);
CREATE OR REPLACE VIEW V2
AS SELECT 'test;test' VARCHAR(10);
""",
            True,
        ),
        (
            """
CREATE OR REPLACE VIEW V1
AS SELECT 'test;test' VARCHAR(10);
CREATE OR REPLACE VIEW V2
AS SELECT 'test;test' VARCHAR(10);
""",
            True,
        ),
        (
            """
CREATE OR REPLACE VIEW V1
AS SELECT 'CREATE OR REPLACE VIEW V2
AS SELECT ''test;test'' VARCHAR(10);' VARCHAR(100);
""",
            False,
        ),
        (
            """
CREATE OR REPLACE PROCEDURE P1 ()
AS $$
code
$$;
""",
            False,
        ),
        (
            """
CREATE OR REPLACE PROCEDURE P1 ()
AS `
code
`;
""",
            False,
        ),
        (
            """
CREATE OR REPLACE PROCEDURE P1 ()
AS $$
code
$$;
CREATE OR REPLACE PROCEDURE P2 ()
AS $$
code
$$;
""",
            True,
        ),
        (
            """
CREATE OR REPLACE PROCEDURE P1 ()
AS $$
code
$$;
CREATE OR REPLACE VIEW V2 ()
AS SELECT 1 INT;
""",
            True,
        ),
    ],
)
def test_ddl_contains_multiple_statements(input, expected):
    # arrange
    content = input

    # act
    result = mse.SolutionObject._ddl_contains_multiple_statements(content)

    # assert
    assert bool(result) == expected


@pytest.mark.parametrize(
    "input, expected",
    [("myschema.myobject", "myobject"), ("MY_SCHEMA.MY_OBJECT", "MY_OBJECT")],
)
def test_get_object_name_from_name(input, expected):
    # act
    result = mse.SolutionObject._get_object_name_from_name(input)

    # assert
    assert result == expected


@pytest.mark.parametrize(
    "input, expected",
    [("myschema.myobject", "myschema"), ("MY_SCHEMA.MY_OBJECT", "MY_SCHEMA")],
)
def test_get_schema_name_from_name(input, expected):
    # act
    result = mse.SolutionObject._get_schema_name_from_name(input)

    # assert
    assert result == expected


@pytest.mark.parametrize(
    "input, error, error_message",
    [
        (
            "mydatabase.myschema.myobject",
            ValueError,
            "Name [ 'mydatabase.myschema.myobject' ] is not a valid object name with pattern [ 'schema_name.object_name' ]",
        ),
        (
            "myobject",
            ValueError,
            "Name [ 'myobject' ] is not a valid object name with pattern [ 'schema_name.object_name' ]",
        ),
    ],
)
def test_get_object_name_from_name_error(input, error, error_message):
    with pytest.raises(error, match=re.escape(error_message)):
        __ = mse.SolutionObject._get_object_name_from_name(input)


@pytest.mark.parametrize(
    "input, error, error_message",
    [
        (
            "mydatabase.myschema.myobject",
            ValueError,
            "Name [ 'mydatabase.myschema.myobject' ] is not a valid object name with pattern [ 'schema_name.object_name' ]",
        ),
        (
            "myschema",
            ValueError,
            "Name [ 'myschema' ] is not a valid object name with pattern [ 'schema_name.object_name' ]",
        ),
    ],
)
def test_get_schema_name_from_name_error(input, error, error_message):
    with pytest.raises(error, match=re.escape(error_message)):
        __ = mse.SolutionObject._get_schema_name_from_name(input)


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            "/home/me/source/sql/myschema/Tables/myschema.mytable.sql",
            "MYSCHEMA.MYTABLE",
        ),
        ("/home/me/source/sql/myschema/myschema.sql", "MYSCHEMA"),
        (
            "/home/me/source/sql/myschema/Tables/myschema.mytable.SQL",
            "MYSCHEMA.MYTABLE",
        ),
        ("/home/me/source/sql/myschema/myschema.SQL", "MYSCHEMA"),
        ("myschema.mytable.SQL", "MYSCHEMA.MYTABLE"),
        ("myschema.SQL", "MYSCHEMA"),
    ],
)
def test_get_full_name_from_filepath(input, expected):
    # act
    result = mse.SolutionObject._get_full_name_from_filepath(input)

    # assert
    assert result == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            """
            CREATE OR REPLACE PROCEDURE p_lew_process.m_load_control_end_app ()
            RETURNS STRING
            LANGUAGE JAVASCRIPT
            EXECUTE AS CALLER
            AS
            $$
                var sql_stmt = `UPDATE p_lew_process.t_current_execution_gtmp SET
            """,
            [],
        ),
        (
            "CREATE FUNCTION MYSCHEMA.MYFUNCTION (A VARCHAR, B INT, C INT)",
            ["VARCHAR", "INT", "INT"],
        ),
        (
            "CREATE PROCEDURE MYSCHEMA.MYPROC ()",
            [],
        ),
        (
            "CREATE PROCEDURE MYSCHEMA.MYPROC (  )",
            [],
        ),
        (
            "CREATE OR REPLACE FUNCTION MYSCHEMA.MYFUNCTION (A VARCHAR, B INT, C INT)",
            ["VARCHAR", "INT", "INT"],
        ),
        (
            """CREATE OR REPLACE FUNCTION "MYSCHEMA"."MYFUNCTION" (A VARCHAR, B INT, C INT)""",
            ["VARCHAR", "INT", "INT"],
        ),
        (
            """CREATE OR REPLACE FUNCTION MYSCHEMA.MYFUNCTION ("A" VARCHAR, "B" INT, "C" INT)""",
            ["VARCHAR", "INT", "INT"],
        ),
        (
            "CREATE OR REPLACE FUNCTION MYSCHEMA.MYFUNCTION(P_TABLE_NAME_I VARCHAR, P_TABLE_NAME_II VARCHAR, P_TABLE_NAME_III VARCHAR, P_TABLE_NAME_IV VARCHAR, P_TABLE_NAME_V VARCHAR)",
            ["VARCHAR", "VARCHAR", "VARCHAR", "VARCHAR", "VARCHAR"],
        ),
        (
            """
            CREATE OR REPLACE PROCEDURE P_LEW_MART_ANALYTICS.X_20200519_P_SCA_FILL_CLUSTER_DIST_TMP_2763040(P_TABLE_NAME_I VARCHAR, P_TABLE_NAME_II VARCHAR, P_TABLE_NAME_III VARCHAR, P_TABLE_NAME_IV VARCHAR, P_TABLE_NAME_V VARCHAR)
            RETURNS VARCHAR(16777216)
            LANGUAGE JAVASCRIPT
            EXECUTE AS OWNER
            AS '""",
            ["VARCHAR", "VARCHAR", "VARCHAR", "VARCHAR", "VARCHAR"],
        ),
        (
            """
            CREATE OR REPLACE PROCEDURE P_LEW_MART_ANALYTICS.X_20200519_P_SCA_FILL_CLUSTER_DIST_TMP_2763040(
                P_TABLE_NAME_I VARCHAR,
                P_TABLE_NAME_II VARCHAR
                , P_TABLE_NAME_III VARCHAR
                , P_TABLE_NAME_IV VARCHAR, P_TABLE_NAME_V VARCHAR)
            RETURNS VARCHAR(16777216)
            LANGUAGE JAVASCRIPT
            EXECUTE AS OWNER
            AS '""",
            ["VARCHAR", "VARCHAR", "VARCHAR", "VARCHAR", "VARCHAR"],
        ),
        (
            """
            CREATE OR REPLACE PROCEDURE P_LEW_MART_ANALYTICS.X_20200519_P_SCA_FILL_CLUSTER_DIST_TMP_2763040(P_TABLE_NAME_I VARCHAR, P_TABLE_NAME_II VARCHAR, P_TABLE_NAME_III VARCHAR, P_TABLE_NAME_IV VARCHAR, P_TABLE_NAME_V VARCHAR)
                RETURNS VARCHAR(16777216)
                LANGUAGE JAVASCRIPT
                EXECUTE AS OWNER
            """,
            ["VARCHAR", "VARCHAR", "VARCHAR", "VARCHAR", "VARCHAR"],
        ),
        (
            """
            CREATE OR REPLACE PROCEDURE p_lew_mart_msi.m_add_threshold_cumulation (I_REQUESTING_USER VARCHAR(128), P_TABLE_NAME_I FLOAT, I_REQUESTING_USER VARCHAR(128))
                RETURNS STRING
                LANGUAGE JAVASCRIPT
                EXECUTE AS OWNER
                AS
            """,
            ["VARCHAR", "FLOAT", "VARCHAR"],
        ),
        (
            """
            CREATE OR REPLACE PROCEDURE p_lew_mart_msi.m_add_threshold_cumulation ("I_REQUESTING_USER" VARCHAR(128), "P_TABLE_NAME_I FLOAT", I_REQUESTING_USER VARCHAR(128))
                RETURNS STRING
                LANGUAGE JAVASCRIPT
                EXECUTE AS OWNER
                AS
            """,
            ["VARCHAR", "FLOAT", "VARCHAR"],
        ),
        (
            """
            CREATE OR REPLACE PROCEDURE FE_MSTR_BGE_PALETTIERER.P_ADD_OR_UPDATE_SHIFT_REPORT_MESSAGES ("ALERTS_DAY_SHIFT_ID" FLOAT, "ALERTS_SHIFT_REPORT_AGREEMENT_TXT" VARCHAR(16777216), "ALERTS_SHIFT_REPORT_NEXT_SHIFT_TXT" VARCHAR(16777216), "ALERTS_SHIFT_REPORT_OUT_OF_ORDER_TXT" VARCHAR(16777216), "ALERTS_SHIFT_REPORT_SECURITY_ISSUES" VARCHAR(16777216))
                RETURNS STRING
                LANGUAGE JAVASCRIPT
            """,
            ["FLOAT", "VARCHAR", "VARCHAR", "VARCHAR", "VARCHAR"],
        ),
        (
            """
            CREATE OR REPLACE PROCEDURE MYSCHEMA.MYPROC (V1 VARCHAR( 10 ), V2 VARCHAR (10 ), V3 VARCHAR ( 10))
                RETURNS STRING
                LANGUAGE JAVASCRIPT
                EXECUTE AS OWNER
                AS
            """,
            ["VARCHAR", "VARCHAR", "VARCHAR"],
        ),
        (
            """
            CREATE FUNCTION TR_GLOBAL.F_CURRENCY_SHIFT (AMOUNT decimal(17, 5), CURX int )
            RETURNS DECIMAL(17, 2)
            AS
                'CAST(AMOUNT * POWER(10, 2 - COALESCE(CURX, 2)) as DECIMAL(17, 2))'
            ;
            """,
            ["DECIMAL", "INT"],
        ),
        (
            """
            CREATE FUNCTION
            TR_GLOBAL.F_CURRENCY_SHIFT (
                AMOUNT
                decimal(17,
                 5),
                  CURX
                   int
                   )
            RETURNS DECIMAL(17, 2)
            AS
            """,
            ["DECIMAL", "INT"],
        ),
    ],
)
def test_get_parameters_from_ddl(input, expected):
    # arrange
    ddl = input

    # act
    result = mse.SolutionParametersObject._get_parameters_from_ddl(ddl)

    # assert
    assert result == expected

@pytest.mark.parametrize(
    "input, expected",
    [
        (
            """
                create or replace procedure s.my_proc (
                    source_schema string
                    , source_table string
                    , target_schema string
                    , target_table string
                    , a_number number(38,0)
                    , insert_mode string default 'APPEND'
                    , truncate_stage boolean default false
                    , check_target_columns boolean default true
                    , ts timestamp default current_timestamp()
                )
                returns int null
                language sql
                ...
            """,
            [
                "STRING",
                "STRING",
                "STRING",
                "STRING",
                "NUMBER",
                "STRING",
                "BOOLEAN",
                "BOOLEAN",
                "TIMESTAMP",
            ],
        ),
        (
            """
                create or replace procedure s.my_proc (
                    source_schema string
                    , source_table string
                    , target_schema string
                    , target_table string
                    , a_number number(38,0)
                    , some_string string default 'hello string default \'hello\''
                )
                returns int null
                language sql
                ...
            """,
            [
                "STRING",
                "STRING",
                "STRING",
                "STRING",
                "NUMBER",
                "STRING",
            ],
        ),
        (
            """
                create or replace procedure s.my_proc (
                    source_schema string
                    , source_table string
                    , target_schema string
                    , target_table string
                    , a_number number(38,0)
                    , some_regex1 string default '.*'
                    , some_regex2 string default '[\d\s]*'
                )
                returns int null
                language sql
                ...
            """,
            [
                "STRING",
                "STRING",
                "STRING",
                "STRING",
                "NUMBER",
                "STRING",
                "STRING",
            ],
        ),
        (
            """
                create or replace procedure s.my_proc (
                    source_schema string
                    , source_table string
                    , target_schema string
                    , target_table string
                    , a_number number(38,0)
                    , some_special_chars string default '!"§$%&/=?*#~@_<>|{[]}\\+-$^'
                    , some_wierd_string string default '  a    a  '
                    , some_string_with_linebreak string default '
                        so
                        many
                        new
                        lines
                    '
                )
                returns int null
                language sql
                ...
            """,
            [
                "STRING",
                "STRING",
                "STRING",
                "STRING",
                "NUMBER",
                "STRING",
                "STRING",
                "STRING",
            ],
        ),
        (
            r"create or replace procedure s.p (a string default '\'hello world\'', b string default 'hi', c string default 'escaped \' single quote')",
            [
                "STRING",
                "STRING",
                "STRING",
            ],
        ),
        (
            r"create or replace procedure s.p (a string default '\'hello world\'', b string default 'hi', c string default 'escaped '' single quote')",
            [
                "STRING",
                "STRING",
                "STRING",
            ],
        ),
        (
            r"create or replace procedure s.p (a string default '1,2,3', b string default 'hello,world', c string default ',,,')",
            [
                "STRING",
                "STRING",
                "STRING",
            ],
        ),
        (
            """
            CREATE OR REPLACE PROCEDURE CORE.SP_LOADING_PROCEDURE_GENERATOR("SRC_TRANSF_VIEW_NAME" VARCHAR(16777216) DEFAULT 'IMPORT.VW_PRODUCT_20240808', "TRG_TABLE_NAME" VARCHAR(16777216) DEFAULT 'CORE.TBL_PRODUCT', "BK_COLUMN_NAMES" VARCHAR(16777216) DEFAULT 'BK_WHL_ITEM_NO', "TECH_COLUMN_NAMES" VARCHAR(16777216) DEFAULT 'DWH_INSERT_TS,DWH_UPDATE_TS,DWH_UNLOAD_TS')
RETURNS VARCHAR(16777216)
            """,
            [
                "VARCHAR",
                "VARCHAR",
                "VARCHAR",
                "VARCHAR",
            ]
        )
    ],
)
def test_get_parameters_from_ddl_with_defaults(input, expected):
    # arrange
    ddl = input

    # act
    result = mse.SolutionParametersObject._get_parameters_from_ddl(ddl)

    # assert
    assert result == expected

@pytest.mark.parametrize(
    "input, expected",
    [
        (
            """
                a string, b string, c number, d boolean
            """,
            [
                "a string",
                "b string",
                "c number",
                "d boolean",
            ],
        ),
        (
            """
                a string default 'hello world', b string, c number default 123, d boolean default true
            """,
            [
                "a string default 'hello world'",
                "b string",
                "c number default 123",
                "d boolean default true",
            ],
        ),
        (
            """
                a string default 'hello \' single quote', b string, c number default 123, d boolean default true
            """,
            [
                "a string default 'hello \' single quote'",
                "b string",
                "c number default 123",
                "d boolean default true",
            ],
        ),
        (
            """
                a string default 'hello \' multiple\' single quotes', b string, c number default 123, d boolean default true
            """,
            [
                "a string default 'hello \' multiple\' single quotes'",
                "b string",
                "c number default 123",
                "d boolean default true",
            ],
        ),
        (
            """
                a string default 'hello \' multiple\' single \' quotes', b string default '\'so\'many\'quotes\'', c number default 123, d boolean default true
            """,
            [
                "a string default 'hello \' multiple\' single \' quotes'",
                "b string default '\'so\'many\'quotes\''",
                "c number default 123",
                "d boolean default true",
            ],
        ),
    ],
)
def test__split_parameters(input, expected):
    # arrange
    ddl = input

    # act
    result = mse.SolutionParametersObject._split_parameters(ddl)

    # assert
    assert [r.strip() for r in result] == expected


# section object generation


def test_SolutionObject_not_instanietable():
    with pytest.raises(TypeError):
        mse.SolutionObject(
            "myschema",
            "myname",
            "/my/file/path/mytable.sql",
            "dummy content",
            DbObjectType.TABLE,
        )  # pylint: disable=abstract-class-instantiated


def test_SolutionParametersObject_not_instanietable():
    with pytest.raises(TypeError):
        mse.SolutionParametersObject(
            "myschema",
            "myname",
            "/my/file/path/mytable.sql",
            "dummy content",
            DbObjectType.TABLE,
        )  # pylint: disable=abstract-class-instantiated


@pytest.mark.parametrize(
    "path, mock_content, git_change_type, expected_dict",
    [
        (
            "/my/file/path/myschema.sql",
            "CREATE SCHEMA MYSCHEMA;",
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYSCHEMA",
                "full_name": "MYSCHEMA",
                "id": "DbObjectType.SCHEMA MYSCHEMA",
                "object_type": DbObjectType.SCHEMA,
                "repr": "SolutionSchema: DbObjectType.SCHEMA MYSCHEMA",
                "str": "SolutionSchema: DbObjectType.SCHEMA MYSCHEMA",
                "type": mse.SolutionSchema,
                "git_change_type": None,
            },
        ),
        (
            "/my/file/path/myschema.mytable.sql",
            "CREATE TABLE myschema.mytable (i int);",
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYTABLE",
                "full_name": "MYSCHEMA.MYTABLE",
                "id": "DbObjectType.TABLE MYSCHEMA.MYTABLE",
                "object_type": DbObjectType.TABLE,
                "repr": "SolutionTable: DbObjectType.TABLE MYSCHEMA.MYTABLE",
                "str": "SolutionTable: DbObjectType.TABLE MYSCHEMA.MYTABLE",
                "type": mse.SolutionTable,
                "git_change_type": None,
            },
        ),
        (
            "/my/file/path/myschema.mytable.sql",
            "CREATE TABLE myschema.mytable(i int);",
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYTABLE",
                "full_name": "MYSCHEMA.MYTABLE",
                "id": "DbObjectType.TABLE MYSCHEMA.MYTABLE",
                "object_type": DbObjectType.TABLE,
                "repr": "SolutionTable: DbObjectType.TABLE MYSCHEMA.MYTABLE",
                "str": "SolutionTable: DbObjectType.TABLE MYSCHEMA.MYTABLE",
                "type": mse.SolutionTable,
                "git_change_type": None,
            },
        ),
        (
            "/my/file/path/myschema.mytable.sql",
            "CREATE TRANSIENT TABLE myschema.mytable(i int);",
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYTABLE",
                "full_name": "MYSCHEMA.MYTABLE",
                "id": "DbObjectType.TABLE MYSCHEMA.MYTABLE",
                "object_type": DbObjectType.TABLE,
                "repr": "SolutionTable: DbObjectType.TABLE MYSCHEMA.MYTABLE",
                "str": "SolutionTable: DbObjectType.TABLE MYSCHEMA.MYTABLE",
                "type": mse.SolutionTable,
                "git_change_type": None,
            },
        ),
        (
            "/my/file/path/myschema.mytable.sql",
            "CREATE TABLE myschema.mytable (i int);",
            "A",
            {
                "schema": "MYSCHEMA",
                "name": "MYTABLE",
                "full_name": "MYSCHEMA.MYTABLE",
                "id": "DbObjectType.TABLE MYSCHEMA.MYTABLE",
                "object_type": DbObjectType.TABLE,
                "repr": "SolutionTable: DbObjectType.TABLE MYSCHEMA.MYTABLE",
                "str": "SolutionTable: DbObjectType.TABLE MYSCHEMA.MYTABLE",
                "type": mse.SolutionTable,
                "git_change_type": "A",
            },
        ),
        (
            "/my/file/path/myschema.myview.sql",
            "CREATE OR REPLACE VIEW myschema.myview as select * from myschema.mytable;",
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYVIEW",
                "full_name": "MYSCHEMA.MYVIEW",
                "id": "DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "object_type": DbObjectType.VIEW,
                "repr": "SolutionView: DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "str": "SolutionView: DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "type": mse.SolutionView,
                "git_change_type": None,
            },
        ),
        (
            "/my/file/path/myschema.myview.sql",
            'CREATE OR REPLACE VIEW "MYSCHEMA"."MYVIEW" as select * from myschema.mytable;',
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYVIEW",
                "full_name": "MYSCHEMA.MYVIEW",
                "id": "DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "object_type": DbObjectType.VIEW,
                "repr": "SolutionView: DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "str": "SolutionView: DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "type": mse.SolutionView,
                "git_change_type": None,
            },
        ),
        (
            "/my/file/path/myschema.myview.sql",
            "CREATE VIEW myschema.myview as select * from myschema.mytable;",
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYVIEW",
                "full_name": "MYSCHEMA.MYVIEW",
                "id": "DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "object_type": DbObjectType.VIEW,
                "repr": "SolutionView: DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "str": "SolutionView: DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "type": mse.SolutionView,
                "git_change_type": None,
            },
        ),
        (
            "/my/file/path/myschema.myview.sql",
            "  CREATE  VIEW    myschema.myview   as     select * from  myschema.mytable ;   ",
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYVIEW",
                "full_name": "MYSCHEMA.MYVIEW",
                "id": "DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "object_type": DbObjectType.VIEW,
                "repr": "SolutionView: DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "str": "SolutionView: DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "type": mse.SolutionView,
                "git_change_type": None,
            },
        ),
        (
            "/my/file/path/myschema.myview.sql",
            'CREATE OR REPLACE VIEW "myschema"."myview" as select * from myschema.mytable;',
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYVIEW",
                "full_name": "MYSCHEMA.MYVIEW",
                "id": "DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "object_type": DbObjectType.VIEW,
                "repr": "SolutionView: DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "str": "SolutionView: DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "type": mse.SolutionView,
                "git_change_type": None,
            },
        ),
        (
            "/my/file/path/myschema.myview.sql",
            'CREATE OR REPLACE SECURE VIEW "myschema"."myview" as select * from myschema.mytable;',
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYVIEW",
                "full_name": "MYSCHEMA.MYVIEW",
                "id": "DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "object_type": DbObjectType.VIEW,
                "repr": "SolutionView: DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "str": "SolutionView: DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "type": mse.SolutionView,
                "git_change_type": None,
            },
        ),
        (
            "/my/file/path/myschema.myview.sql",
            'CREATE OR REPLACE RECURSIVE VIEW "myschema"."myview" as select * from myschema.mytable;',
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYVIEW",
                "full_name": "MYSCHEMA.MYVIEW",
                "id": "DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "object_type": DbObjectType.VIEW,
                "repr": "SolutionView: DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "str": "SolutionView: DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "type": mse.SolutionView,
                "git_change_type": None,
            },
        ),
        (
            "/my/file/path/myschema.myview.sql",
            'CREATE OR REPLACE SECURE RECURSIVE VIEW "myschema"."myview" as select * from myschema.mytable;',
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYVIEW",
                "full_name": "MYSCHEMA.MYVIEW",
                "id": "DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "object_type": DbObjectType.VIEW,
                "repr": "SolutionView: DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "str": "SolutionView: DbObjectType.VIEW MYSCHEMA.MYVIEW",
                "type": mse.SolutionView,
                "git_change_type": None,
            },
        ),
        (
            "/my/file/path/myschema.myview.sql",
            "CREATE OR REPLACE MATERIALIZED VIEW myschema.myview  s select * from myschema.mytable;",
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYVIEW",
                "full_name": "MYSCHEMA.MYVIEW",
                "id": "DbObjectType.MATERIALIZEDVIEW MYSCHEMA.MYVIEW",
                "object_type": DbObjectType.MATERIALIZEDVIEW,
                "repr": "SolutionMaterializedView: DbObjectType.MATERIALIZEDVIEW MYSCHEMA.MYVIEW",
                "str": "SolutionMaterializedView: DbObjectType.MATERIALIZEDVIEW MYSCHEMA.MYVIEW",
                "type": mse.SolutionMaterializedView,
                "git_change_type": None,
            },
        ),
        (
            "/my/file/path/myschema.mystage.sql",
            "CREATE OR REPLACE STAGE myschema.mystage COPY OPTIONS = (...);",
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYSTAGE",
                "full_name": "MYSCHEMA.MYSTAGE",
                "id": "DbObjectType.STAGE MYSCHEMA.MYSTAGE",
                "object_type": DbObjectType.STAGE,
                "repr": "SolutionStage: DbObjectType.STAGE MYSCHEMA.MYSTAGE",
                "str": "SolutionStage: DbObjectType.STAGE MYSCHEMA.MYSTAGE",
                "type": mse.SolutionStage,
                "git_change_type": None,
            },
        ),
        (
            "/my/file/path/myschema.MYFUNCTION.sql",
            "CREATE OR REPLACE FUNCTION MYSCHEMA.MYFUNCTION () AS ...",
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYFUNCTION",
                "full_name": "MYSCHEMA.MYFUNCTION ()",
                "id": "DbObjectType.FUNCTION MYSCHEMA.MYFUNCTION ()",
                "object_type": DbObjectType.FUNCTION,
                "repr": "SolutionFunction: DbObjectType.FUNCTION MYSCHEMA.MYFUNCTION ()",
                "str": "SolutionFunction: DbObjectType.FUNCTION MYSCHEMA.MYFUNCTION ()",
                "type": mse.SolutionFunction,
                "parameters": [],
                "parameters_string": "()",
                "git_change_type": None,
                "function_type": DbFunctionType.SQL,
            },
        ),
        (
            "/my/file/path/myschema.MYFUNCTION.sql",
            "CREATE OR REPLACE FUNCTION MYSCHEMA.MYFUNCTION (V VARCHAR) LANGUAGE JAVASCRIPT AS ...",
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYFUNCTION",
                "full_name": "MYSCHEMA.MYFUNCTION (VARCHAR)",
                "id": "DbObjectType.FUNCTION MYSCHEMA.MYFUNCTION (VARCHAR)",
                "object_type": DbObjectType.FUNCTION,
                "repr": "SolutionFunction: DbObjectType.FUNCTION MYSCHEMA.MYFUNCTION (VARCHAR)",
                "str": "SolutionFunction: DbObjectType.FUNCTION MYSCHEMA.MYFUNCTION (VARCHAR)",
                "type": mse.SolutionFunction,
                "parameters": ["VARCHAR"],
                "parameters_string": "(VARCHAR)",
                "git_change_type": None,
                "function_type": DbFunctionType.JAVASCRIPT,
            },
        ),
        (
            "/my/file/path/myschema.myprocedure.sql",
            "CREATE OR REPLACE PROCEDURE MYSCHEMA.MYPROCEDURE () AS ...",
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYPROCEDURE",
                "full_name": "MYSCHEMA.MYPROCEDURE ()",
                "id": "DbObjectType.PROCEDURE MYSCHEMA.MYPROCEDURE ()",
                "object_type": DbObjectType.PROCEDURE,
                "repr": "SolutionProcedure: DbObjectType.PROCEDURE MYSCHEMA.MYPROCEDURE ()",
                "str": "SolutionProcedure: DbObjectType.PROCEDURE MYSCHEMA.MYPROCEDURE ()",
                "type": mse.SolutionProcedure,
                "parameters": [],
                "parameters_string": "()",
                "git_change_type": None,
            },
        ),
        (
            "/my/file/path/myschema.myprocedure.sql",
            "CREATE OR REPLACE PROCEDURE MYSCHEMA.MYPROCEDURE (V VARCHAR) AS ...",
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYPROCEDURE",
                "full_name": "MYSCHEMA.MYPROCEDURE (VARCHAR)",
                "id": "DbObjectType.PROCEDURE MYSCHEMA.MYPROCEDURE (VARCHAR)",
                "object_type": DbObjectType.PROCEDURE,
                "repr": "SolutionProcedure: DbObjectType.PROCEDURE MYSCHEMA.MYPROCEDURE (VARCHAR)",
                "str": "SolutionProcedure: DbObjectType.PROCEDURE MYSCHEMA.MYPROCEDURE (VARCHAR)",
                "type": mse.SolutionProcedure,
                "parameters": ["VARCHAR"],
                "parameters_string": "(VARCHAR)",
                "git_change_type": None,
            },
        ),
        (
            "/my/file/path/myschema.mytask.sql",
            "CREATE OR REPLACE TASK myschema.mytask ...;",
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYTASK",
                "full_name": "MYSCHEMA.MYTASK",
                "id": "DbObjectType.TASK MYSCHEMA.MYTASK",
                "object_type": DbObjectType.TASK,
                "repr": "SolutionTask: DbObjectType.TASK MYSCHEMA.MYTASK",
                "str": "SolutionTask: DbObjectType.TASK MYSCHEMA.MYTASK",
                "type": mse.SolutionTask,
                "git_change_type": None,
            },
        ),
        (
            "/my/file/path/myschema.myPIPE.sql",
            "CREATE OR REPLACE PIPE myschema.myPIPE COPY OPTIONS = (...);",
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYPIPE",
                "full_name": "MYSCHEMA.MYPIPE",
                "id": "DbObjectType.PIPE MYSCHEMA.MYPIPE",
                "object_type": DbObjectType.PIPE,
                "repr": "SolutionPipe: DbObjectType.PIPE MYSCHEMA.MYPIPE",
                "str": "SolutionPipe: DbObjectType.PIPE MYSCHEMA.MYPIPE",
                "type": mse.SolutionPipe,
                "git_change_type": None,
            },
        ),
        (
            "/my/file/path/myschema.mySTREAM.sql",
            "CREATE OR REPLACE STREAM myschema.mySTREAM COPY OPTIONS = (...);",
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYSTREAM",
                "full_name": "MYSCHEMA.MYSTREAM",
                "id": "DbObjectType.STREAM MYSCHEMA.MYSTREAM",
                "object_type": DbObjectType.STREAM,
                "repr": "SolutionStream: DbObjectType.STREAM MYSCHEMA.MYSTREAM",
                "str": "SolutionStream: DbObjectType.STREAM MYSCHEMA.MYSTREAM",
                "type": mse.SolutionStream,
                "git_change_type": None,
            },
        ),
        (
            "/my/file/path/myschema.mySEQUENCE.sql",
            "CREATE OR REPLACE SEQUENCE myschema.mySEQUENCE ...;",
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYSEQUENCE",
                "full_name": "MYSCHEMA.MYSEQUENCE",
                "id": "DbObjectType.SEQUENCE MYSCHEMA.MYSEQUENCE",
                "object_type": DbObjectType.SEQUENCE,
                "repr": "SolutionSequence: DbObjectType.SEQUENCE MYSCHEMA.MYSEQUENCE",
                "str": "SolutionSequence: DbObjectType.SEQUENCE MYSCHEMA.MYSEQUENCE",
                "type": mse.SolutionSequence,
                "git_change_type": None,
            },
        ),
        (
            "/my/file/path/myschema.mymaskingpolicy.sql",
            "CREATE OR REPLACE MASKING POLICY myschema.mymaskingpolicy ...;",
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYMASKINGPOLICY",
                "full_name": "MYSCHEMA.MYMASKINGPOLICY",
                "id": "DbObjectType.MASKINGPOLICY MYSCHEMA.MYMASKINGPOLICY",
                "object_type": DbObjectType.MASKINGPOLICY,
                "repr": "SolutionMaskingPolicy: DbObjectType.MASKINGPOLICY MYSCHEMA.MYMASKINGPOLICY",
                "str": "SolutionMaskingPolicy: DbObjectType.MASKINGPOLICY MYSCHEMA.MYMASKINGPOLICY",
                "type": mse.SolutionMaskingPolicy,
                "git_change_type": None,
            },
        ),
        (
            "/my/file/path/myschema.myrowaccesspolicy.sql",
            "CREATE OR REPLACE ROW ACCESS POLICY myschema.myrowaccesspolicy ...;",
            None,
            {
                "schema": "MYSCHEMA",
                "name": "MYROWACCESSPOLICY",
                "full_name": "MYSCHEMA.MYROWACCESSPOLICY",
                "id": "DbObjectType.ROWACCESSPOLICY MYSCHEMA.MYROWACCESSPOLICY",
                "object_type": DbObjectType.ROWACCESSPOLICY,
                "repr": "SolutionRowAccessPolicy: DbObjectType.ROWACCESSPOLICY MYSCHEMA.MYROWACCESSPOLICY",
                "str": "SolutionRowAccessPolicy: DbObjectType.ROWACCESSPOLICY MYSCHEMA.MYROWACCESSPOLICY",
                "type": mse.SolutionRowAccessPolicy,
                "git_change_type": None,
            },
        ),
    ],
)
def test_SolutionObject_factory(path, mock_content, git_change_type, expected_dict):
    with patch("aceutils.file_util.load") as mock_load:
        mock_load.return_value = mock_content
        obj = mse.SolutionObject.factory(path, git_change_type)
    assert obj.path == path
    assert (
        obj.content.strip() == mock_content.strip()
    )  # strip because remove_comment_after_statement() might remove some whitespace
    assert obj.schema == expected_dict["schema"]
    assert obj.name == expected_dict["name"]
    assert obj.full_name == expected_dict["full_name"]
    assert obj.id == expected_dict["id"]
    assert obj.object_type == expected_dict["object_type"]
    assert repr(obj) == expected_dict["repr"]
    assert str(obj) == expected_dict["str"]
    assert type(obj) == expected_dict["type"]
    assert obj.git_change_type == expected_dict["git_change_type"]
    if "parameters" in expected_dict:
        assert obj.parameters == expected_dict["parameters"]
    if "parameters_string" in expected_dict:
        assert obj.parameters_string == expected_dict["parameters_string"]
    if "function_type" in expected_dict:
        assert obj.function_type == expected_dict["function_type"]


@pytest.mark.parametrize(
    "mock_content, string_replace_dict, expected_content",
    [
        (
            "CREATE TABLE myschema.%%var1%% (i int);",
            {"var1": "val1"},
            "CREATE TABLE myschema.val1 (i int);",
        ),
        (
            "CREATE TABLE myschema.MY_TABLE (i int comment='%%var1%%');",
            {"var2": "val1"},
            "CREATE TABLE myschema.MY_TABLE (i int comment='%%var1%%');",
        ),
        (
            "CREATE TABLE myschema.%%var1%%%%var2%% (i int);",
            {"var1": "MY_", "var2": "TABLE"},
            "CREATE TABLE myschema.MY_TABLE (i int);",
        ),
    ],
)
def test_SolutionObject_factory_replace_string(
    mock_content, string_replace_dict, expected_content
):
    with patch("aceutils.file_util.load") as mock_load:
        mock_load.return_value = mock_content
        obj = mse.SolutionObject.factory(
            "path/to/file.sql", string_replace_dict=string_replace_dict
        )
    assert obj.content.strip() == expected_content.strip()


@pytest.mark.parametrize(
    "path, mock_content",
    [
        ("/my/file/path/myschema.sql", "CREATE SCHEMA MY_DB.MYSCHEMA;"),
        (
            "/my/file/path/myschema.myobj.sql",
            "CREATE TABLE mydb.myschema.myobj (i int);",
        ),
        ("/my/file/path/myschema.myobj.sql", "CREATE TABLE myobj (i int);"),
        (
            "/my/file/path/myschema.myobj.sql",
            "CREATE VIEW mydb.myschema.myobj as select;",
        ),
        ("/my/file/path/myschema.myobj.sql", "CREATE VIEW myobj as select;"),
        (
            "/my/file/path/myschema.myobj.sql",
            "CREATE MATERIALIZED VIEW mydb.myschema.myobj as select;",
        ),
        (
            "/my/file/path/myschema.myobj.sql",
            "CREATE MATERIALIZED VIEW myobj as select;",
        ),
        ("/my/file/path/myschema.myobj.sql", "CREATE STAGE mydb.myschema.myobj ...;"),
        ("/my/file/path/myschema.myobj.sql", "CREATE STAGE myobj ...;"),
        (
            "/my/file/path/myschema.myobj.sql",
            "CREATE FILE FORMAT mydb.myschema.myobj ...;",
        ),
        ("/my/file/path/myschema.myobj.sql", "CREATE FILE FORMAT myobj ...;"),
        (
            "/my/file/path/myschema.myobj.sql",
            "CREATE FUNCTION mydb.myschema.myobj() ...;",
        ),
        ("/my/file/path/myschema.myobj.sql", "CREATE FUNCTION myobj() ...;"),
        (
            "/my/file/path/myschema.myobj.sql",
            "CREATE PROCEDURE mydb.myschema.myobj() ...;",
        ),
        ("/my/file/path/myschema.myobj.sql", "CREATE PROCEDURE myobj() ...;"),
        ("/my/file/path/myschema.myobj.sql", "CREATE TASK mydb.myschema.myobj ...;"),
        ("/my/file/path/myschema.myobj.sql", "CREATE TASK myobj ...;"),
        ("/my/file/path/myschema.myobj.sql", "CREATE PIPE mydb.myschema.myobj ...;"),
        ("/my/file/path/myschema.myobj.sql", "CREATE PIPE myobj ...;"),
        ("/my/file/path/myschema.myobj.sql", "CREATE STREAM mydb.myschema.myobj ...;"),
        ("/my/file/path/myschema.myobj.sql", "CREATE STREAM myobj ...;"),
        (
            "/my/file/path/myschema.myobj.sql",
            "CREATE SEQUENCE mydb.myschema.myobj ...;",
        ),
        ("/my/file/path/myschema.myobj.sql", "CREATE SEQUENCE myobj ...;"),
        ("/my/file/path/myschema.myobj.sql", "CREATE MASKING POLICY myobj ...;"),
        ("/my/file/path/myschema.myobj.sql", "CREATE ROW ACCESS POLICY myobj ...;"),
    ],
)
def test_SolutionObject_factory_no_match(path, mock_content):
    with patch("aceutils.file_util.load") as mock_load:
        mock_load.return_value = mock_content
        obj = mse.SolutionObject.factory(path)
    assert obj is None


@pytest.mark.parametrize(
    "myclass, path, git_change_type, content, expected",
    [
        (
            mse.SolutionSchema,
            "/my/file/path/myschema.sql",
            None,
            "CREATE SCHEMA MYSCHEMA ...",
            "DbObjectType.SCHEMA MYSCHEMA",
        ),
        (
            mse.SolutionTable,
            "/my/file/path/myschema.mytable.sql",
            None,
            "CREATE TABLE MYSCHEMA.MYTABLE ...",
            "DbObjectType.TABLE MYSCHEMA.MYTABLE",
        ),
        (
            mse.SolutionView,
            "/my/file/path/myschema.myview.sql",
            None,
            "CREATE VIEW MYSCHEMA.MYVIEW ...",
            "DbObjectType.VIEW MYSCHEMA.MYVIEW",
        ),
        (
            mse.SolutionMaterializedView,
            "/my/file/path/myschema.mymatview.sql",
            None,
            "CREATE MATERIALIZED VIEW MYSCHEMA.MYMATVIEW ...",
            "DbObjectType.MATERIALIZEDVIEW MYSCHEMA.MYMATVIEW",
        ),
        (
            mse.SolutionFileformat,
            "/my/file/path/myschema.myfileformat.sql",
            None,
            "CREATE FILE FORMAT MYSCHEMA.MYFILEFORMAT ...",
            "DbObjectType.FILEFORMAT MYSCHEMA.MYFILEFORMAT",
        ),
        (
            mse.SolutionExternalTable,
            "/my/file/path/myschema.myexttable.sql",
            None,
            "CREATE EXTERNAL TABLE MYSCHEMA.MYEXTTABLE ...",
            "DbObjectType.EXTERNALTABLE MYSCHEMA.MYEXTTABLE",
        ),
        (
            mse.SolutionStage,
            "/my/file/path/myschema.mystage.sql",
            None,
            "CREATE STAGE MYSCHEMA.MYSTAGE ...",
            "DbObjectType.STAGE MYSCHEMA.MYSTAGE",
        ),
        (
            mse.SolutionFunction,
            "/my/file/path/myschema.myfunction.sql",
            None,
            "CREATE OR REPLACE FUNCTION MYSCHEMA.MYFUNCTION (V VARCHAR) AS ...",
            "DbObjectType.FUNCTION MYSCHEMA.MYFUNCTION (VARCHAR)",
        ),
        (
            mse.SolutionProcedure,
            "/my/file/path/myschema.myprocedure.sql",
            None,
            "CREATE OR REPLACE PROCEDURE MYSCHEMA.MYPROCEDURE (V VARCHAR) AS ...",
            "DbObjectType.PROCEDURE MYSCHEMA.MYPROCEDURE (VARCHAR)",
        ),
        (
            mse.SolutionStream,
            "/my/file/path/myschema.mystream.sql",
            None,
            "CREATE STREAM MYSCHEMA.MYSTREAM ...",
            "DbObjectType.STREAM MYSCHEMA.MYSTREAM",
        ),
        (
            mse.SolutionTask,
            "/my/file/path/myschema.mytask.sql",
            None,
            "CREATE TASK MYSCHEMA.MYTASK ...",
            "DbObjectType.TASK MYSCHEMA.MYTASK",
        ),
        (
            mse.SolutionPipe,
            "/my/file/path/myschema.mypipe.sql",
            None,
            "CREATE PIPE MYSCHEMA.MYPIPE ...",
            "DbObjectType.PIPE MYSCHEMA.MYPIPE",
        ),
        (
            mse.SolutionSequence,
            "/my/file/path/myschema.mysequence.sql",
            None,
            "CREATE SEQUENCE MYSCHEMA.MYSEQUENCE ...",
            "DbObjectType.SEQUENCE MYSCHEMA.MYSEQUENCE",
        ),
        (
            mse.SolutionMaskingPolicy,
            "/my/file/path/myschema.mymaskingpolicy.sql",
            None,
            "CREATE MASKING POLICY MYSCHEMA.MYMASKINGPOLICY ...",
            "DbObjectType.MASKINGPOLICY MYSCHEMA.MYMASKINGPOLICY",
        ),
        (
            mse.SolutionRowAccessPolicy,
            "/my/file/path/myschema.myrowaccesspolicy.sql",
            None,
            "CREATE ROW ACCESS POLICY MYSCHEMA.MYROWACCESSPOLICY ...",
            "DbObjectType.ROWACCESSPOLICY MYSCHEMA.MYROWACCESSPOLICY",
        ),
        (
            mse.SolutionDynamicTable,
            "/my/file/path/myschema.mydynamictable.sql",
            None,
            "CREATE DYNAMIC TABLE MYSCHEMA.MYDYNAMICTABLE ...",
            "DbObjectType.DYNAMICTABLE MYSCHEMA.MYDYNAMICTABLE",
        ),
        (
            mse.SolutionNetworkRule,
            "/my/file/path/myschema.mynetworkrule.sql",
            None,
            "CREATE NETWORK RULE MYSCHEMA.MYNETWORKRULE ...",
            "DbObjectType.NETWORKRULE MYSCHEMA.MYNETWORKRULE",
        ),
    ],
)
def test_SolutionObject_id(myclass, path, git_change_type, content, expected):
    # directly test object generation (without factory)
    obj = myclass(path, content, git_change_type)
    assert obj.id == expected


# endsection object generation


@pytest.mark.parametrize(
    "file_content, expected",
    [
        (
            """
        CREATE TABLE S.T (I INT);
        """,
            """
        CREATE TABLE S.T (I INT);
        """,
        ),
        (
            """
        CREATE TABLE S.T (I INT);
        -- comment
        """,
            """
        CREATE TABLE S.T (I INT);
        """,
        ),
        (
            """
        CREATE TABLE S.T (I INT); -- comment
        """,
            """
        CREATE TABLE S.T (I INT);
        """,
        ),
    ],
)
def test_load_sql_file(file_content, expected):
    with patch("aceutils.file_util.load") as mock_load:
        mock_load.return_value = file_content
        result = mse.SolutionObject._load_sql_file("/dummy/path/file.sql")
    assert result.strip() == expected.strip()


@pytest.mark.parametrize(
    "file_content",
    [
        (
            """
        CREATE TABLE S.T1 (I INT);
        CREATE TABLE S.T2 (I INT);
        """
        )
    ],
)
def test_load_sql_file_error(file_content):
    with pytest.raises(Exception):
        with patch("aceutils.file_util.load") as mock_load:
            mock_load.return_value = file_content
            __ = mse.SolutionObject._load_sql_file("/dummy/path/file.sql")


@pytest.mark.parametrize(
    "statement, expected",
    [
        (
            """
CREATE OR REPLACE FUNCTION DBP_PROCESS.TRANSCRIPTC(STR VARCHAR)
RETURNS VARCHAR(16777216)
LANGUAGE JAVASCRIPT
COMMENT='Cyrillic to Latin'
AS '
   var answer = ""
      , a = {};

        """,
            DbFunctionType.JAVASCRIPT,
        ),
        (
            """
create or replace function dbp_process.transcriptc()
returns varchar(16777216)
language javascript
comment='cyrillic to latin'
as '
   var answer = ""
      , a = {};

        """,
            DbFunctionType.JAVASCRIPT,
        ),
        (
            """
create secure function dbp_process.transcriptc()
returns varchar(16777216)
language sql
comment='cyrillic to latin'
as
$$
$$
        """,
            DbFunctionType.SQL,
        ),
        (
            """
CREATE function PROCFUNC.area(radius float)
  returns float
  as
  $$
    pi() * radius * radius
  $$
  ;
        """,
            DbFunctionType.SQL,
        ),
    ],
)
def test_get_function_type(statement, expected):
    result = mse.SolutionFunction.get_function_type(statement)
    assert result == expected
