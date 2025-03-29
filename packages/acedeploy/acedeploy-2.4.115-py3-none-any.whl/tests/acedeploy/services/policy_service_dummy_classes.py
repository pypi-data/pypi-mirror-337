import pytest
from acedeploy.core.model_instance_objects import ColumnInstance
class DummyColumn(ColumnInstance):
    """
    Helper class to test without having to provide all arguments
    """

    def __init__(
        self,
        object_schema,
        object_name,
        column_name,
        ordinal_position,
        comment=None,
        column_default=None,
        is_nullable=None,
        data_type=None,
        numeric_precision=None,
        numeric_scale=None,
        character_maximum_length=None,
        character_octet_length=None,
        collation_name=None,
    ):
        self.object_schema = object_schema
        self.object_name = object_name
        self.column_name = column_name
        self.ordinal_position = ordinal_position
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
