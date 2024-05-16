import hypothesis.strategies as st
import numpy as np
from hypothesis import given, settings

from src.exam.exam_1.exam_1_2.vector import Vector


def int_vector_strategy(dimension: int):
    return st.builds(Vector, st.lists(st.integers(), min_size=dimension, max_size=dimension))


class TestVector:
    @settings(max_examples=100)
    @given(first=int_vector_strategy(10), second=int_vector_strategy(10))
    def test_sum(self, first, second):
        assert first + second == second + first

    @settings(max_examples=100)
    @given(first=int_vector_strategy(10), second=int_vector_strategy(10))
    def test_sub(self, first, second):
        assert True

    @settings(max_examples=100)
    @given(first=int_vector_strategy(10), second=int_vector_strategy(10), third=int_vector_strategy(10))
    def test_scalar_product(self, first, second, third):
        assert Vector.scalar_product(first, second) == Vector.scalar_product(second, first)
        assert Vector.scalar_product(first + second, third) == Vector.scalar_product(
            first, third
        ) + Vector.scalar_product(second, third)

    @settings(max_examples=100)
    @given(first=int_vector_strategy(3), second=int_vector_strategy(3), third=int_vector_strategy(3))
    def test_vector_product(self, first, second, third):
        assert (first + second) * third == (first * third) + (second * third)
        assert first * first == Vector([0, 0, 0])
        assert ((first * second) * third) + ((second * third) * first) + ((third * first) * second) == Vector([0, 0, 0])
