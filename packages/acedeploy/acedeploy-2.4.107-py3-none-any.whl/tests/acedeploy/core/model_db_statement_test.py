import acedeploy.core.model_db_statement as mds
import pytest
from acedeploy.core.model_sql_entities import DbObjectType


def test_init_DbStatement():
    result = mds.DbStatement(
        schema="my_schema",
        name="my_object",
        statement="create or replace my_schema.my_object;",
        object_type=DbObjectType.TABLE,
    )
    assert result.schema == "MY_SCHEMA"
    assert result.name == "MY_OBJECT"
    assert result.statement == "create or replace my_schema.my_object;"
    assert result.id == "DbObjectType.TABLE MY_SCHEMA.MY_OBJECT"
    assert repr(result) == "DbStatement: DbObjectType.TABLE MY_SCHEMA.MY_OBJECT"
    assert str(result) == "DbStatement: DbObjectType.TABLE MY_SCHEMA.MY_OBJECT"


def test_equality_DbStatement():
    s1 = mds.DbStatement(
        schema="my_schema",
        name="my_object",
        statement="create or replace my_schema.my_object;",
        object_type=DbObjectType.TABLE,
    )
    s2 = mds.DbStatement(
        schema="my_schema",
        name="my_object",
        statement="create or replace my_schema.my_object;",
        object_type=DbObjectType.TABLE,
    )
    assert s1 == s2


@pytest.mark.parametrize(
    "_input1, _input2",
    [
        (
            mds.DbStatement(
                schema="my_schema1",
                name="my_object1",
                statement="create or replace my_schema1.my_object1;",
                object_type=DbObjectType.TABLE,
            ),
            mds.DbStatement(
                schema="my_schema2",
                name="my_object1",
                statement="create or replace my_schema1.my_object1;",
                object_type=DbObjectType.TABLE,
            ),
        ),
        (
            mds.DbStatement(
                schema="MY_SCHEMA1",
                name="my_object1",
                statement="create or replace MY_SCHEMA1.my_object1;",
                object_type=DbObjectType.TABLE,
            ),
            mds.DbStatement(
                schema="my_schema1",
                name="my_object1",
                statement="create or replace my_schema1.my_object1;",
                object_type=DbObjectType.TABLE,
            ),
        ),
        (
            mds.DbStatement(
                schema="my_schema1",
                name="my_object1",
                statement="create or replace my_schema1.my_object1;",
                object_type=DbObjectType.TABLE,
            ),
            mds.DbStatement(
                schema="my_schema1",
                name="my_object2",
                statement="create or replace my_schema1.my_object1;",
                object_type=DbObjectType.TABLE,
            ),
        ),
        (
            mds.DbStatement(
                schema="my_schema1",
                name="my_object1",
                statement="create or replace my_schema1.my_object1;",
                object_type=DbObjectType.TABLE,
            ),
            mds.DbStatement(
                schema="my_schema1",
                name="my_object1",
                statement="create my_schema1.my_object1;",
                object_type=DbObjectType.TABLE,
            ),
        ),
        (
            mds.DbStatement(
                schema="my_schema1",
                name="my_object1",
                statement="create or replace my_schema1.my_object1;",
                object_type=DbObjectType.TABLE,
            ),
            mds.DbStatement(
                schema="my_schema1",
                name="my_object1",
                statement="create or replace my_schema1.my_object1;",
                object_type=DbObjectType.VIEW,
            ),
        ),
    ],
)
def test_inequality_DbStatement(_input1, _input2):
    assert not (_input1 == _input2)
