import hypothesis.strategies as st
import pytest
from hypothesis import given, settings

from src.exam.exam_1.exam_1_2.vector import DimensionError, Vector


def int_vector_strategy(dimension: int):
    return st.builds(Vector, st.lists(st.integers(), min_size=dimension, max_size=dimension))


class TestPropertyVector:
    @settings(max_examples=100)
    @given(first=int_vector_strategy(10), second=int_vector_strategy(10))
    def test_sum(self, first, second):
        assert first + second == second + first

    @settings(max_examples=100)
    @given(first=int_vector_strategy(10), second=int_vector_strategy(10))
    def test_sub(self, first, second):
        first_result = first - second
        second_result = second - first
        assert all([item[0] == -item[1] for item in zip(first_result.coords, second_result.coords)])

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


class TestExampleVector:
    @pytest.mark.parametrize(
        "first, second, expected", [([], [], []), ([1], [3], [4]), ([3, 5, 6], [7, 3, 2], [10, 8, 8])]
    )
    def test_sum(self, first, second, expected):
        assert Vector(first) + Vector(second) == Vector(expected)

    def test_sum_exc(self):
        with pytest.raises(DimensionError):
            Vector([1, 3, 4]) + Vector([1, 2])

    @pytest.mark.parametrize(
        "first, second, expected", [([], [], []), ([1], [3], [-2]), ([3, 5, 6], [7, 3, 2], [-4, 2, 4])]
    )
    def test_sub(self, first, second, expected):
        assert Vector(first) - Vector(second) == Vector(expected)

    def test_sub_exc(self):
        with pytest.raises(DimensionError):
            Vector([1, 3, 4]) - Vector([1, 2])

    @pytest.mark.parametrize("first, second, expected", [([], [], 0), ([1], [3], 3), ([3, 5, 6], [7, 3, 2], 48)])
    def test_scalar_product(self, first, second, expected):
        assert Vector.scalar_product(Vector(first), Vector(second)) == expected

    def test_scalar_product_exc(self):
        with pytest.raises(DimensionError):
            Vector.scalar_product(Vector([1, 3, 4]), Vector([1, 2]))

    @pytest.mark.parametrize("first, second, expected", [([3, 5, 6], [7, 3, 2], [-8, 36, -26])])
    def test_vector_mul(self, first, second, expected):
        assert Vector(first) * Vector(second) == Vector(expected)

    def test_vector_mul_exc(self):
        with pytest.raises(DimensionError):
            Vector([1, 3, 4, 5]) * Vector([1, 2])

    def test_is_null(self):
        v = Vector([0, 0, 0])
        v2 = Vector([])
        assert v.is_null() == True
        assert v2.is_null() == True

    @pytest.mark.parametrize(
        "first, second, expected", [([3, 5, 6], [7, 3, 2], False), ([], [], True), ([1, 2, 6], [1, 2, 6], True)]
    )
    def test_eq(self, first, second, expected):
        assert (first == second) == expected
