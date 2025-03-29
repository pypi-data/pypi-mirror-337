import acedeploy.core.model_sql_entities as mse
import pytest

# region mse.DbObject


@pytest.mark.parametrize(
    "_input, _output",
    [
        (mse.DbObjectType.SCHEMA, "SCHEMA"),
        (mse.DbObjectType.TABLE, "TABLE"),
        (mse.DbObjectType.VIEW, "VIEW"),
        (mse.DbObjectType.EXTERNALTABLE, "EXTERNAL TABLE"),
        (mse.DbObjectType.MATERIALIZEDVIEW, "MATERIALIZED VIEW"),
        (mse.DbObjectType.FUNCTION, "FUNCTION"),
        (mse.DbObjectType.PROCEDURE, "PROCEDURE"),
        (mse.DbObjectType.STAGE, "STAGE"),
        (mse.DbObjectType.FILEFORMAT, "FILE FORMAT"),
        (mse.DbObjectType.STREAM, "STREAM"),
        (mse.DbObjectType.TASK, "TASK"),
        (mse.DbObjectType.PIPE, "PIPE"),
        (mse.DbObjectType.SEQUENCE, "SEQUENCE"),
        (mse.DbObjectType.MASKINGPOLICY, "MASKING POLICY"),
        (mse.DbObjectType.ROWACCESSPOLICY, "ROW ACCESS POLICY"),
        (mse.DbObjectType.DYNAMICTABLE, "DYNAMIC TABLE"),
        (mse.DbObjectType.NETWORKRULE, "NETWORK RULE"),
    ],
)
def test_get_sql_object_type_success(_input, _output):
    parameter = _input
    result = mse.DbObjectType.get_sql_object_type(parameter)
    assert result == _output


@pytest.mark.parametrize(
    "_input, _error, _error_message",
    [("error", ValueError, r"Given DbObjectType not recognized.")],
)
def test_get_sql_object_type_failure(_input, _error, _error_message):
    with pytest.raises(_error, match=_error_message):
        parameter = _input
        __ = mse.DbObjectType.get_sql_object_type(parameter)


@pytest.mark.parametrize(
    "_input, _output",
    [
        (mse.DbObjectType.SCHEMA, "SCHEMAS"),
        (mse.DbObjectType.TABLE, "TABLES"),
        (mse.DbObjectType.EXTERNALTABLE, "EXTERNAL TABLES"),
        (mse.DbObjectType.VIEW, "VIEWS"),
        (mse.DbObjectType.MATERIALIZEDVIEW, "MATERIALIZED VIEWS"),
        (mse.DbObjectType.FUNCTION, "FUNCTIONS"),
        (mse.DbObjectType.PROCEDURE, "PROCEDURES"),
        (mse.DbObjectType.STAGE, "STAGES"),
        (mse.DbObjectType.FILEFORMAT, "FILE FORMATS"),
        (mse.DbObjectType.STREAM, "STREAMS"),
        (mse.DbObjectType.TASK, "TASKS"),
        (mse.DbObjectType.PIPE, "PIPES"),
        (mse.DbObjectType.SEQUENCE, "SEQUENCES"),
        (mse.DbObjectType.MASKINGPOLICY, "MASKING POLICIES"),
        (mse.DbObjectType.ROWACCESSPOLICY, "ROW ACCESS POLICIES"),
        (mse.DbObjectType.DYNAMICTABLE, "DYNAMIC TABLES"),
        (mse.DbObjectType.NETWORKRULE, "NETWORK RULES"),
    ],
)
def test_get_object_type_for_show(_input, _output):
    parameter = _input
    result = mse.DbObjectType.get_object_type_for_show(parameter)
    assert result == _output


@pytest.mark.parametrize(
    "_input, _error, _error_message",
    [("error", ValueError, r"Given DbObjectType not recognized.")],
)
def test_get_object_type_for_show_failure(_input, _error, _error_message):
    with pytest.raises(_error, match=_error_message):
        parameter = _input
        __ = mse.DbObjectType.get_object_type_for_show(parameter)


@pytest.mark.parametrize(
    "_input, _output",
    [
        (mse.DbObjectType.SCHEMA, "SCHEMA"),
        (mse.DbObjectType.TABLE, "TABLE"),
        (mse.DbObjectType.EXTERNALTABLE, "TABLE"),
        (mse.DbObjectType.VIEW, "VIEW"),
        (mse.DbObjectType.MATERIALIZEDVIEW, "VIEW"),
        (mse.DbObjectType.FUNCTION, "FUNCTION"),
        (mse.DbObjectType.PROCEDURE, "PROCEDURE"),
        # (mse.DbObjectType.STAGE, ''), # not supported
        (mse.DbObjectType.FILEFORMAT, "FILE_FORMAT"),
        (mse.DbObjectType.STREAM, "STREAM"),
        (mse.DbObjectType.TASK, "TASK"),
        (mse.DbObjectType.PIPE, "PIPE"),
        (mse.DbObjectType.SEQUENCE, "SEQUENCE"),
        (mse.DbObjectType.MASKINGPOLICY, "POLICY"),
        (mse.DbObjectType.ROWACCESSPOLICY, "POLICY"),
        (mse.DbObjectType.DYNAMICTABLE, "TABLE"),
        # (mse.DbObjectType.NETWORKRULE, ''), # not supported
    ],
)
def test_get_object_type_for_get_ddl(_input, _output):
    parameter = _input
    result = mse.DbObjectType.get_object_type_for_get_ddl(parameter)
    assert result == _output


@pytest.mark.parametrize(
    "_input, _error, _error_message",
    [
        ("error", ValueError, r"Given DbObjectType not recognized."),
        (
            mse.DbObjectType.STAGE,
            ValueError,
            r"Object of type STAGE cannot be used in GET_DDL()",
        ),
    ],
)
def test_get_object_type_for_get_ddl_failure(_input, _error, _error_message):
    with pytest.raises(_error, match=_error_message):
        parameter = _input
        __ = mse.DbObjectType.get_object_type_for_get_ddl(parameter)



@pytest.mark.parametrize(
    "_input, _output",
    [
        ("TABLE", mse.DbObjectType.TABLE),
        ("VIEW", mse.DbObjectType.VIEW),
    ],
)
def test_get_object_type_for_policy_references(_input, _output):
    parameter = _input
    result = mse.DbObjectType.get_object_type_for_policy_references(parameter)
    assert result == _output
