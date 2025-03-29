import pytest
import inspect
import aceaccount.core.model_account_object_action_entities as oae
from aceaccount.core.model_account_object_instances import (
    AccountObjectInstance,
    StorageIntegrationInstance,
    WarehouseInstance,
    ExternalVolumeInstance,
)
from aceaccount.core.model_account_object_sql_entities import (
    AccountObjectActionType,
)
from aceservices.snowflake_service import SnowClientConfig


# region AccountObjectAction tests

# endregion AccountObjectAction tests


# region StorageIntegrationAction tests
@pytest.mark.parametrize(
    "desired_instance, expected",
    [
        (  # create STI without blocked_locations, with grants
            StorageIntegrationInstance(
                {
                    "name": "STI_TEST",
                    "type": "EXTERNAL_STAGE",
                    "enabled": True,
                    "storage_provider": "AZURE",
                    "azure_tenant_id": "a123b4c5-1234-123a-a12b-1a23b45678c9",
                    "storage_allowed_locations": [
                        "azure://account.blob.core.windows.net/container/path",
                        "azure://account.blob.core.windows.net/container/path2",
                    ],
                    "storage_blocked_locations": [],
                    "comment": "test integration",
                    "grants": {"usage": ["R_TEST_1", "R_TEST_2"]},
                }
            ),
            """
            CREATE STORAGE INTEGRATION "STI_TEST"
            TYPE = EXTERNAL_STAGE
            STORAGE_PROVIDER = AZURE
            AZURE_TENANT_ID = 'a123b4c5-1234-123a-a12b-1a23b45678c9'
            ENABLED = True
            STORAGE_ALLOWED_LOCATIONS = ('azure://account.blob.core.windows.net/container/path', 'azure://account.blob.core.windows.net/container/path2')
            COMMENT = 'test integration';
            GRANT USAGE ON INTEGRATION STI_TEST TO ROLE "R_TEST_1";
            GRANT USAGE ON INTEGRATION STI_TEST TO ROLE "R_TEST_2";""",
        ),
        (  # create STI with blocked_locations, without grants
            StorageIntegrationInstance(
                {
                    "name": "STI_TEST",
                    "type": "EXTERNAL_STAGE",
                    "enabled": True,
                    "storage_provider": "AZURE",
                    "azure_tenant_id": "a123b4c5-1234-123a-a12b-1a23b45678c9",
                    "storage_allowed_locations": [
                        "azure://account.blob.core.windows.net/container/path",
                        "azure://account.blob.core.windows.net/container/path2",
                    ],
                    "storage_blocked_locations": [
                        "azure://account.blob.core.windows.net/container/path3",
                        "azure://account.blob.core.windows.net/container/path4",
                    ],
                    "comment": "test integration",
                }
            ),
            """
            CREATE STORAGE INTEGRATION "STI_TEST"
            TYPE = EXTERNAL_STAGE
            STORAGE_PROVIDER = AZURE
            AZURE_TENANT_ID = 'a123b4c5-1234-123a-a12b-1a23b45678c9'
            ENABLED = True
            STORAGE_ALLOWED_LOCATIONS = ('azure://account.blob.core.windows.net/container/path', 'azure://account.blob.core.windows.net/container/path2')
            COMMENT = 'test integration'
            STORAGE_BLOCKED_LOCATIONS = ('azure://account.blob.core.windows.net/container/path3', 'azure://account.blob.core.windows.net/container/path4');
            """,
        ),
    ],
)
def test_StorageIntegrationAction_generate_create_statement(
    desired_instance: StorageIntegrationInstance,
    expected: str,
):
    result = oae.StorageIntegrationAction._generate_create_statement(desired_instance)
    assert result == inspect.cleandoc(expected)


@pytest.mark.parametrize(
    "current_instance, desired_instance, expected",
    [
        (  # alter STI
            StorageIntegrationInstance(
                {
                    "name": "STI_TEST",
                    "type": "EXTERNAL_STAGE",
                    "enabled": True,
                    "storage_provider": "AZURE",
                    "azure_tenant_id": "a123b4c5-1234-123a-a12b-1a23b45678c9",
                    "storage_allowed_locations": [
                        "azure://account.blob.core.windows.net/container/path",
                        "azure://account.blob.core.windows.net/container/path2",
                    ],
                    "storage_blocked_locations": [],
                    "comment": "test integration",
                    "grants": {"usage": ["R_TEST_1", "R_TEST_2"]},
                }
            ),
            StorageIntegrationInstance(
                {
                    "name": "STI_TEST",
                    "type": "EXTERNAL_STAGE",
                    "enabled": False,
                    "storage_provider": "AZURE",
                    "azure_tenant_id": "1111111-1234-123a-a12b-1a23b45678c9",
                    "storage_allowed_locations": [
                        "azure://account.blob.core.windows.net/container/path2",
                        "azure://account.blob.core.windows.net/container/path3",
                    ],
                    "storage_blocked_locations": [
                        "azure://account.blob.core.windows.net/container/path"
                    ],
                    "comment": "test integration - test change to comment",
                    "grants": {"usage": ["R_TEST_1", "R_TEST_2"]},
                }
            ),
            "ALTER STORAGE INTEGRATION STI_TEST SET ENABLED = False;\nALTER STORAGE INTEGRATION STI_TEST SET COMMENT = 'test integration - test change to comment';\nALTER STORAGE INTEGRATION STI_TEST SET STORAGE_ALLOWED_LOCATIONS = ('azure://account.blob.core.windows.net/container/path2', 'azure://account.blob.core.windows.net/container/path3');\nALTER STORAGE INTEGRATION STI_TEST SET STORAGE_BLOCKED_LOCATIONS = ('azure://account.blob.core.windows.net/container/path');\nALTER STORAGE INTEGRATION STI_TEST SET AZURE_TENANT_ID = '1111111-1234-123a-a12b-1a23b45678c9';",
        )
    ],
)
def test_StorageIntegrationAction_generate_alter_statement(
    current_instance: StorageIntegrationInstance,
    desired_instance: StorageIntegrationInstance,
    expected: str,
):
    result = oae.StorageIntegrationAction._generate_alter_statement(
        current_instance, desired_instance
    )
    assert result == inspect.cleandoc(expected)


# endregion StorageIntegrationAction tests

# region WarehouseAction tests


@pytest.mark.parametrize(
    "desired_instance, snow_client_config, expected",
    [
        (  # create Warehouse, with grants
            WarehouseInstance(
                {
                    "name": "WH_TEST_4",
                    "type": "STANDARD",
                    "size": "X-Small",
                    "max_cluster_count": 1,
                    "min_cluster_count": 1,
                    "scaling_policy": "STANDARD",
                    "auto_suspend": 600,
                    "auto_resume": True,
                    "resource_monitor": "null",
                    "comment": "warehouse test comment",
                    "grants": {"usage": ["R_ACCOUNT_OBJECT_PIPELINE"]},
                    "tags": {
                        "tags_database.tags_schema.tag_warehouse_account": "test_account_1",
                        "tags_database.tags_schema.tag_warehouse_application": "Tag_Value_2",
                        "tags_database.tags_schema.tag_warehouse_billing_type": "Tag_Value_3",
                        "tags_database.tags_schema.tag_warehouse_branch": "Tag_Value_4",
                        "tags_database.tags_schema.tag_warehouse_environment": "Tag_Value_Test",
                        "tags_database.tags_schema.tag_warehouse_purpose": "Tag_Value_6",
                        "tags_database.tags_schema.tag_warehouse_warehouse_department": "Tag_Value_7",
                    },
                    "enable_query_acceleration": False,
                    "query_acceleration_max_scale_factor": 8,
                    "max_concurrency_level": 8,
                    "statement_queued_timeout_in_seconds": 0,
                    "statement_timeout_in_seconds": 172800,
                }
            ),
            SnowClientConfig(
                account="dummy_account",
                user="dummy_user",
                password="dummy_password",
                warehouse="WH_ACEDEPLOY",
            ),
            """
            CREATE WAREHOUSE "WH_TEST_4"
            INITIALLY_SUSPENDED = TRUE
            WAREHOUSE_TYPE = \'STANDARD\'
            WAREHOUSE_SIZE = \'X-SMALL\'
            MAX_CLUSTER_COUNT = 1
            MIN_CLUSTER_COUNT = 1
            SCALING_POLICY = \'STANDARD\'
            AUTO_SUSPEND = 600
            AUTO_RESUME = True
            COMMENT = \'warehouse test comment\'
            QUERY_ACCELERATION_MAX_SCALE_FACTOR = 8
            MAX_CONCURRENCY_LEVEL = 8
            STATEMENT_TIMEOUT_IN_SECONDS = 172800
            WITH TAG (tags_database.tags_schema.tag_warehouse_account = \'test_account_1\', tags_database.tags_schema.tag_warehouse_application = \'Tag_Value_2\', tags_database.tags_schema.tag_warehouse_billing_type = \'Tag_Value_3\', tags_database.tags_schema.tag_warehouse_branch = \'Tag_Value_4\', tags_database.tags_schema.tag_warehouse_environment = \'Tag_Value_Test\', tags_database.tags_schema.tag_warehouse_purpose = \'Tag_Value_6\', tags_database.tags_schema.tag_warehouse_warehouse_department = \'Tag_Value_7\');
            USE WAREHOUSE WH_ACEDEPLOY;
            GRANT USAGE ON WAREHOUSE WH_TEST_4 TO ROLE "R_ACCOUNT_OBJECT_PIPELINE";""",
        ),
    ],
)
def test_WarehouseAction_generate_create_statement(
    desired_instance: WarehouseInstance,
    snow_client_config: SnowClientConfig,
    expected: str,
):
    result = oae.WarehouseAction._generate_create_statement(
        desired_instance, snow_client_config
    )
    assert result == inspect.cleandoc(expected)


# endregion WarehouseAction tests
