import os
import re
import textwrap
import warnings

import pytest
import regex


@pytest.mark.description("Filename must end with .sql")
def test_file_extension_sql(filepath, content, content_clean, object_type):
    assert filepath.lower().endswith(
        ".sql"
    ), f"File name '{filepath}' does not end with '.sql'."


@pytest.mark.description("Statement must end with semicolon")
def test_ends_with_semicolon(filepath, content, content_clean, object_type):
    assert content_clean.rstrip().endswith(
        ";"
    ), f"SQL statement in '{filepath}' does not end with semicolon."


@pytest.mark.description("File name must match object name")
def test_filepath_match_objectname(filepath, content, content_clean, object_type):
    content_stripped = " ".join(
        content_clean.split()
    ).casefold()  # remove linebreaks, tabs and duplicate spaces
    if object_type == "SCHEMA":
        match = re.match(
            r"create\s+(?:or\s+replace\s+)?schema\s+\"?([a-zA-Z0-9_$]+)\"?",
            content_stripped,
        )
        assert (
            os.path.basename(filepath).casefold().replace(".sql", "").casefold()
            == match.groups()[0]
        ), f"File name '{filepath}' does not match object name'{match.groups()[0]}'."
    else:
        match = re.match(
            r"create[a-zA-Z0-9_$\s]*\s\"?([a-zA-Z0-9_$]+\"?\.\"?[a-zA-Z0-9_$#]+)\"?",
            content_stripped,
        )
        assert os.path.basename(filepath).casefold().replace(
            ".sql", ""
        ) == match.groups()[0].replace(
            '"', ""
        ), f"File name '{filepath}' does not match object name'{match.groups()[0]}'."


@pytest.mark.description("File must be in correct schema folder")
def test_file_folder(filepath, content, content_clean, object_type):
    filename_split = (
        os.path.basename(filepath).casefold().replace(".sql", "").split(".")
    )
    schema_from_filepath = filename_split[0]
    if len(filename_split) == 1:  # schema file
        assert (
            os.path.basename(os.path.dirname(filepath)).casefold()
            == schema_from_filepath
        ), f"Schema file '{filepath}' is not in correct schema folder."
    else:  # object file
        assert (
            os.path.basename(os.path.dirname(os.path.dirname(filepath))).casefold()
            == schema_from_filepath
        ), f"Object file '{filepath}' is not in correct schema folder."


@pytest.mark.description("There can be no sql comments after the semicolon")
def test_comment_after_statement(filepath, content, content_clean, object_type):
    content_without_whitespace = textwrap.dedent(content.strip())
    if regex.search(r";[^;]+$", content_without_whitespace):
        warnings.warn(f"There can be no sql comments after the semicolon")
    assert True


@pytest.mark.description("File must contain exactly one statement")
def test_contains_single_statement(filepath, content, content_clean, object_type):
    assert content_clean.count(";") <= 1


@pytest.mark.description(
    'File must be in correct folder for type (e.g. tables in folder "Tables")'
)
def test_file_correct_folder(filepath, content, content_clean, object_type):
    assert (
        re.match(
            rf"CREATE\s+(?:OR\s+REPLACE\s+)?{object_type}\s",
            content_clean,
            re.IGNORECASE,
        )
        is not None
    ), f"File '{filepath}' is in wrong object folder for it's object type."
