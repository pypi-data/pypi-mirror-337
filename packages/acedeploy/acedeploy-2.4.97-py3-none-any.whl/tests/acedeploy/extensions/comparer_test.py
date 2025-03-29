import acedeploy.extensions.comparer as comparer
import pytest


@pytest.mark.parametrize(
    "input, expected",
    [
        ("hello world", "hello world"),
        ("   hello world   ", "hello world"),
        ("   hello world   ", "hello world"),
        ("hello world   ", "hello world"),
        (
            """
  hello
  world
""",
            """
hello
world
""",
        ),
        (
            """
hello

world
""",
            """
hello
world
""",
        ),
        (
            """
  hello
  world
foo foo foo
               bar bar bar
    baz baz
""",
            """
hello
world
foo foo foo
bar bar bar
baz baz
""",
        ),
    ],
)
def test_remove_whitespace(input, expected):
    # arrange
    l = input

    # act
    result = comparer._remove_whitespace(l)

    # assert
    assert result.strip() == expected.strip()
