import acedeploy.core.model_git_entities as mge
import pytest


@pytest.mark.parametrize(
    "file_name, git_change_type, expected_file_name, expected_git_change_type",
    [
        ("/path/to/my/file.sql", "M", "/path/to/my/file.sql", "M"),
        ("/path/to/my/file.sql", "A", "/path/to/my/file.sql", "A"),
        ("/path/to/my/file.sql", "R", "/path/to/my/file.sql", "R"),
        ("/path/to/my/file.sql", "D", "/path/to/my/file.sql", "D"),
        ("/path/to/my/file.sql", "m", "/path/to/my/file.sql", "M"),
    ],
)
def test_GitFile(
    file_name, git_change_type, expected_file_name, expected_git_change_type
):
    g = mge.GitFile(file_name=file_name, git_change_type=git_change_type)
    assert g.file_name == expected_file_name
    assert g.change_type == expected_git_change_type
