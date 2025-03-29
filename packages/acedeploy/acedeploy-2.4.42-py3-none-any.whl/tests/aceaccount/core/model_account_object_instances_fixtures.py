import pytest
import datetime


@pytest.fixture
def metadata_storage_integration():
    return {
        "name": "my_sti",
        "type": "EXTERNAL_STAGE",
        "category": "STORAGE",
        "enabled": "true",
        "comment": "dummy comment",
        "storage_provider": "AZURE",
        "storage_allowed_locations": [
            "azure://account.blob.core.windows.net/container/path",
            "azure://account.blob.core.windows.net/container/path2",
        ],
        "storage_blocked_locations": [
            "azure://account.blob.core.windows.net/container/path3"
        ],
        "azure_tenant_id": "a123b4c5-1234-123a-a12b-1a23b4561234",
        "azure_consent_url": "https://login.microsoftonline.com/a123b4c5-1234-123a-a12b-1a23b4561234/oauth2/authorize?client_id=b68412c3-4d33-468b-8063-3e5ecde9ba26&response_type=code",
        "azure_multi_tenant_app_name": "abc87rsnowflakepacint_1687181291234",
        "grants": {"usage": ["R-TEST-1", "R_ACCOUNT_OBJECTS_TEST"]},
        "OBJECT_NAME": "MY_STI",
    }


@pytest.fixture
def metadata_warehouse():
    return {
        "name": "my_warehouse",
        "state": "STARTED",
        "type": "STANDARD",
        "size": "X-Small",
        "min_cluster_count": 1,
        "max_cluster_count": 1,
        "started_clusters": 1,
        "running": 0,
        "queued": 0,
        "is_default": "N",
        "is_current": "Y",
        "auto_suspend": 600,
        "auto_resume": "true",
        "available": " 100",
        "provisioning": "0",
        "quiescing": "0",
        "other": "0",
        "owner": "R_ACCOUNT_OBJECT_PIPELINE",
        "comment": "",
        "enable_query_acceleration": "false",
        "query_acceleration_max_scale_factor": 8,
        "resource_monitor": "null",
        "actives": 1,
        "pendings": 0,
        "failed": 0,
        "suspended": 0,
        "uuid": "28459528",
        "scaling_policy": "STANDARD",
        "max_concurrency_level": 8,
        "statement_queued_timeout_in_seconds": 0,
        "statement_timeout_in_seconds": 172800,
        "grants": {"usage": ["R_ACCOUNT_OBJECT_PIPELINE"]},
        "tags": {
            "tags_database.tags_schema.tag_warehouse_account": "tag_value_warehouse_account",
            "tags_database.tags_schema.tag_warehouse_application": "tag_value_warehouse_application",
            "tags_database.tags_schema.tag_warehouse_billing_type": "tag_value_warehouse_billing_type",
            "tags_database.tags_schema.tag_warehouse_branch": "tag_value_warehouse_branch",
            "tags_database.tags_schema.tag_warehouse_environment": "tag_value_warehouse_environment",
            "tags_database.tags_schema.tag_warehouse_purpose": "tag_value_warehouse_purpose",
            "tags_database.tags_schema.tag_warehouse_warehouse_department": "tag_value_warehouse_warehouse_department",
        },
        "OBJECT_NAME": "MY_WAREHOUSE",
    }


@pytest.fixture
def metadata_externalvolume():
    return {
        "name": "my_externalvolume",
        "allow_writes": "true",
        "comment": None,
        "storage_locations": {
            "my-s3-us-west-2": {
                "storage_provider": "S3",
                "storage_base_url": "s3://MY_EXAMPLE_BUCKET/",
                "storage_aws_role_arn": "arn:aws:iam::123456789012:role/myrole",
                "storage_aws_external_id": "LV03266_SFCRole=2_1xSGPMuxVkE03TzzaajsZGThMHM=",
                "encryption": {
                    "type": "AWS_SSE_KMS",
                    "kms_key_id": "1234abcd-12ab-34cd-56ef-1234567890ab",
                },
            }
        },
        "active": "",
    }
