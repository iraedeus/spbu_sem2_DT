from hypothesis import given, settings
from hypothesis import strategies as st

from src.homework.homework_4.merge_sort import *


@settings(max_examples=1000)
@given(arr=st.lists(st.integers()), threads_cnt=st.integers(min_value=2, max_value=32))
def test_threading_merge(arr, threads_cnt):
    assert list(sorted(arr)) == parallel_merge_sort(arr, threads_cnt)
    assert parallel_merge_sort(arr, threads_cnt) == parallel_merge_sort(
        parallel_merge_sort(arr, threads_cnt), threads_cnt
    )


@settings(max_examples=1000)
@given(arr=st.lists(st.integers()), threads_cnt=st.integers(min_value=2, max_value=4))
def test_multiprocess_merge(arr, threads_cnt):
    assert list(sorted(arr)) == parallel_merge_sort(arr, 4, True)


@settings(max_examples=1000)
@given(arr=st.lists(st.integers()))
def test_merge(arr):
    assert list(sorted(arr)) == recursive_merge_sort(arr)


@settings(max_examples=1000)
@given(first_arr=st.lists(st.integers()), second_arr=st.lists(st.integers()))
def test_merge_two_arrs(first_arr, second_arr):
    first_arr = list(sorted(first_arr))
    second_arr = list(sorted(second_arr))
    assert list(sorted(merge_two_sorted_lists(first_arr, second_arr))) == merge_two_sorted_lists(first_arr, second_arr)
