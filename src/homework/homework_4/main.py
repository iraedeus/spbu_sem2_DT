import argparse
import copy
import random
import time
from typing import Any, Callable

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from merge_sort import *
from numpy.typing import ArrayLike

matplotlib.use("TkAgg")


def parse_cmd() -> dict[str, Any]:
    parser = argparse.ArgumentParser(prog="Comparing threading and non-threading merge sort")
    parser.add_argument("arr_size", type=int)
    parser.add_argument("thread_count", type=int, nargs="+")
    parser.add_argument("output_file", type=str)
    parser.add_argument("--multiprocess", action="store_true")
    args = parser.parse_args()

    return vars(args)


def evaluate_time(func: Callable, args: list[Any], is_threading: bool) -> float:
    if is_threading:
        start = time.perf_counter()
        func(*args)
        end = time.perf_counter()
    else:
        start = time.perf_counter()
        func(args[0])
        end = time.perf_counter()

    return end - start


def check_time(func: Callable, input_data: dict[str, Any], is_threading: bool) -> ArrayLike:
    output_time = np.array([])
    num_of_tests = 3
    size = input_data["arr_size"]
    threads = input_data["thread_count"]
    array = random.sample(range(-1000000, 1000000), size)
    for thread_cnt in threads:
        total_time = 0.0
        for j in range(num_of_tests):
            arr_copy = copy.copy(array)
            args = [arr_copy, thread_cnt, input_data["multiprocess"]]

            start = time.perf_counter()
            if is_threading:
                func(*args)
            else:
                func(args[0])
            end = time.perf_counter()
            total_time += end - start

        output_time = np.append(output_time, total_time / num_of_tests)

    return output_time


if __name__ == "__main__":
    input_data = parse_cmd()
    x_axis = np.array(input_data["thread_count"])
    y_axis_threading = check_time(parallel_merge_sort, input_data, True)
    y_axis_recursive = check_time(recursive_merge_sort, input_data, False)

    plt.title(
        label=f"size: {input_data['arr_size']}, threads: {input_data['thread_count']}, multiprocess: {input_data['multiprocess']}"
    )
    plt.plot(x_axis, y_axis_threading, color="g", label="thread")
    plt.plot(x_axis, y_axis_recursive, color="b", label="recursive")
    plt.ylabel("time, sec")
    plt.xlabel("threads")
    plt.legend()
    plt.savefig(input_data["output_file"])
    plt.show()
