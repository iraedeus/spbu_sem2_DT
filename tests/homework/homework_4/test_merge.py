from hypothesis import given, settings
from hypothesis import strategies as st

from src.homework.homework_4.merge_sort import *


@settings(max_examples=10)
@given(arr=st.lists(st.integers()))
def test_multiprocessing_merge(arr):
    assert list(sorted(arr)) == multi_merge_sort(arr, 10)
    assert multi_merge_sort(arr, 10) == multi_merge_sort(multi_merge_sort(arr, 10), 10)


@settings(max_examples=200)
@given(arr=st.lists(st.integers()))
def test_merge(arr):
    assert list(sorted(arr)) == recursive_merge_sort(arr)
