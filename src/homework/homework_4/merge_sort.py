from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from typing import TypeVar

T = TypeVar("T", str, int, float)


def merge_two_sorted_lists(first_arr: list, second_arr: list) -> list:
    output = []
    n, m = 0, 0

    while n < len(first_arr) and m < len(second_arr):
        if first_arr[n] <= second_arr[m]:
            output.append(first_arr[n])
            n += 1
        else:
            output.append(second_arr[m])
            m += 1
    else:
        if n == len(first_arr):
            output += second_arr[m:]
        else:
            output += first_arr[n:]

    return output


def recursive_merge_sort(arr: list[T]) -> list[T]:
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    left_half = recursive_merge_sort(left_half)
    right_half = recursive_merge_sort(right_half)

    return merge_two_sorted_lists(left_half, right_half)


def thread_merge_sort(arr: list[T], threads_cnt: int) -> list[T]:
    if threads_cnt > len(arr):
        size = 1
    else:
        size = len(arr) // threads_cnt

    subarrs = [arr[i : i + size] for i in range(0, len(arr), size)]
    output: list[T] = []

    with ThreadPoolExecutor(max_workers=threads_cnt - 1) as executor:
        sorted_subarrs = [executor.submit(recursive_merge_sort, subarr) for subarr in subarrs]
        for sorted_subarr in as_completed(sorted_subarrs):
            output = merge_two_sorted_lists(output, sorted_subarr.result())

    return output


def multiprocess_merge_sort(arr: list[T], threads_cnt: int) -> list[T]:
    if threads_cnt > len(arr):
        size = 1
    else:
        size = len(arr) // threads_cnt
    subarrs = [arr[i : i + size] for i in range(0, len(arr), size)]
    output: list[T] = []

    with ProcessPoolExecutor(max_workers=threads_cnt - 1) as executor:
        sorted_subarrs = [executor.submit(recursive_merge_sort, subarr) for subarr in subarrs]
        for sorted_subarr in as_completed(sorted_subarrs):
            output = merge_two_sorted_lists(output, sorted_subarr.result())
    return output


def parallel_merge_sort(arr: list[T], threads_cnt: int, multiprocess: bool = False) -> list[T]:
    if multiprocess:
        output = multiprocess_merge_sort(arr, threads_cnt)
    else:
        output = thread_merge_sort(arr, threads_cnt)

    return output


if __name__ == "__main__":
    pass
