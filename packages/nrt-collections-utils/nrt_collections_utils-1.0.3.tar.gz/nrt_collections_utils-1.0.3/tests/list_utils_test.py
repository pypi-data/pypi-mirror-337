import pytest

from nrt_collections_utils.list_utils import ListUtil
from tests.list_utils_data import compare_lists_data


@pytest.mark.parametrize('list_1, list_2, expected_result', compare_lists_data)
def test_compare_lists(list_1, list_2, expected_result):
    assert ListUtil.compare_lists(list_1, list_2) == expected_result


def test_remove_none():
    assert ListUtil.remove_none([0, 1, None, 2, None, 3]) == [0, 1, 2, 3]
    assert ListUtil.remove_none([None, None, None]) == []
    assert ListUtil.remove_none([-1, 0, 1, 2, 3]) == [-1, 0, 1, 2, 3]
    assert ListUtil.remove_none([]) == []
    assert ListUtil.remove_none([0.0]) == [0.0]


def test_remove_empty():
    assert ListUtil.remove_empty([1, None, 2, '', 3, 0]) == [1, 2, 3, 0]
    assert ListUtil.remove_empty([None, '', None]) == []
    assert ListUtil.remove_empty([-1, 0, 1, 2, 3]) == [-1, 0, 1, 2, 3]
    assert ListUtil.remove_empty([]) == []
    assert ListUtil.remove_empty([0.0]) == [0.0]


def test_remove_duplicates():
    assert ListUtil.compare_lists(
        ListUtil.remove_duplicates([1, 2, 3, 1, 2, 3]), [1, 2, 3])

    assert ListUtil.compare_lists(ListUtil.remove_duplicates([1, 1, 1, 1, 1]), [1])

    assert ListUtil.remove_duplicates([]) == []

    assert ListUtil.compare_lists(ListUtil.remove_duplicates([1, 2, 3]), [1, 2, 3])

    assert ListUtil.compare_lists(
        ListUtil.remove_duplicates(['a', 'b', 'c', 'a', 'b', 'c']), ['a', 'b', 'c'])

    assert ListUtil.compare_lists(
        ListUtil.remove_duplicates(['a', None, 'b', None]), ['a', None, 'b'])
