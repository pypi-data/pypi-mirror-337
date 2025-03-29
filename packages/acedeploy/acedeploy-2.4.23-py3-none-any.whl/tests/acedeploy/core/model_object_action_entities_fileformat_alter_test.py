import pytest

from acedeploy.core.model_instance_objects import InstanceFileformat
import acedeploy.core.model_object_action_entities as oae


@pytest.mark.parametrize(
    "current_instance, desired_instance",
    [
        (  # csv -> avro
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "AVRO",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"avro","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO"}',
                }
            ),
        ),
    ],
)
def test_ff_generate_alter_statement_raises_error_on_type_change(current_instance, desired_instance):
    with pytest.raises(ValueError):
        __ = oae.FileformatAction._generate_alter_statement(
        current_instance, desired_instance
    )


@pytest.mark.parametrize(
    "current_instance, desired_instance, expected",
    [
        (  # current == desired (no changes required)
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            "",
        ),
        (  # add comment
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "hello world",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET COMMENT = 'hello world';",
        ),
        (  # remove comment
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "hello world",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET COMMENT = '';",
        ),
    ]
)
def test_ff_generic_generate_alter_statement(
    current_instance: InstanceFileformat, desired_instance: InstanceFileformat, expected: str
):
    result = oae.FileformatAction._generate_alter_statement(
        current_instance, desired_instance
    )
    assert result == expected

@pytest.mark.parametrize(
    "current_instance, desired_instance, expected",
    [
        (  # record delimiter
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n-", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET RECORD_DELIMITER = '\\n-';",
        ),
        (  # field delimiter
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": ";", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET FIELD_DELIMITER = ';';",
        ),
        (  # file extension
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "csv", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET FILE_EXTENSION = 'csv';",
        ),
        (  # skip header
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 2, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET SKIP_HEADER = 2;",
        ),
        (  # date format
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "YYYY-MM-DD", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET DATE_FORMAT = 'YYYY-MM-DD';",
        ),
        (  # time format
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "HH24:MI:SS.FF", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET TIME_FORMAT = 'HH24:MI:SS.FF';",
        ),
        (  # timestamp format
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "YYYY-MM-DD HH24:MI:SS.FF TZHTZM", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF TZHTZM';",
        ),
        (  # binary format
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "UTF8", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET BINARY_FORMAT = 'UTF8';",
        ),
        (  # escape
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "/", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET ESCAPE = '/';",
        ),
        (  # escape unenclosed field
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "NONE", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET ESCAPE_UNENCLOSED_FIELD = 'NONE';",
        ),
        (  # TRIM_SPACE
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": true, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET TRIM_SPACE = TRUE;",
        ),
        (  # FIELD_OPTIONALLY_ENCLOSED_BY
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "'", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET FIELD_OPTIONALLY_ENCLOSED_BY = '''';",
        ),
        (  # NULL_IF
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N", "x"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET NULL_IF = ('\\\\N', 'x');",
        ),
        (  # ERROR_ON_COLUMN_COUNT_MISMATCH
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": false, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE;",
        ),
        (  # REPLACE_INVALID_CHARACTERS
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": true, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET REPLACE_INVALID_CHARACTERS = TRUE;",
        ),
        (  # EMPTY_FIELD_AS_NULL
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": false, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET EMPTY_FIELD_AS_NULL = FALSE;",
        ),
        (  # SKIP_BYTE_ORDER_MARK
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": false, "ENCODING": "UTF8"}""",
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET SKIP_BYTE_ORDER_MARK = FALSE;",
        ),
        (  # ENCODING
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "UTF8"}""",
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "CSV",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": """{"TYPE": "csv", "RECORD_DELIMITER": "\\n", "FIELD_DELIMITER": "|", "FILE_EXTENSION": "NONE", "SKIP_HEADER": 1, "DATE_FORMAT": "AUTO", "TIME_FORMAT": "AUTO", "TIMESTAMP_FORMAT": "AUTO", "BINARY_FORMAT": "HEX", "ESCAPE": "NONE", "ESCAPE_UNENCLOSED_FIELD": "\\\\", "TRIM_SPACE": false, "FIELD_OPTIONALLY_ENCLOSED_BY": "NONE", "NULL_IF": ["\\\\N"], "COMPRESSION": "AUTO", "ERROR_ON_COLUMN_COUNT_MISMATCH": true, "VALIDATE_UTF8": true, "SKIP_BLANK_LINES": false, "REPLACE_INVALID_CHARACTERS": false, "EMPTY_FIELD_AS_NULL": true, "SKIP_BYTE_ORDER_MARK": true, "ENCODING": "windows1252"}""",
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET ENCODING = 'windows1252';",
        ),
    ]
)
def test_ff_csv_generate_alter_statement(
    current_instance: InstanceFileformat, desired_instance: InstanceFileformat, expected: str
):
    result = oae.FileformatAction._generate_alter_statement(
        current_instance, desired_instance
    )
    assert result == expected


@pytest.mark.parametrize(
    "current_instance, desired_instance, expected",
    [
        (  # FILE_EXTENSION
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"js","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET FILE_EXTENSION = 'js';",
        ),
        (  # DATE_FORMAT
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"YYYY-MM-DD","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET DATE_FORMAT = 'YYYY-MM-DD';",
        ),
        (  # TIME_FORMAT
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"HH24:MI:SS.FF","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET TIME_FORMAT = 'HH24:MI:SS.FF';",
        ),
        (  # TIMESTAMP_FORMAT
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"YYYY-MM-DD HH24:MI:SS TZHTZM","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS TZHTZM';",
        ),
        (  # BINARY_FORMAT
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"UTF8","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET BINARY_FORMAT = 'UTF8';",
        ),
        (  # TRIM_SPACE
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":true,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET TRIM_SPACE = TRUE;",
        ),
        (  # NULL_IF
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":["\\\\N"],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET NULL_IF = ();",
        ),
        (  # COMPRESSION
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"GZIP","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET COMPRESSION = 'GZIP';",
        ),
        (  # ENABLE_OCTAL
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":true,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET ENABLE_OCTAL = TRUE;",
        ),
        (  # ALLOW_DUPLICATE
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":true,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET ALLOW_DUPLICATE = TRUE;",
        ),
        (  # STRIP_OUTER_ARRAY
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":true,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET STRIP_OUTER_ARRAY = TRUE;",
        ),
        (  # STRIP_NULL_VALUES
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":true,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET STRIP_NULL_VALUES = TRUE;",
        ),
        (  # IGNORE_UTF8_ERRORS
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":true,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET IGNORE_UTF8_ERRORS = TRUE;",
        ),
        (  # REPLACE_INVALID_CHARACTERS
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":true,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET REPLACE_INVALID_CHARACTERS = TRUE;",
        ),
        (  # SKIP_BYTE_ORDER_MARK
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "JSON",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"json","FILE_EXTENSION":"json","DATE_FORMAT":"AUTO","TIME_FORMAT":"AUTO","TIMESTAMP_FORMAT":"AUTO","BINARY_FORMAT":"HEX","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","ENABLE_OCTAL":false,"ALLOW_DUPLICATE":false,"STRIP_OUTER_ARRAY":false,"STRIP_NULL_VALUES":false,"IGNORE_UTF8_ERRORS":false,"REPLACE_INVALID_CHARACTERS":false,"SKIP_BYTE_ORDER_MARK":false}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET SKIP_BYTE_ORDER_MARK = FALSE;",
        ),
    ]
)
def test_ff_json_generate_alter_statement(
    current_instance: InstanceFileformat, desired_instance: InstanceFileformat, expected: str
):
    result = oae.FileformatAction._generate_alter_statement(
        current_instance, desired_instance
    )
    assert result == expected


@pytest.mark.parametrize(
    "current_instance, desired_instance, expected",
    [
        (  # TRIM_SPACE
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "AVRO",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"avro","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO"}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "AVRO",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"avro","TRIM_SPACE":true,"NULL_IF":[],"COMPRESSION":"AUTO"}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET TRIM_SPACE = TRUE;",
        ),
        (  # NULL_IF
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "AVRO",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"avro","TRIM_SPACE":false,"NULL_IF":["\\\\N"],"COMPRESSION":"AUTO"}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "AVRO",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"avro","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO"}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET NULL_IF = ();",
        ),
        (  # COMPRESSION
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "AVRO",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"avro","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO"}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "AVRO",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"avro","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"BROTLI"}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET COMPRESSION = 'BROTLI';",
        ),
    ]
)
def test_ff_avro_generate_alter_statement(
    current_instance: InstanceFileformat, desired_instance: InstanceFileformat, expected: str
):
    result = oae.FileformatAction._generate_alter_statement(
        current_instance, desired_instance
    )
    assert result == expected


@pytest.mark.parametrize(
    "current_instance, desired_instance, expected",
    [
        (  # TRIM_SPACE
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "ORC",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"orc","TRIM_SPACE":false,"NULL_IF":[]}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "ORC",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"orc","TRIM_SPACE":true,"NULL_IF":[]}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET TRIM_SPACE = TRUE;",
        ),
        (  # NULL_IF
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "ORC",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"orc","TRIM_SPACE":false,"NULL_IF":["x"]}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "ORC",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"orc","TRIM_SPACE":false,"NULL_IF":[]}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET NULL_IF = ();",
        ),
    ]
)
def test_ff_orc_generate_alter_statement(
    current_instance: InstanceFileformat, desired_instance: InstanceFileformat, expected: str
):
    result = oae.FileformatAction._generate_alter_statement(
        current_instance, desired_instance
    )
    assert result == expected

@pytest.mark.parametrize(
    "current_instance, desired_instance, expected",
    [
        (  # TRIM_SPACE
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "PARQUET",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"parquet","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","BINARY_AS_TEXT":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "PARQUET",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"parquet","TRIM_SPACE":true,"NULL_IF":[],"COMPRESSION":"AUTO","BINARY_AS_TEXT":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET TRIM_SPACE = TRUE;",
        ),
        (  # NULL_IF
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "PARQUET",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"parquet","TRIM_SPACE":false,"NULL_IF":["\\\\n"],"COMPRESSION":"AUTO","BINARY_AS_TEXT":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "PARQUET",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"parquet","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","BINARY_AS_TEXT":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET NULL_IF = ();",
        ),
        (  # COMPRESSION
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "PARQUET",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"parquet","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","BINARY_AS_TEXT":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "PARQUET",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"parquet","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"SNAPPY","BINARY_AS_TEXT":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET COMPRESSION = 'SNAPPY';",
        ),
        (  # BINARY_AS_TEXT
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "PARQUET",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"parquet","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","BINARY_AS_TEXT":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "PARQUET",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"parquet","TRIM_SPACE":false,"NULL_IF":[],"COMPRESSION":"AUTO","BINARY_AS_TEXT":false}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET BINARY_AS_TEXT = FALSE;",
        ),
    ]
)
def test_ff_parquet_generate_alter_statement(
    current_instance: InstanceFileformat, desired_instance: InstanceFileformat, expected: str
):
    result = oae.FileformatAction._generate_alter_statement(
        current_instance, desired_instance
    )
    assert result == expected

@pytest.mark.parametrize(
    "current_instance, desired_instance, expected",
    [
        (  # COMPRESSION
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "XML",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"xml","COMPRESSION":"AUTO","IGNORE_UTF8_ERRORS":false,"PRESERVE_SPACE":false,"STRIP_OUTER_ELEMENT":false,"DISABLE_SNOWFLAKE_DATA":false,"DISABLE_AUTO_CONVERT":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "XML",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"xml","COMPRESSION":"GZIP","IGNORE_UTF8_ERRORS":false,"PRESERVE_SPACE":false,"STRIP_OUTER_ELEMENT":false,"DISABLE_SNOWFLAKE_DATA":false,"DISABLE_AUTO_CONVERT":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET COMPRESSION = 'GZIP';",
        ),
        (  # IGNORE_UTF8_ERRORS
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "XML",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"xml","COMPRESSION":"AUTO","IGNORE_UTF8_ERRORS":false,"PRESERVE_SPACE":false,"STRIP_OUTER_ELEMENT":false,"DISABLE_SNOWFLAKE_DATA":false,"DISABLE_AUTO_CONVERT":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "XML",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"xml","COMPRESSION":"AUTO","IGNORE_UTF8_ERRORS":true,"PRESERVE_SPACE":false,"STRIP_OUTER_ELEMENT":false,"DISABLE_SNOWFLAKE_DATA":false,"DISABLE_AUTO_CONVERT":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET IGNORE_UTF8_ERRORS = TRUE;",
        ),
        (  # PRESERVE_SPACE
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "XML",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"xml","COMPRESSION":"AUTO","IGNORE_UTF8_ERRORS":false,"PRESERVE_SPACE":false,"STRIP_OUTER_ELEMENT":false,"DISABLE_SNOWFLAKE_DATA":false,"DISABLE_AUTO_CONVERT":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "XML",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"xml","COMPRESSION":"AUTO","IGNORE_UTF8_ERRORS":false,"PRESERVE_SPACE":true,"STRIP_OUTER_ELEMENT":false,"DISABLE_SNOWFLAKE_DATA":false,"DISABLE_AUTO_CONVERT":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET PRESERVE_SPACE = TRUE;",
        ),
        (  # STRIP_OUTER_ELEMENT
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "XML",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"xml","COMPRESSION":"AUTO","IGNORE_UTF8_ERRORS":false,"PRESERVE_SPACE":false,"STRIP_OUTER_ELEMENT":false,"DISABLE_SNOWFLAKE_DATA":false,"DISABLE_AUTO_CONVERT":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "XML",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"xml","COMPRESSION":"AUTO","IGNORE_UTF8_ERRORS":false,"PRESERVE_SPACE":false,"STRIP_OUTER_ELEMENT":true,"DISABLE_SNOWFLAKE_DATA":false,"DISABLE_AUTO_CONVERT":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET STRIP_OUTER_ELEMENT = TRUE;",
        ),
        (  # DISABLE_SNOWFLAKE_DATA
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "XML",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"xml","COMPRESSION":"AUTO","IGNORE_UTF8_ERRORS":false,"PRESERVE_SPACE":false,"STRIP_OUTER_ELEMENT":false,"DISABLE_SNOWFLAKE_DATA":false,"DISABLE_AUTO_CONVERT":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "XML",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"xml","COMPRESSION":"AUTO","IGNORE_UTF8_ERRORS":false,"PRESERVE_SPACE":false,"STRIP_OUTER_ELEMENT":false,"DISABLE_SNOWFLAKE_DATA":true,"DISABLE_AUTO_CONVERT":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET DISABLE_SNOWFLAKE_DATA = TRUE;",
        ),
        (  # DISABLE_AUTO_CONVERT
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "XML",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"xml","COMPRESSION":"AUTO","IGNORE_UTF8_ERRORS":false,"PRESERVE_SPACE":false,"STRIP_OUTER_ELEMENT":false,"DISABLE_SNOWFLAKE_DATA":false,"DISABLE_AUTO_CONVERT":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "XML",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"xml","COMPRESSION":"AUTO","IGNORE_UTF8_ERRORS":false,"PRESERVE_SPACE":false,"STRIP_OUTER_ELEMENT":false,"DISABLE_SNOWFLAKE_DATA":false,"DISABLE_AUTO_CONVERT":true,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET DISABLE_AUTO_CONVERT = TRUE;",
        ),
        (  # xxxx
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "XML",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"xml","COMPRESSION":"AUTO","IGNORE_UTF8_ERRORS":false,"PRESERVE_SPACE":false,"STRIP_OUTER_ELEMENT":false,"DISABLE_SNOWFLAKE_DATA":false,"DISABLE_AUTO_CONVERT":false,"SKIP_BYTE_ORDER_MARK":true}',
                }
            ),
            InstanceFileformat(
                {
                    "name": "MY_OBJECT",
                    "database_name": "ACEDEPLOY_META_DB",
                    "schema_name": "MY_SCHEMA",
                    "type": "XML",
                    "owner": "R_ACEDEPLOY",
                    "comment": "",
                    "format_options": '{"TYPE":"xml","COMPRESSION":"AUTO","IGNORE_UTF8_ERRORS":false,"PRESERVE_SPACE":false,"STRIP_OUTER_ELEMENT":false,"DISABLE_SNOWFLAKE_DATA":false,"DISABLE_AUTO_CONVERT":false,"SKIP_BYTE_ORDER_MARK":false}',
                }
            ),
            "ALTER FILE FORMAT MY_SCHEMA.MY_OBJECT SET SKIP_BYTE_ORDER_MARK = FALSE;",
        ),
    ]
)
def test_ff_xml_generate_alter_statement(
    current_instance: InstanceFileformat, desired_instance: InstanceFileformat, expected: str
):
    result = oae.FileformatAction._generate_alter_statement(
        current_instance, desired_instance
    )
    assert result == expected
