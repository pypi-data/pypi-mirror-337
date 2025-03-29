from typing import List

import pytest
from acedeploy.services.dependency_parser import DependencyParser


def test_parse_object_dependencies_views_static_with_no_dependency_should_return_empty_list():
    # arrange
    sut = DependencyParser(None)  # using None dummy
    statement = """
    SELECT 0
    """

    # act
    result = sut._parse_object_dependencies_views_static(statement)

    # assert
    assert not result


def test_parse_object_dependencies_views_static_with_alias_should_return_list():
    # arrange
    sut = DependencyParser(None)  # using None dummy
    statement = """
    SELECT * FROM table as t WHERE a = b
    """
    expected = ["table"]

    # act
    result = sut._parse_object_dependencies_views_static(statement)

    # assert
    assert result == expected


def test_parse_column_names_should_not_trigger_parse():
    # arrange
    sut = DependencyParser(None)  # using None dummy
    statement = """
    CREATE TABLE x.y(
	DELETED_FG NUMBER(38,0),
	DWH_VALID_FROM DATE,
	DWH_VALID_TO DATE,
    "VALID-FROM" DATE,
    "VALID-TO" DATE
    );
    """
    expected = []

    # act
    result = sut._parse_object_dependencies_views_static(statement)

    # assert
    assert result == expected


def test_parse_column_names_should_not_trigger_parse2():
    # arrange
    sut = DependencyParser(None)  # using None dummy
    statement = """
    CREATE OR REPLACE VIEW x.y AS
    SELECT
        agg.cal_dt,
        ex.from_curr_cd AS curr_cd,
        agg.receipt_cnt,
        agg.receipt_txj_py_swday_cnt,
        agg.receipt_ejr_py_swday_cnt,
        TRUNC(agg.turnover_gross_val / CASE WHEN ex.exchange_rate = 0 THEN null ELSE ex.exchange_rate END) AS turnover_gross_val,
        TRUNC(agg.turnover_ejr_py_swday_gross_val      / CASE WHEN ex.exchange_rate = 0 THEN null ELSE ex.exchange_rate END) AS turnover_ejr_py_swday_gross_val
    FROM a.b;
    """
    expected = ["a.b"]

    # act
    result = sut._parse_object_dependencies_views_static(statement)

    # assert
    assert result == expected


def test_parse_column_names_should_not_trigger_parse3():
    # arrange
    sut = DependencyParser(None)  # using None dummy
    statement = """
CREATE OR REPLACE VIEW P_LEW_BIL_AC.V_FACT_EXCHANGE_RATE
(
     from_curr_cd
,          to_curr_cd

,          exchange_rate_type_cd

,          active_from_dt
,          active_to_dt
,          active_fg

,          bus_year
,          exchange_rate

,          dwh_load_id
,          dwh_created
,          dwh_updated
)
AS
   (
        SELECT      Exch.from_curr_cd                   AS from_curr_cd,
   Exch.to_curr_cd                     AS to_curr_cd,
   Exch.exchange_rate_type_cd          AS exchange_rate_type_cd,
   Exch.active_from_dt                 AS active_from_dt,
   Exch.active_to_dt                   AS active_to_dt,
   Exch.active_fg                      AS active_fg,
   Exch.bus_year                       AS bus_year,
   Exch.exchange_rate                  AS exchange_rate,
   Exch.dwh_load_id                    AS dwh_load_id,
   Exch.dwh_created                    AS dwh_created,
   Exch.dwh_updated                    AS dwh_updated

FROM p_lew_bil.t_fact_exchange_rate        AS Exch
   );
    """
    expected = ["p_lew_bil.t_fact_exchange_rate"]

    # act
    result = sut._parse_object_dependencies_views_static(statement)

    # assert
    assert result == expected


def test_parse_object_dependencies_views_static_with_multipart_identifier_should_return_list():
    # arrange
    sut = DependencyParser(None)  # using None dummy
    statement = """
    SELECT * FROM schema.table as t WHERE a = b
    """
    expected = ["schema.table"]

    # act
    result = sut._parse_object_dependencies_views_static(statement)

    # assert
    assert result == expected


def test_parse_object_dependencies_views_static_should_match_stages():
    # arrange
    sut = DependencyParser(None)  # using None dummy
    statement = """
    SELECT
		$1,
        $2,
		METADATA$FILENAME AS FILENAME
	FROM @MY_SCHEMA.STAGE_TEST
    """
    expected = ["MY_SCHEMA.STAGE_TEST"]

    # act
    result = sut._parse_object_dependencies_views_static(statement)

    # assert
    assert result == expected


@pytest.mark.parametrize(
    "statement, expected_dependencies",
    [
        (
            """SELECT $1, $2, METADATA$FILENAME AS FILENAME
            FROM @MY_SCHEMA.STAGE_TEST
            (pattern => '.*sql[.]gz', file_format => MY_SCHEMA.MY_FF)""",
            ["MY_SCHEMA.STAGE_TEST", "MY_SCHEMA.MY_FF"],
        ),
        (
            """SELECT $1, $2, METADATA$FILENAME AS FILENAME
            FROM @MY_SCHEMA.STAGE_TEST
            (pattern => '.*sql[.]gz', file_format => 'MY_SCHEMA.MY_FF')""",
            ["MY_SCHEMA.STAGE_TEST", "MY_SCHEMA.MY_FF"],
        ),
        (
            """SELECT $1, $2, METADATA$FILENAME AS FILENAME
            FROM @MY_SCHEMA.STAGE_TEST
            (pattern => '.*sql[.]gz', file_format => "MY_SCHEMA"."MY_FF")""",
            ["MY_SCHEMA.STAGE_TEST", '"MY_SCHEMA"."MY_FF"'],
        ),
        (
            """SELECT $1, $2, METADATA$FILENAME AS FILENAME
            FROM @MY_SCHEMA.STAGE_TEST
            (pattern => '.*sql[.]gz', file_format => '"MY_SCHEMA"."MY_FF"')""",
            ["MY_SCHEMA.STAGE_TEST", '"MY_SCHEMA"."MY_FF"'],
        ),
    ],
)
def test_parse_object_dependencies_views_static_should_match_fileformats(
    statement, expected_dependencies
):
    # arrange
    sut = DependencyParser(None)  # using None dummy

    # act
    result = sut._parse_object_dependencies_views_static(statement)

    # assert
    assert result == expected_dependencies


@pytest.mark.parametrize(
    "statement, expected_dependencies",
    [
        (
            """SELECT COL1, COL2
            FROM MY_SCHEMA.MY_TABLE
            CHANGES (INFORMATION => APPEND_ONLY) AT (STREAM => 'MY_SCHEMA.MY_STREAM')""",
            ["MY_SCHEMA.MY_TABLE", "MY_SCHEMA.MY_STREAM"],
        ),
        (
            """SELECT COL1, COL2
            FROM MY_SCHEMA.MY_TABLE
            CHANGES (INFORMATION => APPEND_ONLY) AT (STREAM => '"MY_SCHEMA"."MY_STREAM"')""",
            ["MY_SCHEMA.MY_TABLE", '"MY_SCHEMA"."MY_STREAM"'],
        ),
    ],
)
def test_parse_object_dependencies_views_static_should_match_streams(
    statement, expected_dependencies
):
    # arrange
    sut = DependencyParser(None)  # using None dummy

    # act
    result = sut._parse_object_dependencies_views_static(statement)

    # assert
    assert result == expected_dependencies


def test_parse_object_dependencies_views_static_with_explicit_joins_should_return_list():
    # arrange
    sut = DependencyParser(None)  # using None dummy
    statement = """
    SELECT *
    FROM schema.table as t
    LEFT JOIN "test"."table2" as t2
        ON t.col = t2.col
    INNER JOIN table3
        on table3.id = t.id
    WHERE a = b
    """
    expected = ["schema.table", '"test"."table2"', "table3"]

    # act
    result = sut._parse_object_dependencies_views_static(statement)

    # assert
    assert result == expected


@pytest.mark.parametrize(
    "statement, expected_dependencies",
    [
        (
            """
    SELECT *
    FROM schema.table as t, "test"."table2" as t2
        ,table3
    WHERE
        t.col = t.col
    AND t.id = table3.id
    """,
            ["schema.table", '"test"."table2"', "table3"],
        ),
        (
            """
        		CREATE OR REPLACE VIEW DBP_MSI_VIEW2.MV_PLATZIERUNGSWG_SPR_ZU
(mandant_id
,platzierungswg_id
,platzierungswg_nr
,spr_id
,platzierungswg_bez
)
AS
   SELECT
  a10.mandant_id, a10.platzierungswg_id, platzierungswg_nr, spr_id, platzierungswg_bez
   FROM dbp_view.v_platzierungswg_spr_zu a10, dbp_view.v_l_platzierungswg a11

   WHERE a10.mandant_id = a11.mandant_id
   AND a10.platzierungswg_id = a11.platzierungswg_id
   AND a10.mandant_id = 1
   AND spr_id = 22;

        """,
            ["dbp_view.v_platzierungswg_spr_zu", "dbp_view.v_l_platzierungswg"],
        ),
        (
            """
        FROM bp_view.v_platzierungswg_spr_zu a10 , dbp_view.v_l_platzierungswg av, f, test as test , schema.bla aasfdkj , sdfskjk sdfksdjfhsdkjfh
        xxx yyy zzz
        FROM bp_view.v_platzierungswg_spr_zu2 a10, abc.xyz, aaaaa as bbb
        """,
            [
                "bp_view.v_platzierungswg_spr_zu",
                "dbp_view.v_l_platzierungswg",
                "f",
                "test",
                "schema.bla",
                "sdfskjk",
                "bp_view.v_platzierungswg_spr_zu2",
                "abc.xyz",
                "aaaaa",
            ],
        ),
    ],
)
def test_parse_object_dependencies_views_static_with_implicit_joins_should_return_list(
    statement, expected_dependencies
):
    # arrange
    sut = DependencyParser(None)  # using None dummy

    # act
    result = sut._parse_object_dependencies_views_static(statement)

    # assert
    assert set(result) == set(expected_dependencies)


def test_parse_object_dependencies_views_static_with_system_views_should_not_return_system_views():
    # arrange
    sut = DependencyParser(None)  # using None dummy
    statement = """
    SELECT *
    FROM table AS t
    LEFT JOIN information_schema.login_history('user') AS a
        ON t.col1 = a.col1
    """
    expected = ["table"]

    # act
    result = sut._parse_object_dependencies_views_static(statement)

    # assert
    assert result == expected


@pytest.mark.parametrize(
    "statement, expected_dependencies",
    [
        (
            """
        CREATE OR REPLACE VIEW DBP_MSI_VIEW_EK_INT.MV_WERBEWOCHE_KL
        AS
        SELECT mandant_id, dat, akt_kjwo_ww, akt_kjwo_ww_komplett, kjwo_ww
        ,Substr(To_Char(kjwo_ww),5,2) AS wo_ww
        ,Min(dat) Over (PARTITION BY mandant_id, kjwo_ww) AS ww_dat_von
        ,Max(dat) Over (PARTITION BY mandant_id, kjwo_ww) AS ww_dat_bis
        ,(
            Extract(YEAR From Min(dat) Over (PARTITION BY mandant_id, kjwo_ww)) * 100) +
            Extract(MONTH From Min(dat) Over (PARTITION BY mandant_id, kjwo_ww)
        ) AS ww_mo, Rank() Over (PARTITION BY mandant_id, kjwo_ww ORDER BY dat) AS ww_tag
        -- neue Tabelle wegen VorVortages-Logik
        FROM
        dbp_view.v_werbewoche_kl_vvt;
        """,
            ["dbp_view.v_werbewoche_kl_vvt"],
        ),
        (
            """CREATE OR REPLACE VIEW DBP_MSI_VIEW_REB.MV_JAHR_GJ
        (
        gj
        , akt_gj
        , akt_gj_komplett
        , akt_gj_help
        )
        AS
        SELECT
        gj, akt_gj, akt_gj_komplett, CASE WHEN EXTRACT (MONTH FROM(CURRENT_DATE)) = 3 THEN akt_gj +1 ELSE akt_gj END AS akt_gj_help

        FROM dbp_view.v_jahr_gj
        WHERE gj > 2001
        ;""",
            ["dbp_view.v_jahr_gj"],
        ),
        (
            """CREATE OR REPLACE VIEW DBP_MSI_VIEW_REB.MV_JAHR_GJ
        (
        gj
        , akt_gj
        , akt_gj_komplett
        , akt_gj_help
        )
        AS
        SELECT
        gj, akt_gj, akt_gj_komplett, CASE WHEN EXTRACT (MONTH FROM CURRENT_DATE) = 3 THEN akt_gj +1 ELSE akt_gj END AS akt_gj_help

        FROM dbp_view.v_jahr_gj
        WHERE gj > 2001
        ;""",
            ["dbp_view.v_jahr_gj"],
        ),
        (
            """CREATE OR REPLACE VIEW DBP_MSI_VIEW2.MV_MONAT
        (
        gjmo
        )
        AS
        SELECT
            gjmo
        , to_number(to_varchar(add_months(to_date(to_char(kjmo),'YYYYMM'),-1),'YYYYMM'))
        , (kj-EXTRACT(YEAR FROM CURRENT_DATE))*12+(MOD(kjmo, 100))-EXTRACT(MONTH FROM CURRENT_DATE)
        FROM dbp_view.v_monat;""",
            ["dbp_view.v_monat"],
        ),
    ],
)
def test_parse_object_dependencies_views_static_with_extract_function_should_not_return_extract_statement(
    statement, expected_dependencies
):
    """
    The EXTRACT satement uses the FROM keyword (e.g. EXTRACT(month FROM MIN(dat) OVER (...)))
    This FROM statement should not be interpreted as an external reference
    """

    # arrange
    sut = DependencyParser(None)

    # act
    result = sut._parse_object_dependencies_views_static(statement)

    # assert
    assert result == expected_dependencies


@pytest.mark.parametrize(
    "statement, expected_dependencies",
    [
        (
            """
            CREATE OR REPLACE VIEW s.v 
            WITH ROW ACCESS POLICY s.rap1 ON (my_col)
            AS SELECT ...                
            """,
            ["s.rap1"],
        ),
        (
            """
            CREATE OR REPLACE VIEW s.v 
            ROW ACCESS POLICY s.rap1 ON (my_col)
            AS SELECT ...                
            """,
            ["s.rap1"],
        ),
        (
            """
            create or replace view s.v 
            with row access policy s.rap1 on (my_col)
            as select ...                
            """,
            ["s.rap1"],
        ),
        (
            """
            CREATE OR REPLACE VIEW s.v 
            WITH
              ROW
                ACCESS
                  POLICY
                    s.rap1
                      ON (my_col)
            AS SELECT ...                
            """,
            ["s.rap1"],
        ),
        (
            """
            CREATE OR REPLACE VIEW s.v 
            WITH ROW ACCESS POLICY "s"."rap1" ON (my_col)
            AS SELECT ...                
            """,
            ['"s"."rap1"'],
        ),
    ],
)
def test_parse_object_dependencies_views_static_should_match_rap(
    statement, expected_dependencies
):
    """
    References to row access policies should be found
    """
    # arrange
    sut = DependencyParser(None)

    # act
    result = sut._parse_object_dependencies_views_static(statement)

    # assert
    assert result == expected_dependencies

@pytest.mark.parametrize(
    "statement, expected_dependencies",
    [
        (
            """
            CREATE OR REPLACE VIEW s.v 
            (
                A WITH MASKING POLICY s.mp1
            )
            AS SELECT ...                
            """,
            ['s.mp1'],
        ),
        (
            """
            CREATE OR REPLACE VIEW s.v 
            (
                A WITH MASKING POLICY s.mp1,
                B WITH MASKING POLICY s.mp1
            )
            AS SELECT ...                
            """,
            ['s.mp1', 's.mp1'],
        ),
        (
            """
            CREATE OR REPLACE VIEW s.v 
            (
                A WITH MASKING POLICY s.mp1,
                B WITH MASKING POLICY "s"."mp1"
            )
            AS SELECT ...                
            """,
            ['s.mp1', '"s"."mp1"'],
        ),
        (
            """
            CREATE OR REPLACE VIEW s.v 
            (
                A WITH MASKING POLICY s.mp1,
                B WITH MASKING POLICY s.mp2
            )
            AS SELECT ...                
            """,
            ['s.mp1', 's.mp2'],
        ),
        (
            """
            CREATE OR REPLACE VIEW s.v 
            (
                A MASKING POLICY s.mp1,
                B MASKING POLICY s.mp2
            )
            AS SELECT ...                
            """,
            ['s.mp1', 's.mp2'],
        ),
        (
            """
            create or replace view s.v 
            (
                a with masking policy s.mp1,
                b with masking policy s.mp2
            )
            as select ...                
            """,
            ['s.mp1', 's.mp2'],
        ),
        (
            """
            create or replace view s.v 
            (
                a 
                    with
                        masking
                            policy
                                s.mp1,
                b with masking policy s.mp2
            )
            as select ...                
            """,
            ['s.mp1', 's.mp2'],
        ),
    ],
)
def test_parse_object_dependencies_views_static_should_match_mp(
    statement, expected_dependencies
):
    """
    References to mapping should be found
    """
    # arrange
    sut = DependencyParser(None)

    # act
    result = sut._parse_object_dependencies_views_static(statement)

    # assert
    assert result == expected_dependencies

# @pytest.mark.parametrize('statement, expected_dependencies', [
#     # ("""
#     #     CREATE OR REPLACE VIEW myschema.myview4 AS
#     #     WITH abc AS (SELECT 'test' AS val)
#     #     SELECT * FROM abc;
#     #     """,
#     #     []
#     # ),("""
#     #     CREATE OR REPLACE VIEW T.myview4 AS
#     #     WITH abc AS (SELECT * FROM t.myview2),
#     #         xyz AS (SELECT * FROM t.myview)
#     #     SELECT abc.v2, xyz.v1 FROM abc
#     #     LEFT JOIN xyz
#     #     ON abc.v2 = xyz.v1;
#     #     """,
#     #     []
#     # ),("""
#     #     CREATE OR REPLACE VIEW T.myview4 AS
#     #     WITH abc AS (SELECT * FROM t.myview2)
#     #     SELECT abc.v2, xyz.v1 FROM abc
#     #     LEFT JOIN t.myview as xyz
#     #     ON abc.v2 = xyz.v1;
#     #     """,
#     #     ['t.myview']
#     # ),("""
#     #     CREATE OR REPLACE VIEW T.myview4 AS
#     #     SELECT * FROM (SELECT * FROM S.TABLE1) AS bezeichner;
#     #     """,
#     #     ['S.TABLE1']
#     # )
# ])
# def test_parse_object_dependencies_views_static_should_not_get_cte(statement, expected_dependencies):
#     """
#     CTE should not be parsed
#     """
#     # arrange
#     sut = DependencyParser(None)

#     # act
#     result = sut._parse_object_dependencies_views_static(statement)

#     # assert
#     assert result == expected_dependencies

# @pytest.mark.parametrize('statement, expected_dependencies', [
#     ("""
#     create or replace TABLE DBP_DATA.MARKTBESTAND_ERP_ZU (
#         BESTAND_ID NUMBER(38,0) NOT NULL, DEFAULT DBP_DATA.MARKTBESTAND_ERP_ZU_BESTAND_ID.NEXTVAL,
#         EK_NETTO NUMBER(18,4) NOT NULL DEFAULT 0);
#         """,
#         ['DBP_DATA.MARKTBESTAND_ERP_ZU_BESTAND_ID']
#     )
# ])
# def test_parse_object_dependencies_views_static_should_get_default_sequence(statement, expected_dependencies):
#     """
#     Default sequences should be found
#     """
#     # arrange
#     sut = DependencyParser(None)

#     # act
#     result = sut._parse_object_dependencies_views_static(statement)

#     # assert
#     assert result == expected_dependencies


@pytest.mark.parametrize(
    "statement, expected_dependencies",
    [
        (
            """
    SELECT *
    FROM (dbp_view.v_artbew_mo_ek_cp_sum v01
    JOIN dbp_view.v_mandant v03
    ON (v01.mandant_id = v03.mandant_id))
        """,
            ["dbp_view.v_artbew_mo_ek_cp_sum", "dbp_view.v_mandant"],
        ),
        (
            """
    SELECT colA
    FROM (
		SELECT colA
        FROM dbo.table1
    ) AS my_t,
    LEFT JOIN dbo.table2 AS t2
    ON my_t.colA = t2.colA
    GROUP BY colA
    """,
            ["dbo.table1", "dbo.table2"],
        ),
    ],
)
def test_parse_object_dependencies_views_static_should_get_statement_in_brackets(
    statement, expected_dependencies
):
    """
    from statements in brackets should be found
    """
    # act
    result = DependencyParser._parse_object_dependencies_views_static(statement)

    # assert
    assert result == expected_dependencies


def test_get_tables_and_views_with_multiple_depedencies_should_return_list():
    # arrange
    statement = """
    SELECT *
    FROM table1, schema1.table2 AS t2
    WHERE
        table1.col1 = t2.col1
    """

    # act
    result = DependencyParser._parse_object_dependencies_views_static(statement)

    # assert
    assert len(result) == 2


def test_get_tables_and_views_with_no_depedencies_should_return_empty_list():
    # arrange
    statement = """
    SELECT 0
    """

    # act
    result = DependencyParser._parse_object_dependencies_views_static(statement)

    # assert
    assert len(result) == 0


def test_get_tables_and_views_with_only_system_depedencies_should_return_empty_list():
    # arrange
    statement = """
    SELECT table_schema FROM information_schema.tables GROUP BY table_schema
    """

    # act
    result = DependencyParser._parse_object_dependencies_views_static(statement)

    # assert
    assert len(result) == 0


def test_get_tables_and_views_with_multiple_dependencies_should_return_no_system_dependencies():
    # arrange
    statement = """
    SELECT *
    FROM information_schema.tables AS t
    LEFT JOIN public.my_tables AS mt
    ON t.table_name = mt.table_name
    INNER JOIN other_schema.supertable
        ON other_schema.supertable.col1 = mt.col1
    """

    # act
    result = DependencyParser._parse_object_dependencies_views_static(statement)

    # assert
    assert len(result) == 2


@pytest.mark.parametrize(
    "statement, expected_count",
    [
        ("SELECT * FROM table1, table2 WHERE table1.col1 = table2.col1", 2),
        (
            'SELECT * FROM "dbo"."table_1" AS t1 JOIN public.tab2 AS t2 ON t1.col1 = t2.col1',
            2,
        ),
    ],
)
def test_get_tables_and_views_with_params(statement: str, expected_count: int):
    result = DependencyParser._parse_object_dependencies_views_static(statement)
    assert len(result) == expected_count


@pytest.mark.parametrize(
    "statement, expected_dependencies",
    [
        (
            """
        create or replace table s.t3(
        x int,
        y int,
        z int,
        constraint fk1 foreign key (x, y) references s.t1 (a, b),
        foreign key (z) references s.t2 (c)
        );
        """,
            ["s.t1", "s.t2"],
        ),
        (
            """
        create or replace table s.t3(
        x int,
        y int,
        z int,
        constraint fk1 foreign key(x, y) references s.t1(a, b),
        foreign key(z)references s.t2(c)
        );
        """,
            ["s.t1", "s.t2"],
        ),
        (
            """
        create or replace table s.t3(
        x int,
        y int,
        z int,
        constraint fk1 foreign key (x, y) references s.t1 (a, b),
        foreign key (z) references s.t1 (c)
        );
        """,
            ["s.t1"],
        ),
        (
            """
        create or replace table s.t3(
        x int,
        y int,
        z int,
        -- constraint fk1 foreign key (x, y) references s.t1 (a, b),
        foreign key (z) references s.t2 (c)
        );
        """,
            ["s.t2"],
        ),
        (
            """
        create or replace table s.t3(
        x int,
        y int,
        z int
        );
        """,
            [],
        ),
        (
            """
        create or replace table s.t3(
        x int,
        y int,
        z int
        );
        """,
            [],
        ),
    ],
)
def test_parse_object_dependencies_tables_fk_out_of_line(
    statement, expected_dependencies
):
    sut = DependencyParser(None)
    result = sut._parse_object_dependencies_tables(statement)
    assert isinstance(result, list)
    assert set(result) == set(expected_dependencies)


@pytest.mark.parametrize(
    "statement, expected_dependencies",
    [
        (
        """
           create or replace table t2 (a int, b int) with row access policy s.rap1 on (a);
        """,
            ["s.rap1"],
        ),
        (
        """
           create or replace table t2 (a int, b int) row access policy s.rap1 on (a);
        """,
            ["s.rap1"],
        ),
        (
        """
           CREATE OR REPLACE TABLE T2 (A INT, B INT) WITH ROW ACCESS POLICY S.RAP1 ON (A);
        """,
            ["S.RAP1"],
        ),
        (
        """
           create or replace table t2 (a int, b int) with row access policy "s"."rap1" on (a);
        """,
            ['"s"."rap1"'],
        ),
        (
        """
           create or replace table t2 (a int, b int)
             with
               row
                 access
                   policy
                     s.rap1
                       on
                         (a);
        """,
            ["s.rap1"],
        ),
    ],
)
def test_parse_object_dependencies_tables_rap(
    statement, expected_dependencies
):
    sut = DependencyParser(None)
    result = sut._parse_object_dependencies_tables(statement)
    assert isinstance(result, list)
    assert set(result) == set(expected_dependencies)

@pytest.mark.parametrize(
    "statement, expected_dependencies",
    [
        (
        """
            create or replace table t3 (
                a int with masking policy s.mp1,
                b int
            );
        """,
            ["s.mp1"],
        ),
        (
        """
            CREATE OR REPLACE TABLE T3 (
                A INT WITH MASKING POLICY S.MP1,
                B INT
            );
        """,
            ["S.MP1"],
        ),
        (
        """
            create or replace table t3 (
                a int with masking policy s.mp1 using (a),
                b int
            );
        """,
            ["s.mp1"],
        ),
        (
        """
            create or replace table t3 (
                a int with masking policy "s"."mp1",
                b int
            );
        """,
            ['"s"."mp1"'],
        ),
        (
        """
            create or replace table t3 (
                a int masking policy s.mp1,
                b int
            );
        """,
            ["s.mp1"],
        ),
        (
        """
            create or replace table t3 (
                a int with
                  masking
                    policy
                      s.mp1
                      ,
                b int
            );
        """,
            ["s.mp1"],
        ),
        (
        """
            create or replace table t3 (
                a int with masking policy s.mp1,
                b int with masking policy s.mp1
            );
        """,
            ["s.mp1", "s.mp1"],
        ),
        (
        """
            create or replace table t3 (
                a int with masking policy s.mp1,
                b int with masking policy s.mp2
            );
        """,
            ["s.mp1", "s.mp2"],
        ),
    ],
)
def test_parse_object_dependencies_tables_mp(
    statement, expected_dependencies
):
    sut = DependencyParser(None)
    result = sut._parse_object_dependencies_tables(statement)
    assert isinstance(result, list)
    assert set(result) == set(expected_dependencies)


@pytest.mark.parametrize(
    "statement, expected_dependencies",
    [
        (
            """
        create or replace table s.t3(
        x int,
        y int,
        z int
        );
        """,
            [],
        ),
        (
            """
        create or replace table s.t3(
        x int references s.t1 (a),
        y int,
        z int
        );
        """,
            ["s.t1"],
        ),
        (
            """
        create or replace table s.t3(
        x int references s.t1 (a),
        y int,
        z int references s.t2 (a)
        );
        """,
            ["s.t1", "s.t2"],
        ),
        (
            """
        create or replace table s.t3(
        x int references s.t1 (a),
        y int,
        z int references s.t1 (a)
        );
        """,
            ["s.t1"],
        ),
    ],
)
def test_parse_object_dependencies_tables_fk_inline(statement, expected_dependencies):
    sut = DependencyParser(None)
    result = sut._parse_object_dependencies_tables(statement)
    assert isinstance(result, list)
    assert set(result) == set(expected_dependencies)


@pytest.mark.parametrize(
    "statement, expected_dependencies",
    [
        (
            """
            CREATE or replace EXTERNAL TABLE s1.et1(
            a string as (value:c1::string),
            b int as (value:c2::int),
            c int as (value:c3::int)
            )
            LOCATION=@s1.stage1
            AUTO_REFRESH = true
            FILE_FORMAT=s1.my_file_format;
            """,
            ["s1.stage1", "s1.my_file_format"],
        ),
        (
            """
            CREATE or replace EXTERNAL TABLE s1.et1(
            a string as (value:c1::string),
            b int as (value:c2::int),
            c int as (value:c3::int)
            )
            LOCATION = @s1.stage1
            AUTO_REFRESH = true
            FILE_FORMAT = s1.my_file_format;
            """,
            ["s1.stage1", "s1.my_file_format"],
        ),
        (
            """
            CREATE or replace EXTERNAL TABLE s1.et1(
            a string as (value:c1::string),
            b int as (value:c2::int),
            c int as (value:c3::int)
            )
            LOCATION = @"s1"."stage1"
            AUTO_REFRESH = true
            FILE_FORMAT="s1"."my_file_format";
            """,
            ['"s1"."stage1"', '"s1"."my_file_format"'],
        ),
        (
            """
            CREATE or replace EXTERNAL TABLE s1.et1(
            a string as (value:c1::string),
            b int as (value:c2::int),
            c int as (value:c3::int)
            )
            LOCATION = @"s1"."stage1"
            AUTO_REFRESH = true
            FILE_FORMAT=(TYPE = CSV FIELD_DELIMITER = ',' SKIP_HEADER = 0);
            """,
            ['"s1"."stage1"'],
        ),
        (
            """
            CREATE OR REPLACE EXTERNAL TABLE STAGE.TBLEXT_CV_BC_0001(
            BNAME VARCHAR(16777216) AS ($1:BNAME::VARCHAR(16777216))
            ,NAME_FIRST VARCHAR(16777216) AS ($1:NAME_FIRST::VARCHAR(16777216))
            ,NAME_LAST VARCHAR(16777216) AS ($1:NAME_LAST::VARCHAR(16777216))
            ,NAME_TEXT VARCHAR(16777216) AS ($1:NAME_TEXT::VARCHAR(16777216))
            ,DBMS_USER VARCHAR(16777216) AS ($1:DBMS_USER::VARCHAR(16777216))
            ,SAML_USER VARCHAR(16777216) AS ($1:SAML_USER::VARCHAR(16777216))
            ,"COUNT" NUMBER(38,0) AS ($1:COUNT::NUMBER(38,0))
            ,_SRC VARCHAR(16777216) AS (METADATA$FILENAME)
            ,_ID NUMBER(38,0) AS (METADATA$FILE_ROW_NUMBER)
        )
            LOCATION=@STAGE.STGEX_DATAPLATFORM_SAP_AUTH_CURATED/CV_BC_0001/Mode=Full/
            AUTO_REFRESH=FALSE
            FILE_FORMAT=STAGE.FF_PARQUET
            PATTERN='(?i).*cv_bc.*[.]parquet'
            ;
            """,
            ["STAGE.STGEX_DATAPLATFORM_SAP_AUTH_CURATED", "STAGE.FF_PARQUET"],
        ),
    ],
)
def test_parse_object_dependencies_externaltables(statement, expected_dependencies):
    sut = DependencyParser(None)
    result = sut._parse_object_dependencies_externaltables(statement)
    assert isinstance(result, list)
    assert set(result) == set(expected_dependencies)


@pytest.mark.parametrize(
    "statement, expected",
    [
        (
            """
        create stream mystream on table myschema.mytable at(offset => -60*5);
        """,
            ["myschema.mytable"],
        ),
        (
            """
        create stream mystream on table "myschema"."mytable" at(offset => -60*5);
        """,
            ['"myschema"."mytable"'],
        ),
        (
            """
        create stream mystream on view myschema.myview append_only=true;
        """,
            ["myschema.myview"],
        ),
        (
            """
        create stream mystream on view "myschema"."myview" append_only=true;
        """,
            ['"myschema"."myview"'],
        ),
        (
            """
        create stream mystream on view
        myschema.myview append_only=true;
        """,
            ["myschema.myview"],
        ),
    ],
)
def test_parse_object_dependencies_streams(statement: str, expected: List[str]):
    result = DependencyParser._parse_object_dependencies_streams(statement)
    assert result == expected


@pytest.mark.parametrize(
    "statement, expected",
    [
        (
            """
        CREATE OR REPLACE TASK MISC.MY_FIRST_TASK
        WAREHOUSE = COMPUTE_WH
        SCHEDULE = 'USING CRON 0 * * * * UTC'
        AS
        INSERT INTO DATA.TABLE1 VALUES(1);
        """,
            [],
        ),
        (
            """
        CREATE OR REPLACE TASK MISC.MY_SECOND_TASK
        WAREHOUSE = COMPUTE_WH
        AFTER MISC.MY_FIRST_TASK
        AS
        INSERT INTO DATA.TABLE1 VALUES(2);
        """,
            ["MISC.MY_FIRST_TASK"],
        ),
        (
            """
        create or replace task misc.my_second_task
        warehouse = compute_wh
        after misc.my_first_task
        as
        insert into data.table1 values(2);
        """,
            ["misc.my_first_task"],
        ),
        (
            """
        CREATE OR REPLACE TASK MISC.MY_SECOND_TASK
        WAREHOUSE = COMPUTE_WH
        AFTER "MISC"."MY_FIRST_TASK"
        AS
        INSERT INTO DATA.TABLE1 VALUES(2);
        """,
            ['"MISC"."MY_FIRST_TASK"'],
        ),
        (
            """
        CREATE OR REPLACE TASK MISC.MY_SECOND_TASK
        WAREHOUSE = COMPUTE_WH
        AFTER misc.my_first_task
        AS
        INSERT INTO DATA.TABLE1 VALUES(2);
        """,
            ["misc.my_first_task"],
        ),
        (
            """
        CREATE OR REPLACE TASK MISC.MY_FIRST_TASK_AFTER
        WAREHOUSE = COMPUTE_WH
        SCHEDULE = 'USING CRON 0 * * * * UTC'
        AS
        INSERT INTO DATA.TABLE1 VALUES(1);
        """,
            [],
        ),
        (
            """
        CREATE OR REPLACE TASK MISC.MY_SECOND_TASK_AFTER
        WAREHOUSE = COMPUTE_WH
        COMMENT = 'runs after first task'
        AFTER MISC.MY_FIRST_TASK
        AS
        INSERT INTO DATA.TABLE1 VALUES(2);
        """,
            ["MISC.MY_FIRST_TASK"],
        ),
        (
            """
            CREATE or replace TASK MISC.MY_FOURTH_TASK
            WAREHOUSE = COMPUTE_WH
            AFTER MISC.MY_FIRST_TASK, MISC.MY_THIRD_TASK
            AS
            INSERT INTO DATA.TABLE1 VALUES(2);
            """,
            ["MISC.MY_FIRST_TASK", "MISC.MY_THIRD_TASK"],
        ),
        (
            """
            CREATE or replace TASK MISC.MY_FOURTH_TASK
            WAREHOUSE = COMPUTE_WH
            AFTER MISC.MY_FIRST_TASK,MISC.MY_THIRD_TASK
            AS
            INSERT INTO DATA.TABLE1 VALUES(2);
            """,
            ["MISC.MY_FIRST_TASK", "MISC.MY_THIRD_TASK"],
        ),
        (
            """
            CREATE or replace TASK MISC.MY_FOURTH_TASK
            WAREHOUSE = COMPUTE_WH
            AFTER MISC.MY_FIRST_TASK,
            MISC.MY_THIRD_TASK
            ,MISC.MY_SECOND_TASK
            AS
            INSERT INTO DATA.TABLE1 VALUES(2);
            """,
            ["MISC.MY_FIRST_TASK", "MISC.MY_THIRD_TASK", "MISC.MY_SECOND_TASK"],
        ),
        (
            """
            CREATE or replace TASK MISC.MY_FOURTH_TASK WAREHOUSE = COMPUTE_WH AFTER MISC.MY_FIRST_TASK , MISC.MY_THIRD_TASK AS INSERT INTO DATA.TABLE1 VALUES(2);
            """,
            ["MISC.MY_FIRST_TASK", "MISC.MY_THIRD_TASK"],
        ),
    ],
)
def test_parse_object_dependencies_tasks(statement: str, expected: List[str]):
    result = DependencyParser._parse_object_dependencies_tasks(statement)
    assert result == expected


@pytest.mark.parametrize(
    "statement, expected",
    [
        (
            """
        CREATE STAGE MISC.MY_EXTERNAL_STAGE
            url='azure://example.blob.core.windows.net/test'
            credentials=(azure_sas_token='?sp=r&st=2021-06-14T14:45:56Z&se=2021-06-14T22:45:56Z&spr=https&sv=2020-02-10&sr=c&sig=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
            file_format = MISC.MY_CSV_FORMAT;
        """,
            ["MISC.MY_CSV_FORMAT"],
        ),
        (
            """
        create stage misc.my_external_stage
            url='azure://example.blob.core.windows.net/test'
            credentials=(azure_sas_token='?sp=r&st=2021-06-14t14:45:56z&se=2021-06-14t22:45:56z&spr=https&sv=2020-02-10&sr=c&sig=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
            file_format = misc.my_csv_format;
        """,
            ["misc.my_csv_format"],
        ),
        (
            """
        CREATE STAGE MISC.MY_EXTERNAL_STAGE
            url='azure://example.blob.core.windows.net/test'
            credentials=(azure_sas_token='?sp=r&st=2021-06-14T14:45:56Z&se=2021-06-14T22:45:56Z&spr=https&sv=2020-02-10&sr=c&sig=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
            file_format = (format_name = MISC.MY_CSV_FORMAT);
        """,
            ["MISC.MY_CSV_FORMAT"],
        ),
        (
            """
        CREATE STAGE MISC.MY_EXTERNAL_STAGE
            url='azure://example.blob.core.windows.net/test'
            credentials=(azure_sas_token='?sp=r&st=2021-06-14T14:45:56Z&se=2021-06-14T22:45:56Z&spr=https&sv=2020-02-10&sr=c&sig=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
            file_format = 'MISC.MY_CSV_FORMAT';
        """,
            ["MISC.MY_CSV_FORMAT"],
        ),
        (
            """
        CREATE STAGE MISC.MY_EXTERNAL_STAGE
            url='azure://example.blob.core.windows.net/test'
            credentials=(azure_sas_token='?sp=r&st=2021-06-14T14:45:56Z&se=2021-06-14T22:45:56Z&spr=https&sv=2020-02-10&sr=c&sig=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
            file_format = (format_name = 'MISC.MY_CSV_FORMAT');
        """,
            ["MISC.MY_CSV_FORMAT"],
        ),
        (
            """
        CREATE STAGE MISC.MY_EXTERNAL_STAGE
            url='azure://example.blob.core.windows.net/test'
            credentials=(azure_sas_token='?sp=r&st=2021-06-14T14:45:56Z&se=2021-06-14T22:45:56Z&spr=https&sv=2020-02-10&sr=c&sig=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
            file_format = (TYPE = CSV COMPRESSION = AUTO);
        """,
            [],
        ),
    ],
)
def test_parse_object_dependencies_stages(statement: str, expected: List[str]):
    result = DependencyParser._parse_object_dependencies_stages(statement)
    assert len(result) == len(expected)
    assert set(result) == set(expected)


@pytest.mark.parametrize(
    "statement, expected",
    [
        (
            """
        CREATE PIPE MISC.MY_PIPE
            AUTO_INGEST = FALSE
            AS COPY INTO DATA.TABLE1
            FROM @MISC.MY_EXTERNAL_STAGE
            FILE_FORMAT = MISC.MY_CSV_FORMAT;
        """,
            ["DATA.TABLE1", "MISC.MY_EXTERNAL_STAGE", "MISC.MY_CSV_FORMAT"],
        ),
        (
            """
        create pipe misc.my_pipe
            auto_ingest = false
            as copy into data.table1
            from @misc.my_external_stage
            file_format = misc.my_csv_format;
        """,
            ["data.table1", "misc.my_external_stage", "misc.my_csv_format"],
        ),
        (
            """
        CREATE PIPE "MISC"."MY_PIPE"
            AUTO_INGEST = FALSE
            AS COPY INTO "DATA"."TABLE1"
            FROM @"MISC"."MY_EXTERNAL_STAGE"
            FILE_FORMAT = "MISC"."MY_CSV_FORMAT";
        """,
            ['"DATA"."TABLE1"', '"MISC"."MY_EXTERNAL_STAGE"', '"MISC"."MY_CSV_FORMAT"'],
        ),
        (
            """
        CREATE PIPE "MISC"."MY_PIPE"
            AUTO_INGEST = FALSE
            AS COPY INTO "DATA".TABLE1
            FROM @MISC."MY_EXTERNAL_STAGE1"
            FILE_FORMAT = 'MISC.MY_CSV_FORMAT1';
        """,
            ['"DATA".TABLE1', 'MISC."MY_EXTERNAL_STAGE1"', "MISC.MY_CSV_FORMAT1"],
        ),
        (
            """
        CREATE PIPE "MISC"."MY_PIPE"
            AUTO_INGEST = FALSE
            AS COPY INTO "DATA".TABLE1
            FROM @MISC."MY_EXTERNAL_STAGE1"
            FILE_FORMAT = (FORMAT_NAME = 'MISC.MY_CSV_FORMAT1');
        """,
            ['"DATA".TABLE1', 'MISC."MY_EXTERNAL_STAGE1"', "MISC.MY_CSV_FORMAT1"],
        ),
    ],
)
def test_parse_object_dependencies_pipes(statement: str, expected: List[str]):
    result = DependencyParser._parse_object_dependencies_pipes(statement)
    assert len(result) == len(expected)
    assert set(result) == set(expected)

@pytest.mark.parametrize( # TODO
    "statement, expected_dependencies",
    [
        (
            """
            CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 (COLUMN_1, COLUMN_2)
            TARGET_LAG = '2 hours'
            WAREHOUSE = COMPUTE_WH
            DATA_RETENTION_TIME_IN_DAYS = 0
            COMMENT = 'TEST COMMENT'
            REFRESH_MODE = AUTO
            AS
            SELECT COLUMN_1, MY_COLUMN AS COLUMN_2
            FROM DATA.VIEW1;
            """,
            ["DATA.VIEW1"],
        ),
        (
            """
            CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 (COLUMN_1, COLUMN_2)
            TARGET_LAG = '2 hours'
            WAREHOUSE = COMPUTE_WH
            DATA_RETENTION_TIME_IN_DAYS = 0
            COMMENT = 'TEST COMMENT'
            REFRESH_MODE = AUTO
            AS
            SELECT COLUMN_1, MY_COLUMN AS COLUMN_2
            FROM "DATA".TABLE1;
            """,
            ['"DATA".TABLE1'],
        ),
        (
            """
            CREATE OR REPLACE DYNAMIC TABLE DATA.DYNAMICTABLE1 (COLUMN_1, COLUMN_2)
            TARGET_LAG = '2 hours'
            WAREHOUSE = COMPUTE_WH
            DATA_RETENTION_TIME_IN_DAYS = 0
            COMMENT = 'TEST COMMENT'
            REFRESH_MODE = AUTO
            AS
            SELECT COLUMN_1
            FROM DATA.VIEW1
            UNION
            SELECT COLUMN_2
            FROM DATA.VIEW2;
            """,
            ["DATA.VIEW1", "DATA.VIEW2"],
        ),
        (
            """
            CREATE or replace DYNAMIC TABLE (
                COLUMN_1 WITH MASKING POLICY s.mp1,
                COLUMN_2 WITH MASKING POLICY s.mp2
            )TARGET_LAG = '2 hours'
            WAREHOUSE = COMPUTE_WH
            DATA_RETENTION_TIME_IN_DAYS = 0
            COMMENT = 'TEST COMMENT'
            REFRESH_MODE = AUTO
            AS
            SELECT COLUMN_1, MY_COLUMN AS COLUMN_2
            FROM DATA.VIEW1;
            """,
            ["DATA.VIEW1", "s.mp1", "s.mp2"],
        ),
        (
             """
            CREATE or replace DYNAMIC TABLE (
                my_col
            )TARGET_LAG = '2 hours'
            WAREHOUSE = COMPUTE_WH
            DATA_RETENTION_TIME_IN_DAYS = 0
            COMMENT = 'TEST COMMENT'
            REFRESH_MODE = AUTO
            with row access policy s.rap1 on (my_col)
            AS
            SELECT my_col
            FROM DATA.VIEW1;
            """,
            ["DATA.VIEW1", "s.rap1"],
        ),
    ],
)
def test_parse_object_dependencies_dynamictables_static(statement, expected_dependencies):
    sut = DependencyParser(None)
    result = sut._parse_object_dependencies_dynamictables_static(statement)
    assert isinstance(result, list)
    assert set(result) == set(expected_dependencies)



def test_dummy_parser_empty_result():
    statement = "dummy"
    result = DependencyParser._dummy_parser_empty_result(statement)
    assert result == []


@pytest.mark.parametrize(
    "statement, function_name_list, expected",
    [
        (
            """
        CREATE OR REPLACE VIEW S.V AS SELECT
            S.AREA(RADIUS) AS AREA
            FROM S.T;
        """,
            ["S.AREA"],
            ["S.T", "S.AREA"],
        ),
        (
            """
        CREATE OR REPLACE VIEW S.V AS SELECT
            s.area(RADIUS) AS AREA
            FROM S.T;
        """,
            ["S.AREA"],
            ["S.T", "s.area"],
        ),
        (
            """
        CREATE OR REPLACE VIEW S.V AS SELECT
            S.AREA     ( RADIUS ) AS AREA
            FROM S.T;
        """,
            ["S.AREA"],
            ["S.T", "S.AREA"],
        ),
        (
            """
        CREATE OR REPLACE VIEW S.V AS SELECT
            "S"."AREA"(RADIUS) AS AREA
            FROM S.T;
        """,
            ["S.AREA"],
            ["S.T", "S.AREA"],
        ),
        (
            """
        CREATE OR REPLACE VIEW S.V AS SELECT
            "S".AREA(RADIUS) AS AREA
            FROM S.T;
        """,
            ["S.AREA"],
            ["S.T", "S.AREA"],
        ),
        (
            """
        CREATE OR REPLACE VIEW S.V AS SELECT
            S.AREA(RADIUS) AS AREA
            FROM S.T;
        """,
            [],
            ["S.T"],
        ),
        (
            """
        CREATE OR REPLACE VIEW S.V AS SELECT
            S.AREA(RADIUS) AS AREA
            FROM S.T;
        """,
            ["S.AREA", "S.VOLUME"],
            ["S.T", "S.AREA"],
        ),
        (
            """
        CREATE OR REPLACE VIEW S.V AS SELECT
            S.AREA(RADIUS) AS AREA,
            S.VOLUME(RADIUS) AS VOLUME
            FROM S.T;
        """,
            ["S.AREA", "S.VOLUME"],
            ["S.T", "S.AREA", "S.VOLUME"],
        ),
    ],
)
def test_parse_function_references_are_resolved(
    statement: str, function_name_list: List[str], expected: List[str]
):
    result = (
        DependencyParser._parse_object_dependencies_views_functions_policies_static(
            statement, function_name_list
        )
    )
    assert len(result) == len(expected)
    assert set(result) == set(expected)


@pytest.mark.parametrize(
    "statement, function_name_list, expected",
    [
        (
            """
                CREATE OR REPLACE FUNCTION "PUBLIC"."PERIOD_CONTAINS_UDF"("PERIOD_1" VARCHAR(22), "PERIOD_2" DATE)
                RETURNS BOOLEAN
                LANGUAGE SQL
                IMMUTABLE
                AS $$    PUBLIC.PERIOD_BEGIN_UDF(PERIOD_1) <= PERIOD_2 AND PUBLIC.PERIOD_END_UDF(PERIOD_1) >= PERIOD_2 $$;
            """,
            ["PUBLIC.PERIOD_BEGIN_UDF", "PUBLIC.PERIOD_END_UDF", "A.B"],
            ["PUBLIC.PERIOD_BEGIN_UDF", "PUBLIC.PERIOD_END_UDF"],
        ),
        (
            """
                CREATE OR REPLACE FUNCTION "PUBLIC"."PERIOD_CONTAINS_UDF"("PERIOD_1" VARCHAR(22), "PERIOD_2" DATE)
                RETURNS BOOLEAN
                LANGUAGE SQL
                IMMUTABLE
                AS '    PUBLIC.PERIOD_BEGIN_UDF(PERIOD_1) <= PERIOD_2 AND PUBLIC.PERIOD_END_UDF(PERIOD_1) >= PERIOD_2 ';
            """,
            ["PUBLIC.PERIOD_BEGIN_UDF", "PUBLIC.PERIOD_END_UDF", "A.B"],
            ["PUBLIC.PERIOD_BEGIN_UDF", "PUBLIC.PERIOD_END_UDF"],
        ),
        (
            """
                CREATE OR REPLACE FUNCTION "PUBLIC"."PERIOD_CONTAINS_UDF"("PERIOD_1" VARCHAR(22), "PERIOD_2" DATE)
                RETURNS BOOLEAN
                LANGUAGE SQL
                IMMUTABLE
                AS $$    "PUBLIC"."PERIOD_BEGIN_UDF"(PERIOD_1) <= PERIOD_2 AND "PUBLIC"."PERIOD_END_UDF"(PERIOD_1) >= PERIOD_2 $$;
            """,
            ["PUBLIC.PERIOD_BEGIN_UDF", "PUBLIC.PERIOD_END_UDF", "A.B"],
            ["PUBLIC.PERIOD_BEGIN_UDF", "PUBLIC.PERIOD_END_UDF"],
        ),
        (
            """
                CREATE OR REPLACE FUNCTION "PUBLIC"."PERIOD_CONTAINS_UDF"("PERIOD_1" VARCHAR(22), "PERIOD_2" DATE)
                RETURNS BOOLEAN
                LANGUAGE SQL
                IMMUTABLE
                AS '    PUBLIC.PERIOD_BEGIN_UDF(PERIOD_1) <= PERIOD_2 AND PUBLIC.PERIOD_END_UDF(PERIOD_1) >= PERIOD_2 ';
            """,
            ["PUBLIC.PERIOD_BEGIN_UDF", "A.B"],
            ["PUBLIC.PERIOD_BEGIN_UDF"],
        ),
    ],
)
def test_parse_object_dependencies_functions_static(
    statement: str, function_name_list: List[str], expected: List[str]
):
    result = (
        DependencyParser._parse_object_dependencies_functions_static(
            statement, function_name_list
        )
    )
    assert len(result) == len(expected)
    assert set(result) == set(expected)
