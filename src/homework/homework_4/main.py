import argparse
import random
import time

from typing import Any, Optional, Callable
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import ArrayLike
from merge_sort import *

matplotlib.use("TkAgg")


def parse_cmd() -> dict[str, Any]:
    parser = argparse.ArgumentParser(prog="Comparing threading and non-threading merge sort")
    parser.add_argument("arr_size", type=int)
    parser.add_argument("thread_count", type=int, nargs="+")
    parser.add_argument("output_file", type=str)
    parser.add_argument("--multiprocess", action="store_true")
    args = parser.parse_args()

    output = {
        "size": args.arr_size,
        "threads": args.thread_count,
        "output_fp": args.output_file,
        "multiprocess": args.multiprocess,
    }

    return output


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
    num_of_tests = 1
    size = input_data["size"]
    threads = input_data["threads"]
    for thread_cnt in threads:
        total_time = 0.0
        for j in range(num_of_tests):
            array = random.sample(range(-100000, 100000), size)
            args = [array, thread_cnt, input_data["multiprocess"]]
            total_time += evaluate_time(func, args, is_threading)

        output_time = np.append(output_time, total_time / num_of_tests)

    return output_time


if __name__ == "__main__":
    input_data = parse_cmd()
    x_axis = np.array(input_data["threads"])
    y_axis_threading = check_time(multi_merge_sort, input_data, True)
    y_axis_classic = check_time(merge_sort, input_data, False)
    y_axis_recursive = check_time(recursive_merge_sort, input_data, False)

    plt.plot(x_axis, y_axis_classic, color="r", label="iterative")
    plt.plot(x_axis, y_axis_threading, color="g", label="thread")
    plt.plot(x_axis, y_axis_recursive, color="b", label="recursive")
    plt.ylabel("time, sec")
    plt.xlabel("threads")
    plt.legend()
    plt.show()
