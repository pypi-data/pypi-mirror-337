import aceutils.database_management as dbm
import pytest


@pytest.mark.parametrize(
    "input, expected",
    [
        (["schema.table", "schema", "database.schema.table"], True),
        (["schema.TABLE", "SCHEMA", "database1.schema2.t4ble"], True),
        (["my_schema.my_table", "my_schema", "my_db.schema2.my_table"], True),
        (['schema."table-with-dashes"', '"schema213"'], True),
        (['"sch$ema"."table"', 'schema."tabl$e"'], True),
        (["schema.my-table", "schema", "database.schema.table"], False),
        (["schema.my$table", "schema", "database.schema.table"], False),
        (["schema. table", "schema", "database.schema.table"], False),
        (["schema.table ", "schema", "database.schema.table"], False),
        (["schema.table", "schema( )", "database.schema.table"], False),
        (["schema.table", "drop database d", "database.schema.table"], False),
        (["schema.table;", "drop database d", "database.schema.table"], False),
    ],
)
def test_find_invalid_sql(input, expected):
    # arrange
    l = input

    # act
    result = dbm.check_input_list_valid(l)

    # assert
    assert result == expected
