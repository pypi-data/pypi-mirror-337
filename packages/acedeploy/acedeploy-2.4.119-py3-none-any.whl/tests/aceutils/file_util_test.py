import os

import aceutils.file_util as file_util
import pytest


@pytest.mark.parametrize(
    "input, expected",
    [
        ([], os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))),
        (
            ["f1"],
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "f1")),
        ),
        (
            ["f1", "f2"],
            os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "f1", "f2")
            ),
        ),
        (
            ["f1", "f2", "f3.sql"],
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__), "..", "..", "f1", "f2", "f3.sql"
                )
            ),
        ),
    ],
)
def test_get_path(input, expected):
    # arrange
    i = input
    # act
    result = file_util.get_path(i)
    # assert
    assert result == expected

@pytest.mark.parametrize(
    "filenames, filters, expected",
    [
        (["some/allowed/folder/file.txt", "some/forbidden/folder/file.txt"], ["*/forbidden/*"], ["some/allowed/folder/file.txt"]),
        (["allowed/file1.txt", "forbidden/file2.txt", "allowed/file3.txt"], ["forbidden/*"], ["allowed/file1.txt", "allowed/file3.txt"]),
        (["dir1/file.txt", "dir2/forbidden/file.txt", "dir3/file.txt"], ["*/forbidden/*"], ["dir1/file.txt", "dir3/file.txt"]),
        (["file1.txt", "file2.forbidden", "file3.txt"], ["*.forbidden"], ["file1.txt", "file3.txt"]),
        (["a/b/c.txt", "a/forbidden/c.txt", "a/b/d.txt"], ["a/forbidden/*"], ["a/b/c.txt", "a/b/d.txt"]),
        (["keep/this/file.txt", "remove/that/file.txt"], ["remove/*"], ["keep/this/file.txt"]),
        (["dir/keep.txt", "dir/forbidden.txt"], ["dir/forbidden.txt"], ["dir/keep.txt"]),
        (["folder1/file.txt", "folder2/forbidden/file.txt", "folder3/file.txt"], ["folder2/forbidden/*"], ["folder1/file.txt", "folder3/file.txt"]),
        (["path/to/keep.txt", "path/to/forbidden.txt"], ["path/to/forbidden.txt"], ["path/to/keep.txt"]),
        (["allowed/file.txt", "forbidden/file.txt"], ["forbidden/*"], ["allowed/file.txt"]),
        (
            ["some/path1/file.txt", "some/path2/file.txt"],
            [],
            ["some/path1/file.txt", "some/path2/file.txt"],
        ),
        (
            [
                "sql/MY_SOLUTION/SCHEMA1/Tables/SCHEMA1.T1.sql",
                "sql/MY_SOLUTION/SCHEMA1/Snowpark/some_file.sql",
                "sql/MY_SOLUTION/SCHEMA1/Snowpark/folder/some_file.sql",
                "sql/MY_SOLUTION/Snowpark/Tables/Snowpark.T1.sql",
            ],
            [
                "*/*/*/Snowpark/*"
            ],
            [
                "sql/MY_SOLUTION/SCHEMA1/Tables/SCHEMA1.T1.sql",
                "sql/MY_SOLUTION/Snowpark/Tables/Snowpark.T1.sql",
            ],
        ),
    ],
)
def test_filter_filelist_negative(filenames, filters, expected):
    # act
    result = file_util.filter_filelist_negative(filenames, filters,)
    # assert
    assert result == expected
