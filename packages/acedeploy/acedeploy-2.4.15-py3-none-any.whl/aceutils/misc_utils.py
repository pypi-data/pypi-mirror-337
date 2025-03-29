import re
from typing import Union


def map_datatype_name_to_default(datatype: str) -> str:
    """
    Return the default representation of a snowflake datatype.

    See also https://docs.snowflake.com/en/sql-reference/intro-summary-data-types.html

    Examples:
        TEXT -> VARCHAR
        INT -> NUMBER
        NUMBER(38,5) -> NUMBER
        VARCHAR(10) -> VARCHAR
    """
    # remove precision like (38,0) and strip whitespace
    datatype_clean = re.sub(r"\s*\([\d\s,]+\)", "", datatype.upper().strip())

    if datatype_clean in (
        "NUMBER",
        "DECIMAL",
        "NUMERIC",
        "INT",
        "INTEGER",
        "BIGINT",
        "SMALLINT",
    ):
        return "NUMBER"

    if datatype_clean in ("VARCHAR", "CHAR", "CHARACTER", "STRING", "TEXT"):
        return "VARCHAR"

    if datatype_clean in ("BINARY", "VARBINARY"):
        return "BINARY"

    if datatype_clean in ("DATETIME", "TIMESTAMP", "TIMESTAMP_NTZ"):
        return "TIMESTAMP_NTZ"

    if datatype_clean in (
        "FLOAT",
        "FLOAT4",
        "FLOAT8",
        "DOUBLE",
        "DOUBLE PRECISION",
        "REAL",
    ):
        return "FLOAT"

    return datatype


def string_or_bool_to_bool(v: Union[str, bool]) -> bool:
    """
    Given a boolean, return that boolean.
    Given a string,
    """
    vstr = str(v).lower()
    if vstr == "true":
        return True
    elif vstr == "false":
        return False
    else:
        raise ValueError(f"Given value '{v}' can not be interpreted as boolean.")
