import aceaccount.core.model_account_object as mao
import pytest
from aceaccount.core.model_account_object_sql_entities import AccountObjectType


def test_AccountObject_not_instanietable():
    with pytest.raises(TypeError):
        mao.AccountObject(
            "mystorageintegration", AccountObjectType.STORAGEINTEGRATION
        )  # pylint: disable=abstract-class-instantiated


class DummyAccountObject(mao.AccountObject):
    def __str__(self):
        return f"DummyAccountObject: {self.id}"

    def __repr__(self):
        return f"DummyAccountObject: {self.id}"


def test_properties():
    obj = DummyAccountObject( "my_name", AccountObjectType.STORAGEINTEGRATION)
    assert obj.name == "MY_NAME"
    assert obj.object_type == AccountObjectType.STORAGEINTEGRATION
    assert obj.id == f"{str(AccountObjectType.STORAGEINTEGRATION)} MY_NAME"


def test_account_object_type_error():
    with pytest.raises(TypeError):
        __ = DummyAccountObject("my_name", "AccountObjectType.STORAGEINTEGRATION")


@pytest.mark.parametrize(
    "test_object_name, compare_object_name, expected",
    [
        ("name", "name", True),
        ("name", "wrong", False),
        ('"name"', '"wrong"', False),
        ('"name"', '"name"', True),
        ("name", '"name"', True),
        ("name", 'name', True),
    ],
)
def test_compare_full_name(
    test_object_name, compare_object_name, expected
):
    obj = DummyAccountObject(test_object_name, AccountObjectType.STORAGEINTEGRATION)
    assert obj.compare_full_name(compare_object_name) == expected


@pytest.mark.parametrize(
    "test_object_name, test_object_type, compare_object_id, expected",
    [
        ("name", AccountObjectType.STORAGEINTEGRATION, "AccountObjectType.STORAGEINTEGRATION NAME", True),
        ("name", AccountObjectType.STORAGEINTEGRATION, "AccountObjectType.STORAGEINTEGRATION name", False),
        (
            "name",
            AccountObjectType.STORAGEINTEGRATION,
            'AccountObjectType.STORAGEINTEGRATION "NAME"',
            True,
        ),
        (
            "name",
            AccountObjectType.STORAGEINTEGRATION,
            'AccountObjectType.STORAGEINTEGRATION NAME',
            True,
        ),
        (
            '"name"',
            AccountObjectType.STORAGEINTEGRATION,
            "AccountObjectType.STORAGEINTEGRATION NAME",
            True,
        ),
        ("name", AccountObjectType.WAREHOUSE, "AccountObjectType.STORAGEINTEGRATION NAME", False),
        ("name", AccountObjectType.STORAGEINTEGRATION, "AccountObjectType.WAREHOUSE NAME", False),
        ("name", AccountObjectType.STORAGEINTEGRATION, "AccountObjectType.WAREHOUSE WRONG", False),
    ],
)
def test_compare_id(
    test_object_name, test_object_type, compare_object_id, expected
):
    obj = DummyAccountObject(test_object_name, test_object_type)
    assert obj.compare_id(compare_object_id) == expected
