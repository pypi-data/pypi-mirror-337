import aceutils.dict_and_list_util as dlu
import pytest


@pytest.mark.parametrize(
    "dict1, dict2, expected",
    [
        ({"one": 1}, {"one": 1}, ({}, {})),
        ({"one": 1}, {"one": 2}, ({"one": 1}, {"one": 2})),
        ({"one": 1, "two": "zwei"}, {"one": 1, "two": "zwei"}, ({}, {})),
        (
            {"one": 1, "two": "zwei"},
            {"one": 1, "two": "zwei", "three": "drei"},
            ({}, {"three": "drei"}),
        ),
        (
            {"one": 1, "two": "zwei", "three": "drei"},
            {"one": 1, "two": "zwei"},
            ({"three": "drei"}, {}),
        ),
        (
            {"one": 1, "two": "zwei", "three": "drei"},
            {"one": 1, "two": "zwei", 4: 4},
            ({"three": "drei"}, {4: 4}),
        ),
    ],
)
def test_compare_dicts(dict1, dict2, expected):
    # act
    result = dlu.compare_dicts(dict1, dict2)

    # assert
    assert result == expected

@pytest.mark.parametrize(
    "dict1, dict2, expected",
    [
        ({"one": 1}, {"one": 1}, ({}, {})),
        ({"one": 1}, {"one": 2}, ({"one": 1}, {"one": 2})),
        ({"one": 1, "two": "zwei"}, {"one": 1, "two": "zwei"}, ({}, {})),
        (
            {"one": 1, "two": "zwei"},
            {"one": 1, "two": "zwei", "three": "drei"},
            ({}, {"three": "drei"}),
        ),
        (
            {"one": 1, "two": "zwei", "three": "drei"},
            {"one": 1, "two": "zwei"},
            ({"three": "drei"}, {}),
        ),
        (
            {"one": 1, "two": "zwei", "three": "drei"},
            {"one": 1, "two": "zwei", 4: 4},
            ({"three": "drei"}, {4: 4}),
        ),
        (
            {"one": 1, "two": "zwei", "three": {"nested1": 1, "nested2": 2}},
            {"one": 1, "two": "zwei",},
            ({"three": {"nested1": 1, "nested2": 2}}, {}),
        ),
        (
            {"one": 1, "two": "zwei",},
            {"one": 1, "two": "zwei", "three": {"nested1": 1, "nested2": 2}},
            ({}, {"three": {"nested1": 1, "nested2": 2}}),
        ),
    ],
)
def test_compare_nested_dicts(dict1, dict2, expected):
    # act
    result = dlu.compare_nested_dicts(dict1, dict2)

    # assert
    assert result == expected


@pytest.mark.parametrize(
    "dict1, expected",
    [
        ({"one": 1}, {"one": 1}),
        ({"one": 1, "two": ""}, {"one": 1}),
        ({"one": 1, "two": []}, {"one": 1}),
        ({"one": 1, "two": {}}, {"one": 1}),
        ({"one": 1, "two": None}, {"one": 1}),
        ({"one": 1, "two": {"hello": "world"}}, {"one": 1, "two": {"hello": "world"}}),
        (
            {"one": 1, "two": {"hello": "world", "nothing": ""}},
            {"one": 1, "two": {"hello": "world"}},
        ),
        (
            {"one": 1, "two": {"hello": "world", "nothing": []}},
            {"one": 1, "two": {"hello": "world"}},
        ),
        (
            {"one": 1, "two": {"hello": "world", "nothing": {}}},
            {"one": 1, "two": {"hello": "world"}},
        ),
        (
            {"one": 1, "two": {"hello": "world", "nothing": None}},
            {"one": 1, "two": {"hello": "world"}},
        ),
    ],
)
def test_strip_nested_dict(dict1, expected):
    # act
    result = dlu.strip_nested_dict(dict1)

    # assert
    assert result == expected


@pytest.mark.parametrize(
    "list1, expected",
    [
        (None, []),
        ([], []),
        (["hello", "world"], ["hello", "world"]),
        (["HELLO", "WORLD"], ["hello", "world"]),
        (["H3ll0", "w0RlD"], ["h3ll0", "w0rld"]),
        (["ß"], ["ss"]),
    ],
)
def test_list_casefold(list1, expected):
    # act
    result = dlu.list_casefold(list1)

    # assert
    assert result == expected


@pytest.mark.parametrize(
    "list1, expected",
    [
        (None, []),
        ([], []),
        (["hello", "world"], ["HELLO", "WORLD"]),
        (["HELLO", "WORLD"], ["HELLO", "WORLD"]),
        (["H3ll0", "w0RlD"], ["H3LL0", "W0RLD"]),
    ],
)
def test_list_upper(list1, expected):
    # act
    result = dlu.list_upper(list1)

    # assert
    assert result == expected


@pytest.mark.parametrize(
    "list1, expected",
    [
        (None, []),
        ([], []),
        (["hello", "world"], ["hello", "world"]),
        (["HELLO", "WORLD"], ["hello", "world"]),
        (["H3ll0", "w0RlD"], ["h3ll0", "w0rld"]),
    ],
)
def test_list_lower(list1, expected):
    # act
    result = dlu.list_lower(list1)

    # assert
    assert result == expected


@pytest.mark.parametrize(
    "input, expected",
    [
        (
            [35, 53, [525, 6743], 64, 63, [743, 754, 757]],
            [35, 53, 525, 6743, 64, 63, 743, 754, 757],
        ),
        (
            [35, 53, 525, 6743, 64, 63, 743, 754, 757],
            [35, 53, 525, 6743, 64, 63, 743, 754, 757],
        ),
        (["x", 1, 5.123], ["x", 1, 5.123]),
        ("x", ["x"]),
        ([[123]], [123]),
    ],
)
def test_flatten(input, expected):
    # arrange
    l = input
    # act
    result = dlu.flatten(l)
    # assert
    assert result == expected


@pytest.mark.parametrize(
    "lst, n, expected",
    [
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5, [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 6, [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10]]),
        ([1, 2, 3, 4, 5, 7, 8, 9, 10], 11, [[1, 2, 3, 4, 5, 7, 8, 9, 10]]),
    ],
)
def test_chunks(lst, n, expected):
    result = dlu.chunks(lst, n)
    assert list(result) == expected


@pytest.mark.parametrize(
    "list_a, list_b, expected",
    [
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [9, 10], True),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [10], True),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [], True),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], True),
        ([9, 10], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], False),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [8, 9], False),
        ([1, '2', 'three'], ['2', 'three'], True),
        ([1, '2', 'three'], [9, 10], False),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [8, 10], False),
    ],
)
def test_list_ends_with_list(list_a, list_b, expected):
    result = dlu.list_ends_with_list(list_a, list_b)
    assert result == expected
