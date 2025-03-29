import aceutils.string_util as string_util
import pytest


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            """
SELECT * FROM table WHERE a = b
""",
            """
SELECT * FROM table WHERE a = b
""",
        ),
        (
            """
    SELECT *
    FROM -- here is a commment
    table
    WHERE a= b //maybe better statement
""",
            """
    SELECT *
    FROM 
    table
    WHERE a= b 
""",
        ),
        (
            """
    /*
     * Here we have a doc comment
     * Documenting the table
     */
    SELECT * FROM table
""",
            """
    SELECT * FROM table
""",
        ),
        (
            """
    /*
        Comment
        /* Nested multi line comment */
        /* Even if there are multiple of nested */
    */
    SELECT * FROM table
""",
            """
    SELECT * FROM table
""",
        ),
        (
            """
    /*
        Comment
        /* Nested multi line comment */
        /* Even if there are multiple of nested */
    */
    SELECT 
        ColumnA
        ,ColumnB -- Single Line comment
        ,ColumnC --Another Single line comment
    FROM table
    WHERE
    -- not this
    ColumnA = 'value'
    -- AND ColumnC = 'value'
    /* Final thoughts
        Execution is very slow
    */
""",
            """
    SELECT 
        ColumnA
        ,ColumnB 
        ,ColumnC 
    FROM table
    WHERE
    
    ColumnA = 'value'
""",
        ),
        (
            """
CREATE SCHEMA dbp_data;
/* Test comment */
""",
            """
CREATE SCHEMA dbp_data;
""",
        ),
        (
            """
CREATE SCHEMA dbp_data;
-- test comment
""",
            """
CREATE SCHEMA dbp_data;
""",
        ),
        (
            """
CREATE SCHEMA dbp_data;
//test comment
""",
            """
CREATE SCHEMA dbp_data;
""",
        ),
        (
            """
/* Test comment */
CREATE SCHEMA dbp_data;
""",
            """
CREATE SCHEMA dbp_data;
""",
        ),
        (
            """
-- test comment
CREATE SCHEMA dbp_data;
""",
            """
CREATE SCHEMA dbp_data;
""",
        ),
        (
            """
CREATE TABLE dbp_data.test (
/* Test comment */
id INT);
""",
            """
CREATE TABLE dbp_data.test (

id INT);
""",
        ),
        (
            """
CREATE TABLE dbp_data.test (
/* A long 
test comment */
id INT);
""",
            """
CREATE TABLE dbp_data.test (


id INT);
""",
        ),
        (
            """
CREATE TABLE dbp_data.test (
id INT, -- value1
b BYTE /* value2 */);
""",
            """
CREATE TABLE dbp_data.test (
id INT, 
b BYTE );
""",
        ),
        (
            """
INSERT INTO dbp_data.test VALUES (
'--test', --testcomment
'/*test*/', /*testcomment*/
'//test' //testcomment
);
""",
            """
INSERT INTO dbp_data.test VALUES (
'--test', 
'/*test*/', 
'//test' 
);
""",
        ),
        (
            """
INSERT INTO dbp_data.test VALUES (
'--', 
);
""",
            """
INSERT INTO dbp_data.test VALUES (
'--', 
);
""",
        ),
        (
            """
INSERT INTO dbp_data.test VALUES (
'test with ''quotes'' in values', 
);
""",
            """
INSERT INTO dbp_data.test VALUES (
'test with ''quotes'' in values', 
);
""",
        ),
        (
            """
INSERT INTO dbp_data.test VALUES (
'test with ''/*comment*/'' in values', 
);
""",
            """
INSERT INTO dbp_data.test VALUES (
'test with ''/*comment*/'' in values', 
);
""",
        ),
        (
            """
INSERT INTO dbp_data.test VALUES (
'test with ''--comment'' in values', 
);
""",
            """
INSERT INTO dbp_data.test VALUES (
'test with ''--comment'' in values', 
);
""",
        ),
        (
            """
, COALESCE(v03.wup_str, v01.wup_str, '')           AS wup_str
LEFT JOIN dbp_view.v_vaus_wup  v03
ON v01.wup_id = v03.wup_id 
AND v01.mandant_id = v03.mandant_id

UNION ALL

SELECT
  -1 AS mandant_id
, -1 AS nb_id
, '--' AS land_id
, 0 AS wup_id
, 'unknown' AS wup_standort
, 0 AS DUMMY
, 0 AS vs_id
, 0 AS gf_id
, 0 AS vkl_id
, 0 AS wm_id
, 0 AS hl_id
, 0 AS vw_id
, 0 AS vf_id
, 0 AS region_id
, '' AS wup_str
, '' AS wup_plz
, '' AS wup_stadt
, 0 AS breitengrad
, 0 AS laengengrad

FROM dbp_view.v_mandant
WHERE mandant_id = 1;
""",
            """
, COALESCE(v03.wup_str, v01.wup_str, '')           AS wup_str
LEFT JOIN dbp_view.v_vaus_wup  v03
ON v01.wup_id = v03.wup_id 
AND v01.mandant_id = v03.mandant_id

UNION ALL

SELECT
  -1 AS mandant_id
, -1 AS nb_id
, '--' AS land_id
, 0 AS wup_id
, 'unknown' AS wup_standort
, 0 AS DUMMY
, 0 AS vs_id
, 0 AS gf_id
, 0 AS vkl_id
, 0 AS wm_id
, 0 AS hl_id
, 0 AS vw_id
, 0 AS vf_id
, 0 AS region_id
, '' AS wup_str
, '' AS wup_plz
, '' AS wup_stadt
, 0 AS breitengrad
, 0 AS laengengrad

FROM dbp_view.v_mandant
WHERE mandant_id = 1;
""",
        ),
        (
            """
CREATE OR REPLACE VIEW s.v
AS SELECT 1 AS eins,
/* comment
-- comment */
2 as zwei,
/* comment //comment */
3 as drei;
""",
            """
CREATE OR REPLACE VIEW s.v
AS SELECT 1 AS eins,


2 as zwei,

3 as drei;
""",
        ),
        (
            """
CREATE OR REPLACE VIEW s.v
-- linecomment
-- linecomment */*/
/* block
comment */
2 as zwei,
-- linecomment */
3 as drei;
""",
            """
CREATE OR REPLACE VIEW s.v




2 as zwei,

3 as drei;
""",
        ),
        (
            """SELECT
* FROM x.y;
--comment;""",
            """SELECT
* FROM x.y;""",
        ),
        (
            """SELECT
* FROM x.y;
//comment;""",
            """SELECT
* FROM x.y;""",
        ),
        (
            """
// comment
CREATE OR REPLACE TABLE
// comment
(a INT, // comment
// comment
b INT)
// comment
;
// comment
""",
            """

CREATE OR REPLACE TABLE

(a INT, 

b INT)

;

""",
        ),
        (
            """
/* 
comment
comment
*/
CREATE OR REPLACE TABLE
/* comment
comment
comment */
(a INT, /* comment
comment */
/* comment 
*/
b INT)
/* comment */
;
/* comment 
comment */
""",
            """




CREATE OR REPLACE TABLE



(a INT, 



b INT)

;


""",
        ),
        (
            """
// comment
CREATE OR REPLACE TABLE
// comment
(a INT, // comment
// comment
b INT)
// comment
;
// comment
""",
            """

CREATE OR REPLACE TABLE

(a INT, 

b INT)

;

""",
        ),
        (
            """
CREATE ...
convert($$--this must be kept$$)
JOIN xyz
""",
            """
CREATE ...
convert($$--this must be kept$$)
JOIN xyz
""",
        ),
        (
            """
CREATE ...
convert($$/*this must be kept*/$$)
JOIN xyz
""",
            """
CREATE ...
convert($$/*this must be kept*/$$)
JOIN xyz
""",
        ),
        (
            """
CREATE ...
convert($$/*this must 
be kept*/$$)
JOIN xyz
""",
            """
CREATE ...
convert($$/*this must 
be kept*/$$)
JOIN xyz
""",
        ),
        (
            """
CREATE ...
convert($$keep$$--remove)
)JOIN xyz
""",
            """
CREATE ...
convert($$keep$$
)JOIN xyz
""",
        ),
        (
            """
CREATE ...
convert($$keep$$/*remove)
*/
)JOIN xyz
""",
            """
CREATE ...
convert($$keep$$

)JOIN xyz
""",
        ),
    ],
)
def test_remove_comment(input, expected):
    # arrange
    ddl = input

    # act
    result = string_util.remove_comment(ddl)

    # assert
    assert result.strip() == expected.strip()


def test_remove_comment_none_returns_none():
    # arrange
    ddl = None

    # act
    result = string_util.remove_comment(ddl)

    # assert
    assert result is None


@pytest.mark.parametrize(
    "input",
    [
        (
            """
// comment
CREATE OR REPLACE TABLE
// comment
(a INT, // comment
// comment
b INT)
// comment
;
// comment
"""
        ),
        (
            """
/* 
comment
comment
*/
CREATE OR REPLACE TABLE
/* comment
comment
comment */
(a INT, /* comment
comment */
/* comment 
*/
b INT)
/* comment */
;
/* comment 
comment */
"""
        ),
    ],
)
def test_remove_comment_keeps_whitespace(input):
    # arrange
    ddl = input

    # act
    result = string_util.remove_comment(ddl, keep_whitespace=True)

    # assert
    assert len(result) == len(input)
    assert [r.strip() for r in result.strip().splitlines()] == [
        s.strip()
        for s in string_util.remove_comment(ddl, keep_whitespace=False)
        .strip()
        .splitlines()
    ]


comment_after_statement_testcases = [
    ("CREATE TABLE x;", "CREATE TABLE x;"),
    (
        """CREATE OR REPLACE FUNCTION P_LEW_BIL.CHECK_OVERLAP(S1 DATE, E1 DATE, S2 DATE, E2 DATE)
    RETURNS BOOLEAN
    LANGUAGE JAVASCRIPT
    STRICT
    AS '
        var result =  (S1 > S2 && !(S1 >= E2 && E1 >= E2))   ||
                    (S2 > S1 && !(S2 >= E1 && E2 >= E1))     ||
                    (S1 == S2 && (E1 == E2 || E1 != E2));
        return result;
        
    ';""",
        """CREATE OR REPLACE FUNCTION P_LEW_BIL.CHECK_OVERLAP(S1 DATE, E1 DATE, S2 DATE, E2 DATE)
    RETURNS BOOLEAN
    LANGUAGE JAVASCRIPT
    STRICT
    AS '
        var result =  (S1 > S2 && !(S1 >= E2 && E1 >= E2))   ||
                    (S2 > S1 && !(S2 >= E1 && E2 >= E1))     ||
                    (S1 == S2 && (E1 == E2 || E1 != E2));
        return result;
        
    ';""",
    ),
    (
        """
    // comment
    CREATE OR REPLACE TABLE
    // comment
    (a INT, // comment
    // comment
    b INT)
    // comment
    ;
    // comment
    """,
        """
    // comment
    CREATE OR REPLACE TABLE
    // comment
    (a INT, // comment
    // comment
    b INT)
    // comment
    ;
    """,
    ),
    (
        """
    /* 
    comment
    comment
     */
    CREATE OR REPLACE TABLE
    /* comment
    comment
    comment */
    (a INT, /* comment
    comment */
    /* comment 
    */
    b INT)
    /* comment */
    ;
    /* comment 
    comment */
    """,
        """
    /* 
    comment
    comment
     */
    CREATE OR REPLACE TABLE
    /* comment
    comment
    comment */
    (a INT, /* comment
    comment */
    /* comment 
    */
    b INT)
    /* comment */
    ;
    """,
    ),
    (
        """
    CREATE SCHEMA dbp_data;
    /* i will be removed */
    """,
        """
    CREATE SCHEMA dbp_data;
    """,
    ),
    (
        """
    CREATE SCHEMA dbp_data; // this is removed
    /* i will be removed */
    """,
        """
    CREATE SCHEMA dbp_data;
    """,
    ),
    (
        """
    CREATE SCHEMA dbp_data; // this is removed
        /* i will be removed */
    """,
        """
    CREATE SCHEMA dbp_data;
    """,
    ),
    (
        """
    CREATE SCHEMA dbp_data; // this is removed
    """,
        """
    CREATE SCHEMA dbp_data;
    """,
    ),
    (
        """
    CREATE SCHEMA dbp_data; -- this is removed
    """,
        """
    CREATE SCHEMA dbp_data;
    """,
    ),
    (
        """
    CREATE SCHEMA dbp_data;
    """,
        """
    CREATE SCHEMA dbp_data;
    """,
    ),
    (
        """
    CREATE SCHEMA dbp_data; /* this is not ok */
    """,
        """
    CREATE SCHEMA dbp_data;
    """,
    ),
    (
        """
    CREATE SCHEMA dbp_data;
    /* this
    will 
    fail
    */
    """,
        """
    CREATE SCHEMA dbp_data;
    """,
    ),
    (
        """
    CREATE SCHEMA dbp_data; /* this
    will 
    fail
    */
    """,
        """
    CREATE SCHEMA dbp_data;
    """,
    ),
    (
        """
    /*This is ok*/
    -- This is ok
    CREATE SCHEMA dbp_data;  
    """,
        """
    /*This is ok*/
    -- This is ok
    CREATE SCHEMA dbp_data;  
    """,
    ),
    (
        """
    CREATE /* this is ok */ SCHEMA dbp_data;  
    """,
        """
    CREATE /* this is ok */ SCHEMA dbp_data;  
    """,
    ),
    (
        """
    CREATE /* this is ok */ SCHEMA dbp_data;  

    CREATE VIEW xyz; // not ok

    """,
        """
    CREATE /* this is ok */ SCHEMA dbp_data;  

    CREATE VIEW xyz;

    """,
    ),
    (
        """
    CREATE /* this is ok */ SCHEMA dbp_data;  

    CREAETE VIEW abc;

    //not ok
    """,
        """
    CREATE /* this is ok */ SCHEMA dbp_data;  

    CREAETE VIEW abc;
    """,
    ),
    (
        """
    CREATE PROCEDURE TEST ...
    $$
    $$;
    /*
    comment
    */
    -- comment
    """,
        """
    CREATE PROCEDURE TEST ...
    $$
    $$;
    """,
    ),
    (
        """
    CREATE PROCEDURE TEST ...
    $$;
    -- comment;
    """,
        """
    CREATE PROCEDURE TEST ...
    $$;
    """,
    ),
    (
        """
    CREATE PROCEDURE TEST ...
    $$;
    /* block 
    comment */ -- comment;
    """,
        """
    CREATE PROCEDURE TEST ...
    $$;
    """,
    ),
    (
        """
    CREATE PROCEDURE TEST ...
    $$;
    /* block */
    """,
        """
    CREATE PROCEDURE TEST ...
    $$;
    """,
    ),
    (
        """
    CREATE OR REPLACE TABLE X; /* block */ --line
    """,
        """
    CREATE OR REPLACE TABLE X;
    """,
    ),
    (
        """
    CREATE OR REPLACE TABLE X; --line;
    """,
        """
    CREATE OR REPLACE TABLE X;
    """,
    ),
    (
        """
    CREATE OR REPLACE TABLE X; 
    /* block; */
    """,
        """
    CREATE OR REPLACE TABLE X;
    """,
    ),
    (
        """
    CREATE OR REPLACE TABLE X; 
    --line;
    """,
        """
    CREATE OR REPLACE TABLE X;
    """,
    ),
    (
        """
    CREATE OR REPLACE TABLE X; 
    --line;
    /* block; */
    """,
        """
    CREATE OR REPLACE TABLE X;
    """,
    ),
    (
        """
    CREATE /* test */ OR REPLACE
    /* test*/ TABLE X; /*test*/
    """,
        """
    CREATE /* test */ OR REPLACE
    /* test*/ TABLE X;
    """,
    ),
    (
        """
    CREATE OR REPLACE TABLE X; /*test;test*//*test*/
    """,
        """
    CREATE OR REPLACE TABLE X; 
    """,
    ),
    (
        """
    CREATE /*test*/ OR REPLACE TABLE X; /*test;test*/
    """,
        """
    CREATE /*test*/ OR REPLACE TABLE X; 
    """,
    ),
    (
        """
    CREATE /*test;*/ OR REPLACE TABLE X; /*test;
    test*/
    """,
        """
    CREATE /*test;*/ OR REPLACE TABLE X; 
    """,
    ),
]


@pytest.mark.parametrize("input, expected", comment_after_statement_testcases)
def test_remove_comment_after_statement(input, expected):
    # arrange
    ddl = input

    # act
    result = string_util.remove_comment_after_statement(ddl)

    # assert
    assert result.strip() == expected.strip()


comment_before_statement_testcases = [
    ("CREATE TABLE x;", "CREATE TABLE x;"),
    (
        """CREATE OR REPLACE FUNCTION P_LEW_BIL.CHECK_OVERLAP(S1 DATE, E1 DATE, S2 DATE, E2 DATE)
    RETURNS BOOLEAN
    LANGUAGE JAVASCRIPT
    STRICT
    AS '
        var result =  (S1 > S2 && !(S1 >= E2 && E1 >= E2))   ||
                    (S2 > S1 && !(S2 >= E1 && E2 >= E1))     ||
                    (S1 == S2 && (E1 == E2 || E1 != E2));
        return result;
        
    ';""",
        """CREATE OR REPLACE FUNCTION P_LEW_BIL.CHECK_OVERLAP(S1 DATE, E1 DATE, S2 DATE, E2 DATE)
    RETURNS BOOLEAN
    LANGUAGE JAVASCRIPT
    STRICT
    AS '
        var result =  (S1 > S2 && !(S1 >= E2 && E1 >= E2))   ||
                    (S2 > S1 && !(S2 >= E1 && E2 >= E1))     ||
                    (S1 == S2 && (E1 == E2 || E1 != E2));
        return result;
        
    ';""",
    ),
    (
        """
    // comment
    CREATE OR REPLACE TABLE
    // comment
    (a INT, // comment
    // comment
    b INT)
    // comment
    ;
    // comment
    """,
        """
    CREATE OR REPLACE TABLE
    // comment
    (a INT, // comment
    // comment
    b INT)
    // comment
    ;
    // comment
    """,
    ),
    (
        """
    /* 
    comment
    comment
     */
    CREATE OR REPLACE TABLE
    /* comment
    comment
    comment */
    (a INT, /* comment
    comment */
    /* comment 
    */
    b INT)
    /* comment */
    ;
    /* comment 
    comment */
    """,
        """
    CREATE OR REPLACE TABLE
    /* comment
    comment
    comment */
    (a INT, /* comment
    comment */
    /* comment 
    */
    b INT)
    /* comment */
    ;
    /* comment 
    comment */
    """,
    ),
    (
        """
    CREATE SCHEMA dbp_data;
    /* i will be removed */
    """,
        """
    CREATE SCHEMA dbp_data;
    /* i will be removed */
    """,
    ),
    (
        """
    // this is removed
    /* i will be removed */
    CREATE SCHEMA dbp_data; 
    """,
        """
    CREATE SCHEMA dbp_data;
    """,
    ),
    (
        """
        // this is removed
        /* i will be removed */
    CREATE SCHEMA dbp_data; 
    """,
        """
    CREATE SCHEMA dbp_data;
    """,
    ),
    (
        """
    // this is removed
    CREATE SCHEMA dbp_data; 
    """,
        """
    CREATE SCHEMA dbp_data;
    """,
    ),
    (
        """
    -- this is removed
    CREATE SCHEMA dbp_data; 
    """,
        """
    CREATE SCHEMA dbp_data;
    """,
    ),
    (
        """
    CREATE SCHEMA dbp_data;
    """,
        """
    CREATE SCHEMA dbp_data;
    """,
    ),
    (
        """
    /* this is not ok */
    CREATE SCHEMA dbp_data; 
    """,
        """
    CREATE SCHEMA dbp_data;
    """,
    ),
    (
        """
    /* this
    will 
    fail
    */
    CREATE SCHEMA dbp_data;
    """,
        """
    CREATE SCHEMA dbp_data;
    """,
    ),
    (
        """/* this
    will 
    fail
    */  CREATE SCHEMA dbp_data; 
    """,
        """
    CREATE SCHEMA dbp_data;
    """,
    ),
    (
        """
    /*This is not ok*/
    -- This is not ok
    CREATE SCHEMA dbp_data;  
    """,
        """
    CREATE SCHEMA dbp_data;  
    """,
    ),
    (
        """
    CREATE /* this is ok */ SCHEMA dbp_data;  
    """,
        """
    CREATE /* this is ok */ SCHEMA dbp_data;  
    """,
    ),
    (
        """
    CREATE /* this is ok */ SCHEMA dbp_data;  

    CREATE VIEW xyz; // ok

    """,
        """
    CREATE /* this is ok */ SCHEMA dbp_data;  

    CREATE VIEW xyz; // ok

    """,
    ),
    (
        """
    CREATE /* this is ok */ SCHEMA dbp_data;  

    CREAETE VIEW abc;

    //not ok
    """,
        """
    CREATE /* this is ok */ SCHEMA dbp_data;  

    CREAETE VIEW abc;

    //not ok
    """,
    ),
    (
        """
    CREATE PROCEDURE TEST ...
    $$;
    /* block */
    """,
        """
    CREATE PROCEDURE TEST ...
    $$;
    /* block */
    """,
    ),
    (
        """
    CREATE OR REPLACE TABLE X; /* block */ --line
    """,
        """
    CREATE OR REPLACE TABLE X; /* block */ --line
    """,
    ),
    (
        """
    CREATE /* test */ OR REPLACE
    /* test*/ TABLE X; /*test*/
    """,
        """
    CREATE /* test */ OR REPLACE
    /* test*/ TABLE X; /*test*/
    """,
    ),
    (
        """
    CREATE OR REPLACE TABLE X; /*test;test*//*test*/
    """,
        """
    CREATE OR REPLACE TABLE X; /*test;test*//*test*/
    """,
    ),
]


@pytest.mark.parametrize("input, expected", comment_before_statement_testcases)
def test_remove_comment_before_statement(input, expected):
    # arrange
    ddl = input

    # act
    result = string_util.remove_comment_before_statement(ddl)

    # assert
    assert result.strip() == expected.strip()


@pytest.mark.parametrize(
    "statement, expected",
    [
        (
            """
        CREATE TABLE myschema.mytable(
            ID INT NOT NULL COMMENT 'Das Wort Join soll nicht geparst werden',
            NAME VARCHAR NOT NULL COMMENT 'Das Wort From ebenfalls nicht'
            );
        """,
            """
        CREATE TABLE myschema.mytable(
            ID INT NOT NULL COMMENT '',
            NAME VARCHAR NOT NULL COMMENT ''
            );
        """,
        ),
        (
            """
        CREATE VIEW myschema.myview AS (
            SELECT
            'test' as value1,
            'join abc.xyz' as value2,
            '\\'join abc.xyz\\'' as value3,
            '\\'join\\' abc.xyz' as value4;
        """,
            """
        CREATE VIEW myschema.myview AS (
            SELECT
            '' as value1,
            '' as value2,
            '' as value3,
            '' as value4;
        """,
        ),
        (
            """
        when  regexp_count(error_msg, $$.*The template in report is empty, or the objects on template can not be resolve.*$$) >=1 or regexp_count(error_msg, $$.*The object does not exist in the metadat.*$$)  >= 1
        """,
            """
        when  regexp_count(error_msg, $$$$) >=1 or regexp_count(error_msg, $$$$)  >= 1
        """,
        ),
        (
            """
        text $$this 'should' all be removed$$ more text
        """,
            """
        text $$$$ more text
        """
            #     ),( TODO: make this test work by changing the tested function
            #         """
            #         keep $$remove'remove$$ keep $$remove'remove$$ keep
            #         """,
            #         """
            #         keep $$$$ keep $$$$ keep
            #         """
        ),
        (
            """
        keep 'remove$$remove' keep 'remove$$remove' keep
        """,
            """
        keep '' keep '' keep
        """,
        ),
        (
            """
        keep 'remove' keep \\'keep\\' keep
        """,
            """
        keep '' keep \\'keep\\' keep
        """,
        ),
        (
            """
        keep 'remove' keep '\\'remove\\'' keep
        """,
            """
        keep '' keep '' keep
        """,
        ),
        (
            """
        keep $$remove$$ keep \\$$keep\\$$ keep
        """,
            """
        keep $$$$ keep \\$$keep\\$$ keep
        """,
        ),
    ],
)
def test_remove_text_in_quotes(statement, expected):
    """
    Example: Table columns can have a COMMENT field. Contents should not be parsed as dependencies.
    """

    # act
    result = string_util.remove_text_in_quotes(statement)

    # assert
    assert result.strip() == expected.strip()


@pytest.mark.parametrize(
    "statement, expected",
    [
        (
            """
CREATE OR REPLACE view MSTR_PROMPT_DATA.V_PARSED_EXPRESSION_ANSWERS
comment = 'Parsing view to get simple Elements of Expression Prompt Answer'
as
with cte_splitted_answers as
(
select
      DAY_ID
      ,report_job_id
      ,PROJECT_GUID
      ,REPORT_GUID
      ,PROMPT_GUID
      ,PROMPT_NAME
      ,PROMPT_TYPE
      ,PROMPT_ANSWERS
      ,IS_REQUIRED
      ,case when regexp_like(prompt_answers, $$.*\\)\\sAnd\\s\\(.*||.*\\)\\sUnd\\s\\(.*$$) and regexp_like(prompt_answers, $$.*\\)\\sOr\\s\\(.*||.*\\)\\sOder\\s\\(.*$$)
                then 'mixed'
            when regexp_like(prompt_answers, $$.*\\)\\sAnd\\s\\(.*||.*\\)\\sUnd\\s\\(.*$$) and not regexp_like(prompt_answers, $$.*\\)\\sOr\\s\\(.*||.*\\)\\sOder\\s\\(.*$$)
                then 'AND'
            when not regexp_like(prompt_answers, $$.*\\)\\sAnd\\s\\(.*||.*\\)\\sUnd\\s\\(.*$$) and regexp_like(prompt_answers, $$.*\\)\\sOr\\s\\(.*||.*\\)\\sOder\\s\\(.*$$)
                then 'OR'
            else 'AND'
            end as operator_type
       ,index
       ,value
  FROM em_data.v_complete_prompt_answers
, lateral split_to_table(REGEXP_REPLACE(PROMPT_ANSWERS, $$\\)\\s*(And|Or|Und|Oder)\\s*\\($$, $$)--||--($$,1, 0,'i'), '--||--')
where prompt_type = 'EXPRESSION'
  AND  prompt_answers IS NOT NULL
  and prompt_answers not like '%Między%'
  )
, cte_non_splittet_elements as (
SELECT 
     hist_exp.day_id
    ,hist_exp.report_job_id
    ,hist_exp.index
    ,hist_exp.operator_type
    ,hist_exp.project_guid AS project_guid
    ,hist_exp.report_guid
    ,hist_exp.prompt_guid
    ,hist_exp.prompt_name
    ,hist_exp.prompt_type 
    ,rest_obj.prompt_details_json:objects[0]:name::string AS object_name
    ,rest_obj.prompt_details_json:objects[0]:type::string AS object_type
    ,rest_obj.prompt_details_json:objects[0]:id::string   AS object_id
    ,hist_exp.prompt_answers as all_prompt_answers
    ,hist_exp.value as prompt_answers
    ,REGEXP_REPLACE(hist_exp.value, '^\\\\((.*)\\\\)$',$$\\1$$) as one_expression

    ,REGEXP_REPLACE(
       REGEXP_REPLACE(
       REGEXP_REPLACE(
       REGEXP_REPLACE(
              REGEXP_REPLACE(
                  REGEXP_REPLACE(hist_exp.value, $${.*}$$, $$$$)
              ,$$[^\\=\\<\\>\\!]+\\s*([\\=|\\>|\\!|\\<|\\<\\=|\\>\\=]+)\\s*[^\\=\\<\\>\\!]*$$,$$\\1$$ )
       ,$$.*Between.*$$     ,$$Between$$ )
       ,$$.*zwischen.*$$    ,$$zwischen$$ )
       ,$$.*enthält.*$$     ,$$enthält$$ )
       ,$$.*beginnt mit.*$$ ,$$beginnt mit$$ )
       AS operator_parsed
  
    /*,case when hist_exp.value not ilike '%{%'
            then    REGEXP_REPLACE(
                        REGEXP_REPLACE(
                            REGEXP_REPLACE(
                                trim(hist_exp.value, '()')
                            ,$$^([^\\<\\>\\=]+)\\s.+$$, $$\\1$$)
                        ,$$\\sBetween.*$$, $$$$)
                     ,$$\\szwischen.*$$, $$$$)
             else   REGEXP_REPLACE(
                          REGEXP_REPLACE(
                              --REGEXP_REPLACE(
                                  REGEXP_REPLACE(
                                      trim(hist_exp.value, '()')
                                  ,$$([^\\<\\>\\=]+)\\s.+$$, $$\\1$$)
                              --,$${$$, $$$$)
                          ,$$\\sBetween.*$$, $$$$)
                      ,$$\\szwischen.*$$, $$$$)
             end
       AS prompt_answer_left
    */
    /*,REGEXP_REPLACE(
     REGEXP_REPLACE(
     REGEXP_REPLACE(
     REGEXP_REPLACE(
            REGEXP_REPLACE(
                trim(hist_exp.value, '()')
            ,$$^([^\\<\\>\\=]+)\\s.+$$, $$\\1$$)
     ,$$\\sBetween.*$$    , $$$$)
     ,$$\\szwischen.*$$   , $$$$)
     ,$$\\senthält.*$$    , $$$$)
     ,$$\\sbeginnt mit.*$$, $$$$)
     AS prompt_answer_left */
  
      /*,REGEXP_REPLACE(
         REGEXP_REPLACE(
         REGEXP_REPLACE(
         REGEXP_REPLACE(
                
                    substring(hist_exp.value, 1, length(hist_exp.value) -
                                                           length(operator_parsed||' '||regexp_replace(
                                                                                                regexp_replace(
                                                                                                        trim(hist_exp.value, '()')
                                                                                                ,$${.*}$$, $$$$)
                                                                                         ,$$.*$$||operator_parsed, $$$$)
                                                            )
                    )
                
         ,$$\\sBetween.*$$    , $$$$)
         ,$$\\szwischen.*$$   , $$$$)
         ,$$\\senthält.*$$    , $$$$)
         ,$$\\sbeginnt mit.*$$, $$$$)
         AS prompt_answer_left */
     , REGEXP_REPLACE(
       REGEXP_REPLACE(
       REGEXP_REPLACE(
       REGEXP_REPLACE(
       REGEXP_REPLACE(
              REGEXP_REPLACE(
                  ifnull(
                        regexp_replace(
                                trim(hist_exp.value, '()')
                        ,$$\\{.*\\}$$, regexp_replace(
                                regexp_substr(
                                        trim(hist_exp.value, '()')
                                ,$$\\{.*\\}$$)
                                ,$$<=$$, $$-|~$$))
                    ,trim(hist_exp.value, '()'))
              ,$$^([^\\<\\>\\=]+)\\s.+$$, $$\\1$$)
       ,$$\\sBetween.*$$    , $$$$)
       ,$$\\szwischen.*$$   , $$$$)
       ,$$\\senthält.*$$    , $$$$)
       ,$$\\sbeginnt mit.*$$, $$$$)
       ,$$-\\|~$$, $$<=$$)
     as prompt_answer_left 
    

--  ifnull(regexp_replace(trim(hist_exp.value, '()'), $$\\{.*\\}$$ , regexp_replace(regexp_substr(trim(hist_exp.value, '()'), $$\\{.*\\}$$), $$<=$$, $$-|~$$)), trim(hist_exp.value, '()'))
  
  
  
    ,trim(
        regexp_substr(
            regexp_replace(prompt_answer_left, $$\\{.*?\\}$$)
        ,$$\\(.*?\\)$$)
      ,'()') 
     AS attribute_form
     ,trim(
        trim(
            REPLACE(
                REGEXP_REPLACE(prompt_answer_left, ifnull($$\\($$ || attribute_form || $$\\)$$, '') , $$$$)
            ,$$()$$, $$$$)
        )
      , '{}') 
     AS attribute
  
    ,t_leo.rest_operator as operator
  
    ,regexp_replace(
     regexp_replace(
       regexp_replace(
     regexp_replace(
     regexp_replace(
     regexp_replace(
                    REGEXP_REPLACE(
                        REGEXP_REPLACE(   
                                one_expression, $${.*}$$, $$$$)
                    , $$[^\\<\\>]+\\s*([\\=|\\>|\\!|\\<]+)\\s*([^\\<\\>\\"\\'\\)\\(]+)$$,'\\2')
                        
     ,$$.*Between\\s$$   , $$$$)
     ,$$\\sand\\s$$       , $$|$$)
     ,$$.*zwischen\\s$$  , $$$$)
     ,$$\\sund\\s$$       , $$|$$) 
      ,$$.*enthält\\s$$    , $$$$)
       ,$$.*beginnt mit\\s$$, $$$$)
     AS answer_values
    , case when pe.replace_value is not null
            then pe.replace_value
            else answer_values
            end as replace_value
    ,hist_exp.is_required
FROM cte_splitted_answers AS hist_exp
LEFT JOIN mstr_prompt_data.t_rest_prompt_objects AS rest_obj
  ON  hist_exp.project_guid = rest_obj.project_guid
  AND hist_exp.prompt_guid  = rest_obj.prompt_guid
LEFT JOIN mstr_prompt_data.t_operator_mapping t_leo
  on REGEXP_REPLACE(
     REGEXP_REPLACE(
     REGEXP_REPLACE(
     REGEXP_REPLACE(
            REGEXP_REPLACE(
                REGEXP_REPLACE(hist_exp.value, $${.*}$$, $$$$)
            ,$$[^\\=\\<\\>\\!]+\\s*([\\=|\\>|\\!|\\<]+)\\s*[^\\=\\<\\>\\!]*$$,$$\\1$$ )
     ,$$.*Between.*$$     ,$$Between$$ )
     ,$$.*zwischen.*$$    ,$$zwischen$$ )
     ,$$.*enthält.*$$     ,$$enthält$$ )
     ,$$.*beginnt mit.*$$ ,$$beginnt mit$$ ) = t_leo.em_operator
left join mstr_prompt_data.t_parsing_exceptions pe
    on pe.em_log = regexp_replace(
     regexp_replace(
       regexp_replace(
     regexp_replace(
     regexp_replace(
     regexp_replace(
                    REGEXP_REPLACE(
                        REGEXP_REPLACE(   
                                REGEXP_REPLACE(hist_exp.value, '^\\\\((.*)\\\\)$',$$\\1$$), $${.*}$$, $$$$)
                    , $$[^\\<\\>]+\\s*([\\=|\\>|\\!|\\<]+)\\s*([^\\<\\>\\"\\'\\)\\(]+)$$,$$\\2$$)
                        
     ,$$.*Between\\s$$   , $$$$)
     ,$$\\sand\\s$$       , $$|$$)
     ,$$.*zwischen\\s$$  , $$$$)
     ,$$\\sund\\s$$       , $$|$$) 
      ,$$.*enthält\\s$$    , $$$$)
       ,$$.*beginnt mit\\s$$, $$$$)
WHERE 
     --jobid in (1016107) and
     hist_exp.prompt_type = 'EXPRESSION'
AND  hist_exp.prompt_answers IS NOT NULL
)
-- split The Elements-Answers in answer in case multiple elements were selected
select      
     day_id
    ,report_job_id
    ,project_guid AS project_guid
    ,report_guid
    ,prompt_guid
    ,prompt_name
    ,prompt_type 
    ,object_name
    ,object_type
    ,object_id
    ,a.index as logical_index
    ,all_prompt_answers
    ,prompt_answers
    ,operator_type
    ,one_expression
    --,aaaaaaaaaa 
    ,prompt_answer_left
    ,attribute_form
    ,attribute
    ,a.operator_parsed
    ,operator
    ,b.index as index
    , replace_value
    ,replace(replace(b.value, '|*^ ', ', '),'"','') as answer_values
    --,replace(replace(replace_value, '|*^ ', ', '),'"','') as answer_values
    ,is_required
from cte_non_splittet_elements a
--, lateral split_to_table(REPLACE(REPLACE(answer_values, '"; "', '", "'), '" oder "', '", "'), '", "') b;
, lateral split_to_table(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(replace_value, ' or ', ', '), '"; "', ', '), '" oder "', ', '), '; ', ', '), ' oder ', ', '), ', ') b

--where jobid = 5538135
;
    """,
            """
CREATE OR REPLACE view MSTR_PROMPT_DATA.V_PARSED_EXPRESSION_ANSWERS
comment = ''
as
with cte_splitted_answers as
(
select
      DAY_ID
      ,report_job_id
      ,PROJECT_GUID
      ,REPORT_GUID
      ,PROMPT_GUID
      ,PROMPT_NAME
      ,PROMPT_TYPE
      ,PROMPT_ANSWERS
      ,IS_REQUIRED
      ,case when regexp_like(prompt_answers, $$$$) and regexp_like(prompt_answers, $$$$)
                then ''
            when regexp_like(prompt_answers, $$$$) and not regexp_like(prompt_answers, $$$$)
                then ''
            when not regexp_like(prompt_answers, $$$$) and regexp_like(prompt_answers, $$$$)
                then ''
            else ''
            end as operator_type
       ,index
       ,value
  FROM em_data.v_complete_prompt_answers
, lateral split_to_table(REGEXP_REPLACE(PROMPT_ANSWERS, $$$$, $$$$,1, 0,''), '')
where prompt_type = ''
  AND  prompt_answers IS NOT NULL
  and prompt_answers not like ''
  )
, cte_non_splittet_elements as (
SELECT 
     hist_exp.day_id
    ,hist_exp.report_job_id
    ,hist_exp.index
    ,hist_exp.operator_type
    ,hist_exp.project_guid AS project_guid
    ,hist_exp.report_guid
    ,hist_exp.prompt_guid
    ,hist_exp.prompt_name
    ,hist_exp.prompt_type 
    ,rest_obj.prompt_details_json:objects[0]:name::string AS object_name
    ,rest_obj.prompt_details_json:objects[0]:type::string AS object_type
    ,rest_obj.prompt_details_json:objects[0]:id::string   AS object_id
    ,hist_exp.prompt_answers as all_prompt_answers
    ,hist_exp.value as prompt_answers
    ,REGEXP_REPLACE(hist_exp.value, '',$$$$) as one_expression

    ,REGEXP_REPLACE(
       REGEXP_REPLACE(
       REGEXP_REPLACE(
       REGEXP_REPLACE(
              REGEXP_REPLACE(
                  REGEXP_REPLACE(hist_exp.value, $$$$, $$$$)
              ,$$$$,$$$$ )
       ,$$$$     ,$$$$ )
       ,$$$$    ,$$$$ )
       ,$$$$     ,$$$$ )
       ,$$$$ ,$$$$ )
       AS operator_parsed
  
    



















    











  
      


















     , REGEXP_REPLACE(
       REGEXP_REPLACE(
       REGEXP_REPLACE(
       REGEXP_REPLACE(
       REGEXP_REPLACE(
              REGEXP_REPLACE(
                  ifnull(
                        regexp_replace(
                                trim(hist_exp.value, '')
                        ,$$$$, regexp_replace(
                                regexp_substr(
                                        trim(hist_exp.value, '')
                                ,$$$$)
                                ,$$$$, $$$$))
                    ,trim(hist_exp.value, ''))
              ,$$$$, $$$$)
       ,$$$$    , $$$$)
       ,$$$$   , $$$$)
       ,$$$$    , $$$$)
       ,$$$$, $$$$)
       ,$$$$, $$$$)
     as prompt_answer_left 
    


  
  
  
    ,trim(
        regexp_substr(
            regexp_replace(prompt_answer_left, $$$$)
        ,$$$$)
      ,'') 
     AS attribute_form
     ,trim(
        trim(
            REPLACE(
                REGEXP_REPLACE(prompt_answer_left, ifnull($$$$ || attribute_form || $$$$, '') , $$$$)
            ,$$$$, $$$$)
        )
      , '') 
     AS attribute
  
    ,t_leo.rest_operator as operator
  
    ,regexp_replace(
     regexp_replace(
       regexp_replace(
     regexp_replace(
     regexp_replace(
     regexp_replace(
                    REGEXP_REPLACE(
                        REGEXP_REPLACE(   
                                one_expression, $$$$, $$$$)
                    , $$$$,'')
                        
     ,$$$$   , $$$$)
     ,$$$$       , $$$$)
     ,$$$$  , $$$$)
     ,$$$$       , $$$$) 
      ,$$$$    , $$$$)
       ,$$$$, $$$$)
     AS answer_values
    , case when pe.replace_value is not null
            then pe.replace_value
            else answer_values
            end as replace_value
    ,hist_exp.is_required
FROM cte_splitted_answers AS hist_exp
LEFT JOIN mstr_prompt_data.t_rest_prompt_objects AS rest_obj
  ON  hist_exp.project_guid = rest_obj.project_guid
  AND hist_exp.prompt_guid  = rest_obj.prompt_guid
LEFT JOIN mstr_prompt_data.t_operator_mapping t_leo
  on REGEXP_REPLACE(
     REGEXP_REPLACE(
     REGEXP_REPLACE(
     REGEXP_REPLACE(
            REGEXP_REPLACE(
                REGEXP_REPLACE(hist_exp.value, $$$$, $$$$)
            ,$$$$,$$$$ )
     ,$$$$     ,$$$$ )
     ,$$$$    ,$$$$ )
     ,$$$$     ,$$$$ )
     ,$$$$ ,$$$$ ) = t_leo.em_operator
left join mstr_prompt_data.t_parsing_exceptions pe
    on pe.em_log = regexp_replace(
     regexp_replace(
       regexp_replace(
     regexp_replace(
     regexp_replace(
     regexp_replace(
                    REGEXP_REPLACE(
                        REGEXP_REPLACE(   
                                REGEXP_REPLACE(hist_exp.value, '',$$$$), $$$$, $$$$)
                    , $$$$,$$$$)
                        
     ,$$$$   , $$$$)
     ,$$$$       , $$$$)
     ,$$$$  , $$$$)
     ,$$$$       , $$$$) 
      ,$$$$    , $$$$)
       ,$$$$, $$$$)
WHERE 
     
     hist_exp.prompt_type = ''
AND  hist_exp.prompt_answers IS NOT NULL
)

select      
     day_id
    ,report_job_id
    ,project_guid AS project_guid
    ,report_guid
    ,prompt_guid
    ,prompt_name
    ,prompt_type 
    ,object_name
    ,object_type
    ,object_id
    ,a.index as logical_index
    ,all_prompt_answers
    ,prompt_answers
    ,operator_type
    ,one_expression
    
    ,prompt_answer_left
    ,attribute_form
    ,attribute
    ,a.operator_parsed
    ,operator
    ,b.index as index
    , replace_value
    ,replace(replace(b.value, '', ''),'','') as answer_values
    
    ,is_required
from cte_non_splittet_elements a

, lateral split_to_table(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(replace_value, '', ''), '', ''), '', ''), '', ''), '', ''), '') b


;
    """,
        )
    ],
)
def test_real_world_example(statement, expected):
    """
    Test the combination of remove_comment and remove_text_in_quotes, as used in dependency parser
    """
    # act
    s1 = string_util.remove_comment(statement)
    s2 = string_util.remove_text_in_quotes(s1)

    # assert
    assert len(s2.strip().splitlines()) == len(expected.strip().splitlines())
    for result, expect in zip(s2.strip().splitlines(), expected.strip().splitlines()):
        assert result == expect


@pytest.mark.parametrize(
    "input, expected",
    [
        ("(EINS, ZWEI, DREI)", ["EINS", "ZWEI", "DREI"]),
        ("()", []),
        ("", []),
        ("(EINS)", ["EINS"]),
        ("EINS", ["EINS"]),
        ("EINS, ZWEI, DREI", ["EINS", "ZWEI", "DREI"]),
        ("(EINS,ZWEI,DREI)", ["EINS", "ZWEI", "DREI"]),
        ("(     EINS,    ZWEI, DREI             )", ["EINS", "ZWEI", "DREI"]),
        ("(EINS(1,2), ZWEI(1,2), DREI(1,2))", ["EINS(1,2)", "ZWEI(1,2)", "DREI(1,2)"]),
        (
            "(EINS(1,2), ZWEI(1,    2), DREI( 1, 2  ))",
            ["EINS(1,2)", "ZWEI(1,    2)", "DREI( 1, 2  )"],
        ),
    ],
)
def test_split_parameters_string(input, expected):
    # arrange
    parameters = input

    # act
    result = string_util.split_parameters_string(parameters)

    # assert
    assert result == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            """
            CREATE VIEW S.V AS SELECT 1 I;
            """,
            """
            CREATE OR REPLACE VIEW S.V AS SELECT 1 I;
            """,
        ),
        (
            """
                CREATE   VIEW  S.V AS  SELECT 1 I;
            """,
            """
            CREATE OR REPLACE VIEW  S.V AS  SELECT 1 I;
            """,
        ),
        (
            """
            CREATE 
            VIEW 
            S.V AS SELECT 1 I;
            """,
            """
            CREATE OR REPLACE VIEW 
            S.V AS SELECT 1 I;
            """,
        ),
        (
            """
            CREATE OR REPLACE VIEW S.V AS SELECT 1 I;
            """,
            """
            CREATE OR REPLACE VIEW S.V AS SELECT 1 I;
            """,
        ),
        (
            """
               CREATE   OR    REPLACE   VIEW S.V AS SELECT 1 I;
            """,
            """
            CREATE OR REPLACE VIEW S.V AS SELECT 1 I;
            """,
        ),
        (
            """
            CREATE 
            OR 
            REPLACE
             VIEW S.V AS SELECT 1 I;
            """,
            """
            CREATE OR REPLACE VIEW S.V AS SELECT 1 I;
            """,
        ),
        (
            """
            // comment
            CREATE VIEW S.V AS SELECT 1 I;
            // comment
            """,
            """
            CREATE OR REPLACE VIEW S.V AS SELECT 1 I;
            // comment
            """,
        ),
        (
            """
            /*
             comment
            */
            CREATE VIEW S.V AS SELECT 1 I;
            /*
             comment
            */
            """,
            """
            CREATE OR REPLACE VIEW S.V AS SELECT 1 I;
            /*
             comment
            */
            """,
        ),
        (
            """
            /*
             comment
            */ CREATE VIEW S.V AS SELECT 1 I;
            /*
             comment
            */
            """,
            """
             CREATE OR REPLACE VIEW S.V AS SELECT 1 I;
            /*
             comment
            */
            """,
        ),
        (
            """
            CREATE VIEW S.V AS SELECT 1 I COMMENT 'CREATE VIEW COMMENT';
            """,
            """
            CREATE OR REPLACE VIEW S.V AS SELECT 1 I COMMENT 'CREATE VIEW COMMENT';
            """,
        ),
        (
            """
            CREATE VIEW CREATE AS SELECT 1 I;
            """,
            """
            CREATE OR REPLACE VIEW CREATE AS SELECT 1 I;
            """,
        ),
    ],
)
def test_add_create_or_replace(input, expected):
    # arrange
    ddl = input

    # act
    result = string_util.add_create_or_replace(ddl)

    # assert
    assert result.strip() == expected.strip()


@pytest.mark.parametrize(
    "input",
    [
        (
            """
            DROP VIEW S.V;
            """
        ),
        (
            """
            CERATE VIEW S.V;
            """
        ),
        (
            """
            DROP VIEW CREATE ;
            """
        ),
    ],
)
def test_add_create_or_replace_error(input):
    with pytest.raises(ValueError):
        __ = string_util.add_create_or_replace(input)


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            """
            CREATE OR REPLACE VIEW S.V AS SELECT 1 I;
            """,
            """
            CREATE VIEW S.V AS SELECT 1 I;
            """,
        ),
        (
            """
                CREATE   OR   REPLACE VIEW  S.V AS  SELECT 1 I;
            """,
            """
            CREATE VIEW  S.V AS  SELECT 1 I;
            """,
        ),
        (
            """
            CREATE OR REPLACE
            VIEW 
            S.V AS SELECT 1 I;
            """,
            """
            CREATE VIEW 
            S.V AS SELECT 1 I;
            """,
        ),
        (
            """
            CREATE VIEW S.V AS SELECT 1 I;
            """,
            """
            CREATE VIEW S.V AS SELECT 1 I;
            """,
        ),
        (
            """
               CREATE      VIEW      S.V       AS SELECT 1 I;
            """,
            """
            CREATE VIEW      S.V       AS SELECT 1 I;
            """,
        ),
        (
            """
            CREATE 

             VIEW
              S.V
               AS SELECT 1 I;
            """,
            """
            CREATE VIEW
              S.V
               AS SELECT 1 I;
            """,
        ),
        (
            """
            // comment
            CREATE OR REPLACE VIEW S.V AS SELECT 1 I;
            // comment
            """,
            """
            CREATE VIEW S.V AS SELECT 1 I;
            // comment
            """,
        ),
        (
            """
            /*
             comment
            */
            CREATE OR REPLACE VIEW S.V AS SELECT 1 I;
            /*
             comment
            */
            """,
            """
            CREATE VIEW S.V AS SELECT 1 I;
            /*
             comment
            */
            """,
        ),
        (
            """
            /*
             comment
            */ CREATE OR REPLACE VIEW S.V AS SELECT 1 I;
            /*
             comment
            */
            """,
            """
             CREATE VIEW S.V AS SELECT 1 I;
            /*
             comment
            */
            """,
        ),
        (
            """
            CREATE OR REPLACE VIEW S.V AS SELECT 1 I COMMENT 'CREATE VIEW COMMENT';
            """,
            """
            CREATE VIEW S.V AS SELECT 1 I COMMENT 'CREATE VIEW COMMENT';
            """,
        ),
        (
            """
            CREATE OR REPLACE VIEW CREATE AS SELECT 1 I;
            """,
            """
            CREATE VIEW CREATE AS SELECT 1 I;
            """,
        ),
    ],
)
def test_remove_create_or_replace(input, expected):
    # arrange
    ddl = input

    # act
    result = string_util.remove_create_or_replace(ddl)

    # assert
    assert result.strip() == expected.strip()


@pytest.mark.parametrize(
    "input",
    [
        (
            """
            DROP VIEW S.V;
            """
        ),
        (
            """
            CERATE VIEW S.V;
            """
        ),
        (
            """
            DROP VIEW CREATE ;
            """
        ),
    ],
)
def test_remove_create_or_replace_error(input):
    with pytest.raises(ValueError):
        __ = string_util.remove_create_or_replace(input)


@pytest.mark.parametrize(
    "s, prefix, expected",
    [
        ("pre_some_text", "pre_", "some_text"),
        ("pre some text", "pre ", "some text"),
        ("pre some text", "", "pre some text"),
        ("pre some text", "hello", "pre some text"),
        ("pre\nsome\ntext", "pre\n", "some\ntext"),
        ("hello world hello", "hello", " world hello"),
    ],
)
def test_remove_prefix(s, prefix, expected):
    result = string_util.remove_prefix(s, prefix)
    assert result == expected


@pytest.mark.parametrize(
    "s, string_replace_dict, expected",
    [
        (
            "Franz jagt im komplett verwahrlosten Taxi quer durch Bayern",
            {},
            "Franz jagt im komplett verwahrlosten Taxi quer durch Bayern",
        ),
        (
            "Franz jagt im komplett verwahrlosten %%var1%% quer durch Bayern",
            {"var1": "Taxi"},
            "Franz jagt im komplett verwahrlosten Taxi quer durch Bayern",
        ),
        (
            "%%var2%% jagt im komplett verwahrlosten %%var1%% quer durch Bayern",
            {"var1": "Taxi", "var2": "Franz"},
            "Franz jagt im komplett verwahrlosten Taxi quer durch Bayern",
        ),
        (
            "%%var2%% jagt im komplett verwahrlosten %%var1%% quer durch Bayern",
            {"varA": "Taxi", "varB": "Franz"},
            "%%var2%% jagt im komplett verwahrlosten %%var1%% quer durch Bayern",
        ),
        (
            "%%var2%% jagt im komplett %%var3%%%%var4%% %%var1%% quer durch Bayern",
            {"var1": "Taxi", "var2": "Franz", "var3": "verwah", "var4": "rlosten"},
            "Franz jagt im komplett verwahrlosten Taxi quer durch Bayern",
        ),
    ],
)
def test_string_replace_by_dict(s, string_replace_dict, expected):
    result = string_util.string_replace_by_dict(s, string_replace_dict)
    assert result == expected


@pytest.mark.parametrize(
    "s, expected",
    [
        ("hello world", "hello world"),
        ("hello 'world'", "hello ''world''"),
    ],
)
def test_escape_string_for_snowflake(s, expected):
    result = string_util.escape_string_for_snowflake(s)
    assert result == expected


@pytest.mark.parametrize(
    "s, expected",
    [
        (None, "NONE"),
        ("hello world", "'hello world'"),
        ("hello 'world'", "'hello ''world'''"),
        (
            """hello
         world""",
            r"'hello\n         world'",
        ),
        (True, "TRUE"),
        (False, "FALSE"),
        (123, "123"),
        (0, "0"),
        (["hello", "world"], "('hello', 'world')"),
        (["hello", "world", 123], "('hello', 'world', 123)"),
    ],
)
def test_convert_python_variable_to_snowflake_value(s, expected):
    result = string_util.convert_python_variable_to_snowflake_value(s)
    assert result == expected


@pytest.mark.parametrize(
    "val",
    [
        ({"key1": "val1", "key2": "val2"}),
        (12.3),
    ],
)
def test_convert_python_variable_to_snowflake_value_raises_error(val):
    with pytest.raises(ValueError):
        __ = string_util.convert_python_variable_to_snowflake_value(val)



@pytest.mark.parametrize(
    "str1, str2, expected",
    [
        (
            """CREATE OR REPLACE VIEW s.v AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW s.v AS SELECT 1 I;""",
            True,
        ),
        (
            """CREATE OR REPLACE VIEW s.v AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW S.V as SELECT 1 I;""",
            True,
        ),
        (
            """CREATE OR REPLACE 
            VIEW s.v AS SELECT 1 I;""",
            """CREATE 
            OR 
            REPLACE VIEW S.V 
            as     SELECT 1 I  ;   """,
            True,
        ),
        (
            """CREATE OR REPLACE VIEW s.v AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW S.V_DIFF as SELECT 1 I;""",
            False,
        )
    ],
)
def test_compare_strings_ignore_whitespace_and_case(str1, str2, expected):
    result = string_util.compare_strings_ignore_whitespace_and_case(str1, str2)
    assert result == expected


@pytest.mark.parametrize(
    "view_ddl, expected",
    [
        (
            """CREATE OR REPLACE VIEW s.v AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW s.v COPY GRANTS  AS SELECT 1 I;""",
        ),
        (
            """CREATE OR REPLACE VIEW s. v AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW s. v COPY GRANTS  AS SELECT 1 I;""",
        ),
        (
            """CREATE OR REPLACE VIEW s.
                v AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW s.
                v COPY GRANTS  AS SELECT 1 I;""",
        ),
        (
            """CREATE OR REPLACE VIEW s .v AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW s .v COPY GRANTS  AS SELECT 1 I;""",
        ),
        (
            """CREATE OR REPLACE VIEW d. s . "v" AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW d. s . "v" COPY GRANTS  AS SELECT 1 I;""",
        ),
        (
            """CREATE OR REPLACE VIEW d. "s" ."v" AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW d. "s" ."v" COPY GRANTS  AS SELECT 1 I;""",
        ),
        (
            """CREATE OR REPLACE VIEW "d". s ."v" AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW "d". s ."v" COPY GRANTS  AS SELECT 1 I;""",
        ),
        (
            """CREATE OR REPLACE VIEW "d". "s" .v AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW "d". "s" .v COPY GRANTS  AS SELECT 1 I;""",
        ),
        (
            """CREATE OR REPLACE VIEW s
                .v AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW s
                .v COPY GRANTS  AS SELECT 1 I;""",
        ),
        (
            """CREATE OR REPLACE view s.v AS SELECT 1 I;""",
            """CREATE OR REPLACE view s.v COPY GRANTS  AS SELECT 1 I;""",
        ),
        (
            """CREATE OR REPLACE VIEW s.v COPY GRANTS AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW s.v COPY GRANTS AS SELECT 1 I;""",
        ),
        (
            """CREATE OR REPLACE VIEW s. v COPY GRANTS AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW s. v COPY GRANTS AS SELECT 1 I;""",
        ),
        (
            """CREATE OR REPLACE VIEW s.
               v COPY GRANTS AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW s.
               v COPY GRANTS AS SELECT 1 I;""",
        ),
        (
            """CREATE OR REPLACE VIEW s .v COPY GRANTS AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW s .v COPY GRANTS AS SELECT 1 I;""",
        ),
        (
            """CREATE OR REPLACE VIEW "d". "s" ."v" COPY GRANTS  AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW "d". "s" ."v" COPY GRANTS  AS SELECT 1 I;""",
        ),
        (
            """CREATE OR REPLACE VIEW s
               .v COPY GRANTS AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW s
               .v COPY GRANTS AS SELECT 1 I;""",
        ),
        (
            """CREATE VIEW s.v AS SELECT 1 I;""",
            """CREATE VIEW s.v COPY GRANTS  AS SELECT 1 I;""",  # this will not work in snowflake, because the OR REPLACE is missing. in the full script, we make sure to add that before passing it to add_copy_grants
        ),
        (
            """CREATE
            OR
                REPLACE
            VIEW
            s.v
            AS
                 SELECT
         1 I;""",
            """CREATE
            OR
                REPLACE
            VIEW
            s.v COPY GRANTS 
            AS
                 SELECT
         1 I;""",
        ),
        (
            """CREATE OR REPLACE VIEW d.s.v AS SELECT 1 I;""",
            """CREATE OR REPLACE VIEW d.s.v COPY GRANTS  AS SELECT 1 I;""",
        ),
    ],
)
def test_add_copy_grants(view_ddl, expected):
    result = string_util.add_copy_grants(view_ddl)
    assert result == expected