import acedeploy.core.model_database_object as mdo
import pytest
from acedeploy.core.model_sql_entities import DbObjectType


def test_DatabaseObject_not_instanietable():
    with pytest.raises(TypeError):
        mdo.DatabaseObject(
            "myschema", "mytable", DbObjectType.TABLE
        )  # pylint: disable=abstract-class-instantiated


class DummyDatabaseObject(mdo.DatabaseObject):
    def __str__(self):
        return f"DummyDatabaseObject: {self.id}"

    def __repr__(self):
        return f"DummyDatabaseObject: {self.id}"


def test_properties():
    obj = DummyDatabaseObject("my_schema", "my_name", DbObjectType.TABLE)
    assert obj.schema == "MY_SCHEMA"
    assert obj.name == "MY_NAME"
    assert obj.object_type == DbObjectType.TABLE
    assert obj.id == f"{str(DbObjectType.TABLE)} MY_SCHEMA.MY_NAME"


def test_object_type_error():
    with pytest.raises(TypeError):
        __ = DummyDatabaseObject("my_schema", "my_name", "DbObjectType.TABLE")


@pytest.mark.parametrize(
    "test_object_schema, test_object_name, compare_object_name, expected",
    [
        ("schema", "name", "schema.name", True),
        ("schema", "name", "wrong.name", False),
        ("schema", "name", "schema.wrong", False),
        ('"schema"', '"name"', '"wrong"."name"', False),
        ('"schema"', '"name"', '"schema"."wrong"', False),
        ('"schema"', '"name"', '"schema"."name"', True),
        ('"schema"', "name", '"schema"."name"', True),
        ("schema", '"name"', '"schema"."name"', True),
        ("schema", "name", '"schema"."name"', True),
        ("schema", "name", '"schema".name', True),
        ("schema", "name", 'schema."name"', True),
    ],
)
def test_compare_full_name(
    test_object_schema, test_object_name, compare_object_name, expected
):
    obj = DummyDatabaseObject(test_object_schema, test_object_name, DbObjectType.TABLE)
    assert obj.compare_full_name(compare_object_name) == expected


@pytest.mark.parametrize(
    "test_object_schema, test_object_name, test_object_type, compare_object_id, expected",
    [
        ("schema", "name", DbObjectType.TABLE, "DbObjectType.TABLE SCHEMA.NAME", True),
        ("schema", "name", DbObjectType.TABLE, "DbObjectType.TABLE schema.NAME", False),
        (
            "schema",
            "name",
            DbObjectType.TABLE,
            'DbObjectType.TABLE "SCHEMA"."NAME"',
            True,
        ),
        (
            "schema",
            "name",
            DbObjectType.TABLE,
            'DbObjectType.TABLE "SCHEMA".NAME',
            True,
        ),
        (
            '"schema"',
            '"name"',
            DbObjectType.TABLE,
            "DbObjectType.TABLE SCHEMA.NAME",
            True,
        ),
        ("schema", "name", DbObjectType.VIEW, "DbObjectType.TABLE SCHEMA.NAME", False),
        ("schema", "name", DbObjectType.TABLE, "DbObjectType.VIEW SCHEMA.NAME", False),
        ("schema", "name", DbObjectType.TABLE, "DbObjectType.VIEW WRONG.NAME", False),
        ("schema", "name", DbObjectType.TABLE, "DbObjectType.VIEW SCHEMA.WRONG", False),
    ],
)
def test_compare_id(
    test_object_schema, test_object_name, test_object_type, compare_object_id, expected
):
    obj = DummyDatabaseObject(test_object_schema, test_object_name, test_object_type)
    assert obj.compare_id(compare_object_id) == expected
