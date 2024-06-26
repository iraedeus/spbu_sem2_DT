from abc import ABCMeta, abstractmethod
from concurrent.futures import Future, ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from typing import Any, Protocol, TypeVar, Union


class Comparable(Protocol):
    @abstractmethod
    def __lt__(self: "CT", other: "CT") -> bool:
        ...

    @abstractmethod
    def __le__(self: "CT", other: "CT") -> bool:
        ...


CT = TypeVar("CT", bound=Comparable)


def merge_two_sorted_lists(first_arr: list[CT], second_arr: list[CT]) -> list:
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


def recursive_merge_sort(arr: list[CT]) -> list[CT]:
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    left_half = recursive_merge_sort(left_half)
    right_half = recursive_merge_sort(right_half)

    return merge_two_sorted_lists(left_half, right_half)


def threading_recursive_merge_sort(arr: list[CT], threads_cnt: int, multiprocess: bool) -> list[CT]:
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    sublist_1: Union[Future, list[CT]]
    sublist_2: Union[Future, list[CT]]

    if threads_cnt == 2:
        if multiprocess:
            with ThreadPoolExecutor(max_workers=2) as executor:
                sublist_1 = executor.submit(recursive_merge_sort, left_half)
                sublist_2 = executor.submit(recursive_merge_sort, right_half)
                return merge_two_sorted_lists(sublist_1.result(), sublist_2.result())
        else:
            with ProcessPoolExecutor(max_workers=2) as executor:
                sublist_1 = executor.submit(recursive_merge_sort, left_half)
                sublist_2 = executor.submit(recursive_merge_sort, right_half)
                return merge_two_sorted_lists(sublist_1.result(), sublist_2.result())

    elif threads_cnt > 2:
        sublist_1 = threading_recursive_merge_sort(left_half, threads_cnt // 2, multiprocess)
        sublist_2 = threading_recursive_merge_sort(right_half, threads_cnt // 2, multiprocess)
        return merge_two_sorted_lists(sublist_1, sublist_2)
    else:
        return merge_two_sorted_lists(recursive_merge_sort(left_half), recursive_merge_sort(right_half))


def get_subarrs(arr: list[CT], threads_cnt: int) -> list[list[CT]]:
    if threads_cnt > len(arr):
        size = 1
    else:
        size = len(arr) // threads_cnt

    return [arr[i : i + size] for i in range(0, len(arr), size)]


def executor_work(
    executor: Union[ThreadPoolExecutor, ProcessPoolExecutor], subarrs: list[list[CT]], output: list[CT]
) -> list[CT]:
    sorted_subarrs: list = [executor.submit(recursive_merge_sort, subarr) for subarr in subarrs]
    for sorted_subarr in as_completed(sorted_subarrs):
        output = merge_two_sorted_lists(output, sorted_subarr.result())
    return output


def thread_merge_sort(arr: list[CT], threads_cnt: int) -> list[CT]:
    subarrs = get_subarrs(arr, threads_cnt)
    with ThreadPoolExecutor(max_workers=threads_cnt - 1) as executor:
        return executor_work(executor, subarrs, [])


def multiprocess_merge_sort(arr: list[CT], threads_cnt: int) -> list[CT]:
    subarrs = get_subarrs(arr, threads_cnt)
    with ProcessPoolExecutor(max_workers=threads_cnt - 1) as executor:
        return executor_work(executor, subarrs, [])


def first_merge_sort(arr: list[CT], threads_cnt: int, multiprocess: bool = False) -> list[CT]:
    if multiprocess and threads_cnt > 0:
        output = multiprocess_merge_sort(arr, threads_cnt)
    elif threads_cnt > 0:
        output = thread_merge_sort(arr, threads_cnt)
    else:
        output = recursive_merge_sort(arr)

    return output


def second_merge_sort(arr: list[CT], threads_cnt: int, multiprocess: bool = False) -> list[CT]:
    if multiprocess and threads_cnt > 0:
        output = threading_recursive_merge_sort(arr, threads_cnt, multiprocess)
    else:
        output = recursive_merge_sort(arr)

    return output


if __name__ == "__main__":
    pass
