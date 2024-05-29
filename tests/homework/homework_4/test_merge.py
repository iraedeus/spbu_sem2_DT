from hypothesis import given, settings
from hypothesis import strategies as st

from src.homework.homework_4.merge_sort import *


@settings(max_examples=1000, deadline=None)
@given(arr=st.lists(st.integers()), threads_cnt=st.integers(min_value=2, max_value=32))
def test_threading_merge(arr, threads_cnt):
    assert list(sorted(arr)) == first_merge_sort(arr, threads_cnt)
    assert first_merge_sort(arr, threads_cnt) == first_merge_sort(first_merge_sort(arr, threads_cnt), threads_cnt)
    assert list(sorted(arr)) == second_merge_sort(arr, threads_cnt)
    assert second_merge_sort(arr, threads_cnt) == second_merge_sort(second_merge_sort(arr, threads_cnt), threads_cnt)


@settings(max_examples=1000, deadline=None)
@given(arr=st.lists(st.integers()), threads_cnt=st.integers(min_value=2, max_value=4))
def test_multiprocess_merge(arr, threads_cnt):
    assert list(sorted(arr)) == first_merge_sort(arr, 4, True)
    assert list(sorted(arr)) == second_merge_sort(arr, 4, True)


@settings(max_examples=1000, deadline=None)
@given(arr=st.lists(st.integers()))
def test_merge(arr):
    assert list(sorted(arr)) == first_merge_sort(arr, 0)
    assert list(sorted(arr)) == second_merge_sort(arr, 0)


@settings(max_examples=1000, deadline=None)
@given(first_arr=st.lists(st.integers()), second_arr=st.lists(st.integers()))
def test_merge_two_arrs(first_arr, second_arr):
    first_arr = list(sorted(first_arr))
    second_arr = list(sorted(second_arr))
    assert list(sorted(merge_two_sorted_lists(first_arr, second_arr))) == merge_two_sorted_lists(first_arr, second_arr)
