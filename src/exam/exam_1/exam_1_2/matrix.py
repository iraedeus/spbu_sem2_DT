from typing import Any, Generic, Optional, Protocol, TypeVar


class MatrixError(Exception):
    pass


class MatrixOperationError(Exception):
    pass


class ArithmeticAvailable(Protocol):
    def __add__(self, other: Any) -> Any:
        ...

    def __mul__(self, other: Any) -> Any:
        ...

    def __sub__(self, other: Any) -> Any:
        ...

    def __eq__(self, other: Any) -> bool:
        ...


T = TypeVar("T", bound=ArithmeticAvailable)


class Matrix(Generic[T]):
    def __init__(self, elements: list[list[T]]) -> None:
        self.elements = elements
        self._rows: int
        self._columns: int
        self._order: Optional[int]
        self.set_properties()

    def set_properties(self) -> None:
        self._rows = len(self.elements)

        if all([len(self.elements[0]) == len(row) for row in self.elements]):
            self._columns = len(self.elements[0])
        else:
            raise MatrixError("The number of elements in the rows does not match.")

        if self._rows == self._columns:
            self._order = self._rows
        else:
            self._order = None

    def transpose(self) -> "Matrix[T]":
        elements = self.elements
        new_elements = [[elements[j][i] for j in range(len(elements))] for i in range(len(elements[0]))]

        return Matrix(new_elements)

    def get_element(self, row: int, column: int) -> T:
        return self.elements[row][column]

    def adamar_product(self, other: object) -> "Matrix[T]":
        if not isinstance(other, Matrix):
            raise TypeError(f"It is impossible to adamar product matrix with object of type {object}.")

        if self._rows != other._rows or self._columns != other._columns:
            raise MatrixOperationError("It is impossible to adamar multiply matrices of different sizes.")

        new_matrix_elements = [
            [self.elements[i][j] * other.elements[i][j] for j in range(len(self.elements[0]))]
            for i in range(len(self.elements))
        ]

        return Matrix(new_matrix_elements)

    def __add__(self, other: object) -> "Matrix[T]":
        if not isinstance(other, Matrix):
            raise TypeError(f"It is impossible to sum matrix with object of type {object}.")

        if self._rows != other._rows or self._columns != other._columns:
            raise MatrixOperationError("It is impossible to sum matrices of different sizes.")

        new_matrix_elements = [
            [self.elements[i][j] + other.elements[i][j] for j in range(len(self.elements[0]))]
            for i in range(len(self.elements))
        ]

        return Matrix(new_matrix_elements)

    def __mul__(self, other: object) -> "Matrix[T]":
        if not isinstance(other, Matrix):
            raise TypeError(f"It is impossible to multiply matrix with object of type {object}")

        if self._columns != other._rows:
            raise MatrixOperationError(
                "It is impossible to multiply matrices in which the number of columns of the first does not match the number of rows of the second."
            )

        def scalar_product(vector_1: list[T], vector_2: list[T]) -> T:
            new_vector = [x * y for x, y in zip(vector_1, vector_2)]
            return sum(new_vector)

        other = other.transpose()
        return Matrix(
            [[scalar_product(vector_1, vector_2) for vector_2 in other.elements] for vector_1 in self.elements]
        )

    def __sub__(self, other: object) -> "Matrix":
        if not isinstance(other, Matrix):
            raise TypeError(f"It is impossible to subtract matrix with object of type {object}.")

        if self._rows != other._rows or self._columns != other._columns:
            raise MatrixOperationError("It is impossible to subtract matrices of different sizes.")

        new_matrix_elements = [
            [self.elements[i][j] - other.elements[i][j] for j in range(len(self.elements[0]))]
            for i in range(len(self.elements))
        ]

        return Matrix(new_matrix_elements)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            raise TypeError(f"It is impossible to compare matrix with object of type {object}")

        return all(
            [
                self.elements[i][j] == other.elements[i][j]
                for j in range(len(self.elements[0]))
                for i in range(len(self.elements))
            ]
        )

    def __repr__(self) -> str:
        output = ""
        for row in self.elements:
            for element in row:
                output += str(element) + " "
            output += "\n"
        return output

    @property
    def order(self) -> Optional[int]:
        return self._order


class IntMatrix(Matrix[int]):
    def __init__(self, elements: list[list[int]]) -> None:
        super().__init__(elements)

    def check_if_identity(self) -> bool:
        if self._rows != self._columns:
            raise MatrixError("The matrix must be square")

        def check(matrix: IntMatrix, row: int, column: int) -> bool:
            if (row == column) and (matrix.get_element(row, column) == 1):
                return True
            elif (row != column) and (matrix.get_element(row, column) == 0):
                return True
            else:
                return False

        return all([check(self, j, i) for j in range(self._rows) for i in range(self._columns)])

    def zeroise(self) -> "IntMatrix":
        elements = []
        for i in range(self._rows):
            row = []
            for j in range(self._columns):
                row.append(0)
            elements.append(row)

        return IntMatrix(elements)


if __name__ == "__main__":
    pass
