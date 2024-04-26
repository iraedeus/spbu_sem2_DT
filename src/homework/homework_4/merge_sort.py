import queue
from typing import Union
from threading import Thread


Comparable = Union[int, float, str]


def merge(first_arr: list, second_arr: list) -> list:
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


def merge_iter(arr: list[Comparable], init_step: int, step: int, n: int) -> list:
    output = []
    sep = init_step + step
    if init_step + step * 2 > n:
        output += merge(arr[init_step:sep], arr[sep:n])
    else:
        output += merge(arr[init_step:sep], arr[sep : init_step + step * 2])

    return output


def multi_merge_sort(arr: list[Comparable], threads_cnt: int, multiprocess: bool = False) -> list[Comparable]:
    q = queue.Queue[list[Comparable]]()

    def worker() -> None:
        while True:
            a = q.get()
            if q.qsize() != 0:
                b = q.get()
                q.put(merge(a, b))
                q.task_done()
                q.task_done()
            else:
                nonlocal arr
                arr = a
                q.task_done()

    threads = [Thread(target=worker, name=f"{i} Thread", daemon=True) for i in range(threads_cnt)]

    for t in threads:
        t.start()
    for elem in arr:
        q.put([elem])

    q.join()
    return arr


def merge_sort(arr: list[Comparable]) -> list[Comparable]:
    n = len(arr)
    i = 1
    while i < n:
        new_arr = []
        lists = [merge_iter(arr, j, i, n) for j in range(0, n, i * 2)]
        for list in lists:
            new_arr += list
        arr = new_arr
        i *= 2
    print(arr)
    return arr


def recursive_merge_sort(arr: list[Comparable]) -> list[Comparable]:
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    left_half = recursive_merge_sort(left_half)
    right_half = recursive_merge_sort(right_half)

    print(arr)
    return merge(left_half, right_half)
