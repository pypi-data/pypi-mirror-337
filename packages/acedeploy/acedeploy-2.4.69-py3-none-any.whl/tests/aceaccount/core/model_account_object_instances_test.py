import aceaccount.core.model_account_object_instances as maoi
import pytest

from model_account_object_instances_fixtures import (
    metadata_storage_integration,
    metadata_warehouse,
    metadata_externalvolume,
)

@pytest.mark.parametrize(
    "object_type, metadata_query_result, expected_id, expected_full_name, expected_repr",
    [
        (
            maoi.StorageIntegrationInstance,
            pytest.lazy_fixture("metadata_storage_integration"),
            "AccountObjectType.STORAGEINTEGRATION MY_STI",
            "MY_STI",
            "StorageIntegrationInstance: AccountObjectType.STORAGEINTEGRATION MY_STI",
        ),
        (
            maoi.WarehouseInstance,
            pytest.lazy_fixture("metadata_warehouse"),
            "AccountObjectType.WAREHOUSE MY_WAREHOUSE",
            "MY_WAREHOUSE",
            "WarehouseInstance: AccountObjectType.WAREHOUSE MY_WAREHOUSE",
        ),
        (
            maoi.ExternalVolumeInstance,
            pytest.lazy_fixture("metadata_externalvolume"),
            "AccountObjectType.EXTERNALVOLUME MY_EXTERNALVOLUME",
            "MY_EXTERNALVOLUME",
            "ExternalVolumeInstance: AccountObjectType.EXTERNALVOLUME MY_EXTERNALVOLUME",
        ),
    ],
)
def test_AccountObjectInstance_properties(
    object_type, metadata_query_result, expected_id, expected_full_name, expected_repr
):
    obj = object_type(metadata_query_result)
    assert obj.id == expected_id
    assert obj.full_name == expected_full_name
    assert repr(obj) == expected_repr
    assert str(obj) == expected_repr