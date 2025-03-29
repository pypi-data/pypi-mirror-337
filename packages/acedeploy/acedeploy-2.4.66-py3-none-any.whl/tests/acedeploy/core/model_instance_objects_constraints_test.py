import acedeploy.core.model_instance_objects as mio
import pytest

# region columns


def test_ConstraintColumn_init():
    key_sequence = 1
    column_name = "my_column"
    result = mio.ConstraintColumn(key_sequence, column_name)
    assert result.key_sequence == key_sequence
    assert result.column_name == column_name


def test_ConstraintColumn_eq():
    key_sequence_1 = 1
    column_name_1 = "my_column"
    col_1 = mio.ConstraintColumn(key_sequence_1, column_name_1)
    key_sequence_2 = 1
    column_name_2 = "my_column"
    col_2 = mio.ConstraintColumn(key_sequence_2, column_name_2)
    assert (col_1 == col_2) == True


def test_ConstraintColumn_not_eq():
    key_sequence_1 = 1
    column_name_1 = "my_column"
    col_1 = mio.ConstraintColumn(key_sequence_1, column_name_1)
    key_sequence_2 = 1
    column_name_2 = "my_other_column"
    col_2 = mio.ConstraintColumn(key_sequence_2, column_name_2)
    assert (col_1 == col_2) == False


def test_ConstraintColumnForeignKey_init():
    key_sequence = 1
    column_name = "my_column"
    pk_column_name = "my_pk_col"
    result = mio.ConstraintColumnForeignKey(key_sequence, column_name, pk_column_name)
    assert result.key_sequence == key_sequence
    assert result.column_name == column_name
    assert result.pk_column_name == pk_column_name


def test_ConstraintColumnForeignKey_eq():
    key_sequence_1 = 1
    column_name_1 = "my_column"
    pk_column_name_1 = "my_pk_col"
    col_1 = mio.ConstraintColumnForeignKey(
        key_sequence_1, column_name_1, pk_column_name_1
    )
    key_sequence_2 = 1
    column_name_2 = "my_column"
    pk_column_name_2 = "my_pk_col"
    col_2 = mio.ConstraintColumnForeignKey(
        key_sequence_2, column_name_2, pk_column_name_2
    )
    assert (col_1 == col_2) == True


def test_ConstraintColumnForeignKey_not_eq():
    key_sequence_1 = 1
    column_name_1 = "my_column"
    pk_column_name_1 = "my_pk_col"
    col_1 = mio.ConstraintColumnForeignKey(
        key_sequence_1, column_name_1, pk_column_name_1
    )
    key_sequence_2 = 1
    column_name_2 = "my_other_column"
    pk_column_name_2 = "my_pk_col"
    col_2 = mio.ConstraintColumnForeignKey(
        key_sequence_2, column_name_2, pk_column_name_2
    )
    assert (col_1 == col_2) == False


# endregion columns

# region constraints


@pytest.mark.parametrize(
    "input, expected",
    [
        ("SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff9959", True),
        ("SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff99591", False),
        ("SYS_CONSTRAINT_68a8226c-e9e7-4de6-87e6-9467f1ff9959_new", False),
        ("SYS_CONSTRAINT_68a8226c-xxe7-4de6-87e6-9467f1ff9959", False),
        ("MY_CONSTRAINT", False),
    ],
)
def test_is_system_assigned_name(input, expected):
    result = mio.InstanceConstraint._is_system_assigned_name(input)
    assert result == expected


def test_InstanceConstraintPrimaryKey_init():
    metadata = [
        {
            "schema_name": "MY_SCHEMA",
            "table_name": "MY_TABLE",
            "constraint_name": "MY_CONSTRAINT",
            "comment": None,
            "key_sequence": 1,
            "column_name": "COL_1",
        },
        {
            "schema_name": "MY_SCHEMA",
            "table_name": "MY_TABLE",
            "constraint_name": "MY_CONSTRAINT",
            "comment": None,
            "key_sequence": 2,
            "column_name": "COL_2",
        },
    ]
    result = mio.InstanceConstraintPrimaryKey(metadata)
    assert result.schema_name == "MY_SCHEMA"
    assert result.table_name == "MY_TABLE"
    assert result.constraint_name == "MY_CONSTRAINT"
    assert result.comment == None
    assert result.columns == [
        mio.ConstraintColumn(1, "COL_1"),
        mio.ConstraintColumn(2, "COL_2"),
    ]


def test_InstanceConstraintPrimaryKey_eq():
    metadata1 = [
        {
            "schema_name": "MY_SCHEMA",
            "table_name": "MY_TABLE",
            "constraint_name": "MY_CONSTRAINT",
            "comment": None,
            "key_sequence": 1,
            "column_name": "COL_1",
        }
    ]
    result1 = mio.InstanceConstraintPrimaryKey(metadata1)
    metadata2 = [
        {
            "schema_name": "MY_SCHEMA",
            "table_name": "MY_TABLE",
            "constraint_name": "MY_CONSTRAINT",
            "comment": None,
            "key_sequence": 1,
            "column_name": "COL_1",
        }
    ]
    result2 = mio.InstanceConstraintPrimaryKey(metadata2)
    assert (result1 == result2) == True


def test_InstanceConstraintPrimaryKey_not_eq():
    metadata1 = [
        {
            "schema_name": "MY_SCHEMA",
            "table_name": "MY_TABLE",
            "constraint_name": "MY_CONSTRAINT",
            "comment": None,
            "key_sequence": 1,
            "column_name": "COL_1",
        }
    ]
    result1 = mio.InstanceConstraintPrimaryKey(metadata1)
    metadata2 = [
        {
            "schema_name": "MY_SCHEMA",
            "table_name": "MY_TABLE",
            "constraint_name": "MY_CONSTRAINT",
            "comment": None,
            "key_sequence": 1,
            "column_name": "COL_X",
        }
    ]
    result2 = mio.InstanceConstraintPrimaryKey(metadata2)
    assert (result1 == result2) == False


def test_InstanceConstraintUniqueKey_init():
    metadata = [
        {
            "schema_name": "MY_SCHEMA",
            "table_name": "MY_TABLE",
            "constraint_name": "MY_CONSTRAINT",
            "comment": None,
            "key_sequence": 1,
            "column_name": "COL_1",
        },
        {
            "schema_name": "MY_SCHEMA",
            "table_name": "MY_TABLE",
            "constraint_name": "MY_CONSTRAINT",
            "comment": None,
            "key_sequence": 2,
            "column_name": "COL_2",
        },
    ]
    result = mio.InstanceConstraintUniqueKey(metadata)
    assert result.schema_name == "MY_SCHEMA"
    assert result.table_name == "MY_TABLE"
    assert result.constraint_name == "MY_CONSTRAINT"
    assert result.comment == None
    assert result.columns == [
        mio.ConstraintColumn(1, "COL_1"),
        mio.ConstraintColumn(2, "COL_2"),
    ]


def test_InstanceConstraintUniqueKey_eq():
    metadata1 = [
        {
            "schema_name": "MY_SCHEMA",
            "table_name": "MY_TABLE",
            "constraint_name": "MY_CONSTRAINT",
            "comment": None,
            "key_sequence": 1,
            "column_name": "COL_1",
        }
    ]
    result1 = mio.InstanceConstraintUniqueKey(metadata1)
    metadata2 = [
        {
            "schema_name": "MY_SCHEMA",
            "table_name": "MY_TABLE",
            "constraint_name": "MY_CONSTRAINT",
            "comment": None,
            "key_sequence": 1,
            "column_name": "COL_1",
        }
    ]
    result2 = mio.InstanceConstraintUniqueKey(metadata2)
    assert (result1 == result2) == True


def test_InstanceConstraintUniqueKey_not_eq():
    metadata1 = [
        {
            "schema_name": "MY_SCHEMA",
            "table_name": "MY_TABLE",
            "constraint_name": "MY_CONSTRAINT",
            "comment": None,
            "key_sequence": 1,
            "column_name": "COL_1",
        }
    ]
    result1 = mio.InstanceConstraintUniqueKey(metadata1)
    metadata2 = [
        {
            "schema_name": "MY_SCHEMA",
            "table_name": "MY_TABLE",
            "constraint_name": "MY_CONSTRAINT",
            "comment": None,
            "key_sequence": 1,
            "column_name": "COL_X",
        }
    ]
    result2 = mio.InstanceConstraintUniqueKey(metadata2)
    assert (result1 == result2) == False


def test_InstanceConstraintForeignKey_init():
    metadata = [
        {
            "fk_schema_name": "MY_SCHEMA",
            "fk_table_name": "MY_TABLE",
            "fk_name": "MY_CONSTRAINT",
            "pk_schema_name": "MY_SCHEMA_2",
            "pk_table_name": "MY_TABLE_2",
            "pk_name": "MY_CONSTRAINT_2",
            "comment": None,
            "key_sequence": 1,
            "fk_column_name": "COL_1",
            "pk_column_name": "COL_A",
        },
        {
            "fk_schema_name": "MY_SCHEMA",
            "fk_table_name": "MY_TABLE",
            "fk_name": "MY_CONSTRAINT",
            "pk_schema_name": "MY_SCHEMA_2",
            "pk_table_name": "MY_TABLE_2",
            "pk_name": "MY_CONSTRAINT_2",
            "comment": None,
            "key_sequence": 2,
            "fk_column_name": "COL_2",
            "pk_column_name": "COL_B",
        },
    ]
    result = mio.InstanceConstraintForeignKey(metadata)
    assert result.schema_name == "MY_SCHEMA"
    assert result.fk_schema_name == "MY_SCHEMA"
    assert result.table_name == "MY_TABLE"
    assert result.fk_table_name == "MY_TABLE"
    assert result.constraint_name == "MY_CONSTRAINT"
    assert result.fk_name == "MY_CONSTRAINT"
    assert result.pk_schema_name == "MY_SCHEMA_2"
    assert result.pk_table_name == "MY_TABLE_2"
    assert result.pk_name == "MY_CONSTRAINT_2"
    assert result.comment == None
    assert result.columns == [
        mio.ConstraintColumnForeignKey(1, "COL_1", "COL_A"),
        mio.ConstraintColumnForeignKey(2, "COL_2", "COL_B"),
    ]


def test_InstanceConstraintForeignKey_eq():
    metadata1 = [
        {
            "fk_schema_name": "MY_SCHEMA",
            "fk_table_name": "MY_TABLE",
            "fk_name": "MY_CONSTRAINT",
            "pk_schema_name": "MY_SCHEMA_2",
            "pk_table_name": "MY_TABLE_2",
            "pk_name": "MY_CONSTRAINT_2",
            "comment": None,
            "key_sequence": 1,
            "fk_column_name": "COL_1",
            "pk_column_name": "COL_A",
        }
    ]
    result1 = mio.InstanceConstraintForeignKey(metadata1)
    metadata2 = [
        {
            "fk_schema_name": "MY_SCHEMA",
            "fk_table_name": "MY_TABLE",
            "fk_name": "MY_CONSTRAINT",
            "pk_schema_name": "MY_SCHEMA_2",
            "pk_table_name": "MY_TABLE_2",
            "pk_name": "MY_CONSTRAINT_2",
            "comment": None,
            "key_sequence": 1,
            "fk_column_name": "COL_1",
            "pk_column_name": "COL_A",
        }
    ]
    result2 = mio.InstanceConstraintForeignKey(metadata2)
    assert (result1 == result2) == True


def test_InstanceConstraintForeignKey_not_eq():
    metadata1 = [
        {
            "fk_schema_name": "MY_SCHEMA",
            "fk_table_name": "MY_TABLE",
            "fk_name": "MY_CONSTRAINT",
            "pk_schema_name": "MY_SCHEMA_2",
            "pk_table_name": "MY_TABLE_2",
            "pk_name": "MY_CONSTRAINT_2",
            "comment": None,
            "key_sequence": 1,
            "fk_column_name": "COL_1",
            "pk_column_name": "COL_A",
        }
    ]
    result1 = mio.InstanceConstraintForeignKey(metadata1)
    metadata2 = [
        {
            "fk_schema_name": "MY_SCHEMA",
            "fk_table_name": "MY_TABLE",
            "fk_name": "MY_CONSTRAINT",
            "pk_schema_name": "MY_SCHEMA_2",
            "pk_table_name": "MY_TABLE_2",
            "pk_name": "MY_CONSTRAINT_2",
            "comment": None,
            "key_sequence": 1,
            "fk_column_name": "COL_1",
            "pk_column_name": "COL_X",
        }
    ]
    result2 = mio.InstanceConstraintForeignKey(metadata2)
    assert (result1 == result2) == False


def test_InstanceConstraint_factory_multiple_foreign_keys():
    metadata = [
        {
            "created_on": "2022-04-22 05:44:36.834000-07:00",
            "pk_database_name": "TWZ_META",
            "pk_schema_name": "REP_DMA",
            "pk_table_name": "DM_D_BOOKING_CODES",
            "pk_column_name": "DWH_DIM_ID",
            "fk_database_name": "TWZ_META",
            "fk_schema_name": "REP_DMA",
            "fk_table_name": "DM_F_LOGISTIC_COST_FACTORS",
            "fk_column_name": "FK_BOC_ID",
            "key_sequence": 1,
            "update_rule": "NO ACTION",
            "delete_rule": "NO ACTION",
            "fk_name": "LOGCOSTF_FK_BOC_ID",
            "pk_name": "BOC_PK",
            "deferrability": "NOT DEFERRABLE",
            "rely": "false",
            "comment": None,
        },
        {
            "created_on": "2022-04-22 05:44:36.834000-07:00",
            "pk_database_name": "TWZ_META",
            "pk_schema_name": "REP_DMA",
            "pk_table_name": "DM_D_FIRMS",
            "pk_column_name": "DWH_DIM_ID",
            "fk_database_name": "TWZ_META",
            "fk_schema_name": "REP_DMA",
            "fk_table_name": "DM_F_LOGISTIC_COST_FACTORS",
            "fk_column_name": "FK_FIR_ID",
            "key_sequence": 1,
            "update_rule": "NO ACTION",
            "delete_rule": "NO ACTION",
            "fk_name": "LOGCOSTF_FK_FIR_ID",
            "pk_name": "FIR_PK",
            "deferrability": "NOT DEFERRABLE",
            "rely": "false",
            "comment": None,
        },
        {
            "created_on": "2022-04-22 05:44:36.834000-07:00",
            "pk_database_name": "TWZ_META",
            "pk_schema_name": "REP_DMA",
            "pk_table_name": "DM_D_PARTNERS",
            "pk_column_name": "DWH_DIM_ID",
            "fk_database_name": "TWZ_META",
            "fk_schema_name": "REP_DMA",
            "fk_table_name": "DM_F_LOGISTIC_COST_FACTORS",
            "fk_column_name": "FK_PAR_ID",
            "key_sequence": 1,
            "update_rule": "NO ACTION",
            "delete_rule": "NO ACTION",
            "fk_name": "LOGCOSTF_FK_PAR_ID",
            "pk_name": "PAR_PK",
            "deferrability": "NOT DEFERRABLE",
            "rely": "false",
            "comment": None,
        },
    ]
    constraints_foreign_key = mio.InstanceConstraint.factory(
        metadata, constraint_type="foreign_key"
    )
    assert len(constraints_foreign_key) == 3
    fk_names = set([cfk.fk_name for cfk in constraints_foreign_key])
    assert (
        set(["LOGCOSTF_FK_PAR_ID", "LOGCOSTF_FK_FIR_ID", "LOGCOSTF_FK_BOC_ID"])
        == fk_names
    )


# endregion constraints
