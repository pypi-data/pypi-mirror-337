import os
from typing import List
from unittest.mock import patch

import acedeploy.core.model_db_statement as mds
import acedeploy.services.deploy_service as ds
import pytest
from acedeploy.core.model_sql_entities import DbActionType, DbObjectType
from db_compare_service_test import DummyDbObjectAction


@pytest.mark.parametrize(
    "original_statement, expected",
    [
        (
            mds.DbStatement(
                schema="my_schema1",
                name="my_object1",
                statement="",
                object_type=DbObjectType.TABLE,
            ),
            "ALTER TABLE IF EXISTS DB_TARGET.MY_SCHEMA1.MY_OBJECT1 RENAME TO DB_TARGET.MY_SCHEMA1.MY_OBJECT1_ROLLBACK_MY_RELEASE_123;ALTER TABLE IF EXISTS DB_ROLLBACK.MY_SCHEMA1.MY_OBJECT1 RENAME TO DB_TARGET.MY_SCHEMA1.MY_OBJECT1;",
        ),
        (
            mds.DbStatement(
                schema="my_schema1",
                name="my_object1",
                statement="",
                object_type=DbObjectType.VIEW,
            ),
            "ALTER VIEW IF EXISTS DB_TARGET.MY_SCHEMA1.MY_OBJECT1 RENAME TO DB_TARGET.MY_SCHEMA1.MY_OBJECT1_ROLLBACK_MY_RELEASE_123;ALTER VIEW IF EXISTS DB_ROLLBACK.MY_SCHEMA1.MY_OBJECT1 RENAME TO DB_TARGET.MY_SCHEMA1.MY_OBJECT1;",
        ),
        (
            mds.DbStatement(
                schema="my_schema1",
                name="my_object1",
                statement="",
                object_type=DbObjectType.MATERIALIZEDVIEW,
            ),
            "ALTER MATERIALIZED VIEW IF EXISTS DB_TARGET.MY_SCHEMA1.MY_OBJECT1 RENAME TO DB_TARGET.MY_SCHEMA1.MY_OBJECT1_ROLLBACK_MY_RELEASE_123;ALTER MATERIALIZED VIEW IF EXISTS DB_ROLLBACK.MY_SCHEMA1.MY_OBJECT1 RENAME TO DB_TARGET.MY_SCHEMA1.MY_OBJECT1;",
        ),
        (
            mds.DbStatement(
                schema="my_schema1",
                name="my_object1",
                statement="",
                object_type=DbObjectType.FILEFORMAT,
            ),
            "ALTER FILE FORMAT IF EXISTS DB_TARGET.MY_SCHEMA1.MY_OBJECT1 RENAME TO DB_TARGET.MY_SCHEMA1.MY_OBJECT1_ROLLBACK_MY_RELEASE_123;ALTER FILE FORMAT IF EXISTS DB_ROLLBACK.MY_SCHEMA1.MY_OBJECT1 RENAME TO DB_TARGET.MY_SCHEMA1.MY_OBJECT1;",
        ),
        (
            mds.ParametersObjectStatement(
                schema="my_schema1",
                name="my_object1",
                statement="",
                object_type=DbObjectType.FUNCTION,
                parameters=["FLOAT", "VARCHAR"],
            ),
            "ALTER FUNCTION IF EXISTS DB_TARGET.MY_SCHEMA1.MY_OBJECT1 (FLOAT, VARCHAR) RENAME TO DB_TARGET.MY_SCHEMA1.MY_OBJECT1_ROLLBACK_MY_RELEASE_123;ALTER FUNCTION IF EXISTS DB_ROLLBACK.MY_SCHEMA1.MY_OBJECT1 (FLOAT, VARCHAR) RENAME TO DB_TARGET.MY_SCHEMA1.MY_OBJECT1;",
        ),
        (
            mds.ParametersObjectStatement(
                schema="my_schema1",
                name="my_object1",
                statement="",
                object_type=DbObjectType.FUNCTION,
                parameters=[],
            ),
            "ALTER FUNCTION IF EXISTS DB_TARGET.MY_SCHEMA1.MY_OBJECT1 () RENAME TO DB_TARGET.MY_SCHEMA1.MY_OBJECT1_ROLLBACK_MY_RELEASE_123;ALTER FUNCTION IF EXISTS DB_ROLLBACK.MY_SCHEMA1.MY_OBJECT1 () RENAME TO DB_TARGET.MY_SCHEMA1.MY_OBJECT1;",
        ),
        (
            mds.ParametersObjectStatement(
                schema="my_schema1",
                name="my_object1",
                statement="",
                object_type=DbObjectType.PROCEDURE,
                parameters=["FLOAT", "VARCHAR"],
            ),
            "ALTER PROCEDURE IF EXISTS DB_TARGET.MY_SCHEMA1.MY_OBJECT1 (FLOAT, VARCHAR) RENAME TO DB_TARGET.MY_SCHEMA1.MY_OBJECT1_ROLLBACK_MY_RELEASE_123;ALTER PROCEDURE IF EXISTS DB_ROLLBACK.MY_SCHEMA1.MY_OBJECT1 (FLOAT, VARCHAR) RENAME TO DB_TARGET.MY_SCHEMA1.MY_OBJECT1;",
        ),
        (
            mds.ParametersObjectStatement(
                schema="my_schema1",
                name="my_object1",
                statement="",
                object_type=DbObjectType.PROCEDURE,
                parameters=[],
            ),
            "ALTER PROCEDURE IF EXISTS DB_TARGET.MY_SCHEMA1.MY_OBJECT1 () RENAME TO DB_TARGET.MY_SCHEMA1.MY_OBJECT1_ROLLBACK_MY_RELEASE_123;ALTER PROCEDURE IF EXISTS DB_ROLLBACK.MY_SCHEMA1.MY_OBJECT1 () RENAME TO DB_TARGET.MY_SCHEMA1.MY_OBJECT1;",
        ),
    ],
)
def test_generate_rollback_statement(original_statement, expected):
    result = ds.DeployService._generate_rollback_statement(
        original_statement=original_statement,
        target_db_name="DB_TARGET",
        rollback_db_name="DB_ROLLBACK",
        release_name_clean="MY_RELEASE_123",
    )
    assert result == expected


@pytest.mark.parametrize(
    "original_statement",
    [
        mds.DbStatement(
            schema="my_schema1",
            name="my_object1",
            statement="",
            object_type=DbObjectType.STREAM,
        ),
        mds.DbStatement(
            schema="my_schema1",
            name="my_object1",
            statement="",
            object_type=DbObjectType.STAGE,
        ),
        mds.DbStatement(
            schema="my_schema1",
            name="my_object1",
            statement="",
            object_type=DbObjectType.TASK,
        ),
        mds.DbStatement(
            schema="my_schema1",
            name="my_object1",
            statement="",
            object_type=DbObjectType.PIPE,
        ),
    ],
)
def test_generate_rollback_statement_error(original_statement):
    with pytest.raises(ValueError):
        _ = ds.DeployService._generate_rollback_statement(
            original_statement=original_statement,
            target_db_name="DB_TARGET",
            rollback_db_name="DB_ROLLBACK",
            release_name_clean="MY_RELEASE_123",
        )


@pytest.mark.parametrize(
    "action_list, schema_list, expected",
    [
        (
            [
                DummyDbObjectAction(
                    "CORE",
                    "VIEW2",
                    "CREATE VIEW CORE.VIEW2 AS SELECT col1 FROM CORE.TABLE0;",
                    DbObjectType.MATERIALIZEDVIEW,
                    DbActionType.ADD
                ),
                DummyDbObjectAction(
                    "VIEWS",
                    "VIEW_DROP_ME",
                    None,
                    DbObjectType.MATERIALIZEDVIEW,
                    DbActionType.DROP
                )
            ],
            {"blacklist":["core"]},
            {"whitelist":["views"]}
        )
       ,
        (
            [
                DummyDbObjectAction(
                    "CORE",
                    "VIEW2",
                    "CREATE VIEW CORE.VIEW2 AS SELECT col1 FROM CORE.TABLE0;",
                    DbObjectType.MATERIALIZEDVIEW,
                    DbActionType.ADD
                ),
                DummyDbObjectAction(
                    "VIEWS",
                    "VIEW_DROP_ME",
                    None,
                    DbObjectType.MATERIALIZEDVIEW,
                    DbActionType.DROP
                )
            ],
            {"whitelist":["views"]},
            {"whitelist":["views"]}
       ),(
            [
                DummyDbObjectAction(
                    "CORE",
                    "VIEW2",
                    "CREATE VIEW CORE.VIEW2 AS SELECT col1 FROM CORE.TABLE0;",
                    DbObjectType.MATERIALIZEDVIEW,
                    DbActionType.ADD
                ),
                DummyDbObjectAction(
                    "VIEWS",
                    "VIEW_DROP_ME",
                    None,
                    DbObjectType.MATERIALIZEDVIEW,
                    DbActionType.DROP
                )
            ],
            None,
            {"whitelist":["core","views"]}
       ),(
            [
                DummyDbObjectAction(
                    "CORE",
                    "VIEW2",
                    "CREATE VIEW CORE.VIEW2 AS SELECT col1 FROM CORE.TABLE0;",
                    DbObjectType.MATERIALIZEDVIEW,
                    DbActionType.ADD
                ),
                DummyDbObjectAction(
                    "VIEWS",
                    "VIEW_DROP_ME",
                    None,
                    DbObjectType.MATERIALIZEDVIEW,
                    DbActionType.DROP
                )
            ],
            {},
            {"whitelist":["core","views"]}
       ),(
            [
                DummyDbObjectAction(
                    "CORE",
                    "VIEW2",
                    "CREATE VIEW CORE.VIEW2 AS SELECT col1 FROM CORE.TABLE0;",
                    DbObjectType.MATERIALIZEDVIEW,
                    DbActionType.ADD
                ),
                DummyDbObjectAction(
                    "VIEWS",
                    "VIEW_DROP_ME",
                    None,
                    DbObjectType.MATERIALIZEDVIEW,
                    DbActionType.DROP
                )
            ],
            {"whitelist":["CORE","views","schema_1"]},
            {"whitelist":["core","views"]}
       )
        
    ],
)
def test_filter_schema_list_by_action_list(action_list, schema_list, expected):
    result = ds.DeployService._filter_schema_list_by_action_list(
        action_list=action_list,
        schema_list=schema_list,
    )
    assert result == expected