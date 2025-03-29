import aceaccount.core.model_account_object_statement as maos
import pytest
from aceaccount.core.model_account_object_sql_entities import AccountObjectType

# region maos.AccountObjectStatement

def test_init_AccountObjectStatement():
    result = maos.AccountObjectStatement(
        name="MY_ACCOUNT_OBJECT",
        statement="ALTER STORAGE INTEGRATION MY_ACCOUNT_OBJECT SET COMMENT = 'Testcomment';",
        object_type=AccountObjectType.STORAGEINTEGRATION,
    )
    assert result.name == "MY_ACCOUNT_OBJECT"
    assert result.statement == "ALTER STORAGE INTEGRATION MY_ACCOUNT_OBJECT SET COMMENT = 'Testcomment';"
    assert result.id == "AccountObjectType.STORAGEINTEGRATION MY_ACCOUNT_OBJECT"
    assert repr(result) == "AccountObjectStatement: AccountObjectType.STORAGEINTEGRATION MY_ACCOUNT_OBJECT"
    assert str(result) == "AccountObjectStatement: AccountObjectType.STORAGEINTEGRATION MY_ACCOUNT_OBJECT"


def test_equality_AccountObjectStatement():
    s1 = maos.AccountObjectStatement(
        name="MY_ACCOUNT_OBJECT",
        statement="ALTER STORAGE INTEGRATION MY_ACCOUNT_OBJECT SET COMMENT = 'Testcomment';",
        object_type=AccountObjectType.STORAGEINTEGRATION,
    )
    s2 = maos.AccountObjectStatement(
        name="MY_ACCOUNT_OBJECT",
        statement="ALTER STORAGE INTEGRATION MY_ACCOUNT_OBJECT SET COMMENT = 'Testcomment';",
        object_type=AccountObjectType.STORAGEINTEGRATION,
    )
    assert s1 == s2


@pytest.mark.parametrize(
    "_input1, _input2",
    [
        (
            maos.AccountObjectStatement(
                name="MY_ACCOUNT_OBJECT1",
                statement="ALTER STORAGE INTEGRATION MY_ACCOUNT_OBJECT SET COMMENT = 'Testcomment';",
                object_type=AccountObjectType.STORAGEINTEGRATION,
            ),
            maos.AccountObjectStatement(
                name="MY_ACCOUNT_OBJECT2",
                statement="ALTER STORAGE INTEGRATION MY_ACCOUNT_OBJECT SET COMMENT = 'Testcomment';",
                object_type=AccountObjectType.STORAGEINTEGRATION,
            ),
        ),
        (
            maos.AccountObjectStatement(
                name="MY_ACCOUNT_OBJECT1",
                statement="ALTER STORAGE INTEGRATION MY_ACCOUNT_OBJECT SET COMMENT = 'Testcomment';",
                object_type=AccountObjectType.STORAGEINTEGRATION,
            ),
            maos.AccountObjectStatement(
                name="MY_ACCOUNT_OBJECT1",
                statement="ALTER STORAGE INTEGRATION MY_ACCOUNT_OBJECT SET COMMENT = 'Testcomment1';",
                object_type=AccountObjectType.STORAGEINTEGRATION,
            ),
        ),
        (
            maos.AccountObjectStatement(
                name="MY_ACCOUNT_OBJECT1",
                statement="ALTER STORAGE INTEGRATION MY_ACCOUNT_OBJECT SET COMMENT = 'Testcomment';",
                object_type=AccountObjectType.STORAGEINTEGRATION,
            ),
            maos.AccountObjectStatement(
                name="MY_ACCOUNT_OBJECT1",
                statement="ALTER STORAGE INTEGRATION MY_ACCOUNT_OBJECT SET COMMENT = 'Testcomment';",
                object_type=AccountObjectType.WAREHOUSE,
            ),
        ),
    ],
)
def test_inequality_AccountObjectStatement(_input1, _input2):
    assert not (_input1 == _input2)

# endregion maos.AccountObjectStatement