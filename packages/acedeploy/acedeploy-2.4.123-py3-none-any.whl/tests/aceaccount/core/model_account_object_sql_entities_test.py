import aceaccount.core.model_account_object_sql_entities as maose
import pytest

# region maose.AccountObjectType


@pytest.mark.parametrize(
    "_input, _output",
    [
        (maose.AccountObjectType.STORAGEINTEGRATION, "INTEGRATION"),
        (maose.AccountObjectType.WAREHOUSE, "WAREHOUSE"),
        (maose.AccountObjectType.EXTERNALVOLUME, "EXTERNAL VOLUME"),
    ],
)
def test_get_object_domain_from_object_type_success(_input, _output):
    parameter = _input
    result = maose.AccountObjectType.get_object_domain_from_object_type(parameter)
    assert result == _output

# endregion maose.AccountObjectType