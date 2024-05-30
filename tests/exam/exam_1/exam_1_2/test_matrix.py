import hypothesis.strategies as st
import pytest
from hypothesis import given, settings

from src.exam.exam_1.exam_1_2.matrix import IntMatrix, Matrix, MatrixError, MatrixOperationError


def matrix_strategy(rows, columns):
    elements = st.lists(st.lists(st.integers(), min_size=columns, max_size=columns), min_size=rows, max_size=rows)
    return st.builds(Matrix, elements)


class TestPropertyMatrix:
    @settings(max_examples=100)
    @given(matrix=matrix_strategy(10, 10))
    def test_transpose(self, matrix):
        assert matrix == matrix.transpose().transpose()

    @settings(max_examples=100)
    @given(first_matrix=matrix_strategy(10, 20), second_matrix=matrix_strategy(10, 20))
    def test_add(self, first_matrix, second_matrix):
        assert first_matrix + second_matrix == second_matrix + first_matrix

    @settings(max_examples=100)
    @given(first_matrix=matrix_strategy(10, 20), second_matrix=matrix_strategy(10, 20))
    def test_adamar_product(self, first_matrix, second_matrix):
        assert first_matrix.adamar_product(second_matrix) == second_matrix.adamar_product(first_matrix)

    @settings(max_examples=50)
    @given(
        first_matrix=matrix_strategy(10, 10),
        second_matrix=matrix_strategy(10, 5),
        third_matrix=matrix_strategy(10, 5),
    )
    def test_multiple_disctributive(self, first_matrix, second_matrix, third_matrix):
        assert (first_matrix * second_matrix) + (first_matrix * third_matrix) == first_matrix * (
            second_matrix + third_matrix
        )

    @settings(max_examples=50)
    @given(
        first_matrix=matrix_strategy(10, 10),
        second_matrix=matrix_strategy(10, 5),
        third_matrix=matrix_strategy(5, 1),
    )
    def test_multiple_associative(self, first_matrix, second_matrix, third_matrix):
        assert (first_matrix * second_matrix) * third_matrix == first_matrix * (second_matrix * third_matrix)


class TestUnitMatrix:
    def test_build_error(self):
        with pytest.raises(MatrixError):
            Matrix([[1, 0], [0]])

    @pytest.mark.parametrize(
        "elements, expected", [([[1, 2, 3]], [[1], [2], [3]]), ([[1, 2, 3], [3, 5, 6]], [[3, 1], [5, 2], [6, 3]])]
    )
    def test_transpose(self, elements, expected):
        matrix = Matrix(elements)
        assert matrix == matrix.transpose().transpose()

    @pytest.mark.parametrize(
        "elements_1, elements_2, expected",
        [
            ([[1, 2, 3]], [[1, 6, 3]], [[2, 8, 6]]),
            ([[1, 2, 3], [3, 5, 6]], [[3, 1, 7], [5, 6, 2]], [[4, 3, 10], [8, 11, 8]]),
        ],
    )
    def test_add(self, elements_1, elements_2, expected):
        first_matrix = Matrix(elements_1)
        second_matrix = Matrix(elements_2)
        output = first_matrix + second_matrix
        assert output.elements == expected

    def test_add_err(self):
        with pytest.raises(MatrixOperationError):
            first_matrix = Matrix([[0], [0]])
            second_matrix = Matrix([[12, 6]])
            first_matrix + second_matrix

    @pytest.mark.parametrize(
        "elements_1, elements_2, expected",
        [
            ([[1, 2, 3]], [[1, 6, 3]], [[0, -4, 0]]),
            ([[1, 2, 3], [3, 5, 6]], [[3, 1, 7], [5, 6, 2]], [[-2, 1, -4], [-2, -1, 4]]),
        ],
    )
    def test_sub(self, elements_1, elements_2, expected):
        first_matrix = Matrix(elements_1)
        second_matrix = Matrix(elements_2)
        output = first_matrix - second_matrix
        assert output.elements == expected

    def test_sub_err(self):
        with pytest.raises(MatrixOperationError):
            first_matrix = Matrix([[0], [0]])
            second_matrix = Matrix([[12, 6]])
            first_matrix - second_matrix

    @pytest.mark.parametrize(
        "elements_1, elements_2, expected",
        [
            ([[1, 2, 3]], [[1, 6, 3]], [[1, 12, 9]]),
            ([[1, 2, 3], [3, 5, 6]], [[3, 1, 7], [5, 6, 2]], [[3, 2, 21], [15, 30, 12]]),
        ],
    )
    def test_adamar_product(self, elements_1, elements_2, expected):
        first_matrix = Matrix(elements_1)
        second_matrix = Matrix(elements_2)
        output = first_matrix.adamar_product(second_matrix)
        assert output.elements == expected

    def test_adamar_err(self):
        with pytest.raises(MatrixOperationError):
            first_matrix = Matrix([[0], [0]])
            second_matrix = Matrix([[12, 6]])
            first_matrix.adamar_product(second_matrix)

    @pytest.mark.parametrize(
        "elements_1, elements_2, expected",
        [
            ([[2, 5, 1], [0, 2, 5]], [[3], [3], [4]], [[25], [26]]),
            ([[2], [0], [1], [0], [3]], [[3, 1, 0]], [[6, 2, 0], [0, 0, 0], [3, 1, 0], [0, 0, 0], [9, 3, 0]]),
        ],
    )
    def test_multiple(self, elements_1, elements_2, expected):
        first_matrix = Matrix(elements_1)
        second_matrix = Matrix(elements_2)
        output = first_matrix * second_matrix
        assert output.elements == expected

    def test_multiple_err(self):
        with pytest.raises(MatrixOperationError):
            first_matrix = Matrix([[0, 4], [0, 9]])
            second_matrix = Matrix([[12, 6]])
            output = first_matrix * second_matrix


class TestIntMatrix:
    @pytest.mark.parametrize(
        "elements, expected", [([[2, 5, 1], [0, 2, 5], [1, 1, 1]], False), ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], True)]
    )
    def test_is_identity(self, elements, expected):
        matrix = IntMatrix(elements)
        assert matrix.check_if_identity() == expected

    def test_if_identity_err(self):
        with pytest.raises(MatrixError):
            matrix = IntMatrix([[1, 0], [0, 1], [1, 1]])
            matrix.check_if_identity()

    @pytest.mark.parametrize(
        "elements, expected",
        [
            ([[2, 5, 1], [0, 2, 5], [1, 1, 1]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
            ([[1, 2], [0, 1], [0, 0]], [[0, 0], [0, 0], [0, 0]]),
        ],
    )
    def test_zeroise(self, elements, expected):
        matrix = IntMatrix(elements)
        assert matrix.zeroise() == IntMatrix(expected)
