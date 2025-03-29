import json
from typing import Dict, List

from acedeploy.core.model_instance_objects import (
    ColumnInstance,
    InstanceConstraintForeignKey,
    InstanceConstraintPrimaryKey,
    InstanceConstraintUniqueKey,
    InstanceTable,
    RowAccessPolicyReference,
    MaskingPolicyReference,
)
from acedeploy.core.model_sql_entities import PolicyType
from aceservices.snowflake_service import SnowClient


class DummySnowClient(SnowClient):
    def __init__(self, query_response: List[Dict]):
        self.query_response = query_response

    def execute_query(self, *__, **___):
        return self.query_response

    def __del__(self):
        pass


class DummyColumn(ColumnInstance):
    """
    Helper class to test without having to provide all arguments
    """

    def __init__(
        self,
        column_name,
        column_default=None,
        comment=None,
        is_nullable=None,
        data_type=None,
        numeric_precision=None,
        numeric_scale=None,
        character_maximum_length=None,
        character_octet_length=None,
        collation_name=None,
    ):
        self.object_schema = None
        self.object_name = None
        self.column_name = column_name
        self.ordinal_position = None
        self.column_default = column_default
        self.is_nullable = is_nullable
        self.data_type = data_type
        self.character_maximum_length = character_maximum_length
        self.character_octet_length = character_octet_length
        self.numeric_precision = numeric_precision
        self.numeric_precision_radix = None
        self.numeric_scale = numeric_scale
        self.datetime_precision = None
        self.interval_type = None
        self.interval_precision = None
        self.character_set_catalog = None
        self.character_set_schema = None
        self.character_set_name = None
        self.collation_catalog = None
        self.collation_schema = None
        self.collation_name = collation_name
        self.domain_catalog = None
        self.domain_schema = None
        self.domain_name = None
        self.udt_catalog = None
        self.udt_schema = None
        self.udt_name = None
        self.scope_catalog = None
        self.scope_schema = None
        self.scope_name = None
        self.maximum_cardinality = None
        self.dtd_identifier = None
        self.is_self_referencing = None
        self.is_identity = None
        self.identity_generation = None
        self.identity_start = None
        self.identity_increment = None
        self.identity_maximum = None
        self.identity_minimum = None
        self.identity_cycle = None
        self.tags = None
        self.comment = comment


class DummyInstanceTable(InstanceTable):
    def __init__(
        self,
        table_columns=List[ColumnInstance],
        clustering_key: str = None,
        comment: str = None,
        retention_time: int = 90,
        schema_retention_time: int = 90,
        constraints_foreign_key: List[InstanceConstraintForeignKey] = [],
        constraints_primary_key: List[InstanceConstraintPrimaryKey] = [],
        constraints_unique_key: List[InstanceConstraintUniqueKey] = [],
        tags: dict = {},
        row_access_policy_references: List[RowAccessPolicyReference] = [],
        masking_policy_references: List[RowAccessPolicyReference] = [],
    ):
        self.table_columns = table_columns
        self.clustering_key = clustering_key
        self.retention_time = retention_time
        self.schema_retention_time = schema_retention_time
        self.comment = comment
        self.constraints_foreign_key = constraints_foreign_key
        self.constraints_primary_key = constraints_primary_key
        self.constraints_unique_key = constraints_unique_key
        self.tags = tags
        self.row_access_policy_references = row_access_policy_references
        self.masking_policy_references = masking_policy_references


class DummyRowAccessPolicyReference(RowAccessPolicyReference):
    def __init__(
        self,
        policy_db = "mydb",
        policy_schema = "myschema",
        policy_name = "myrap",
        policy_kind = "ROW_ACCESS_POLICY",
        ref_database_name = "my_db",
        ref_schema_name = "my_schema",
        ref_entity_name = "my_table",
        ref_entity_domain = "TABLE",
        ref_column_name = "",
        ref_arg_column_names = '["A", "B"]',
        tag_database = "",
        tag_schema = "",
        tag_name = "",
        policy_status = "",
    ):
        self.policy_type = PolicyType.ROWACCESS
        self.policy_db = policy_db
        self.policy_schema = policy_schema
        self.policy_name = policy_name
        self.policy_kind = policy_kind
        self.ref_database_name = ref_database_name
        self.ref_schema_name = ref_schema_name
        self.ref_entity_name = ref_entity_name
        self.ref_entity_domain = ref_entity_domain
        self.ref_column_name = ref_column_name
        self.ref_arg_column_names = ref_arg_column_names
        self.ref_arg_column_names_dict = json.loads(ref_arg_column_names)
        self.tag_database = tag_database
        self.tag_schema = tag_schema
        self.tag_name = tag_name
        self.policy_status = policy_status


class DummyMaskingPolicyReference(MaskingPolicyReference):
    def __init__(
        self,
        policy_db = "mydb",
        policy_schema = "myschema",
        policy_name = "mymp",
        policy_kind = "MASKING_POLICY",
        ref_database_name = "my_db",
        ref_schema_name = "my_schema",
        ref_entity_name = "my_table",
        ref_entity_domain = "TABLE",
        ref_column_name = "col1",
        ref_arg_column_names = "[]",
        tag_database = "",
        tag_schema = "",
        tag_name = "",
        policy_status = "",
    ):
        self.policy_type = PolicyType.ROWACCESS
        self.policy_db = policy_db
        self.policy_schema = policy_schema
        self.policy_name = policy_name
        self.policy_kind = policy_kind
        self.ref_database_name = ref_database_name
        self.ref_schema_name = ref_schema_name
        self.ref_entity_name = ref_entity_name
        self.ref_entity_domain = ref_entity_domain
        self.ref_column_name = ref_column_name
        self.ref_arg_column_names = ref_arg_column_names
        self.ref_arg_column_names_dict = json.loads(ref_arg_column_names)
        self.tag_database = tag_database
        self.tag_schema = tag_schema
        self.tag_name = tag_name
        self.policy_status = policy_status
