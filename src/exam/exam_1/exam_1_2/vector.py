from typing import TypeVar

T = TypeVar("T")


class DimensionError(Exception):
    pass


class Vector:
    def __init__(self, coords: list[T]) -> None:
        self.coords = coords
        self.dim = len(coords)

    @staticmethod
    def scalar_product(fisrt: "Vector", second: "Vector") -> float:
        if fisrt.dim != second.dim:
            raise DimensionError(
                "It is not possible to perform a scalar product operation for vectors of different dimensions"
            )
        return sum([item[0]*item[1] for item in zip(fisrt.coords, second.coords)])

    def is_null(self) -> bool:
        return sum(self.coords) == 0

    def __add__(self, other: "Vector") -> "Vector":
        if self.dim != other.dim:
            raise DimensionError(
                "It is not possible to perform an addition operation for vectors of different dimensions"
            )
        new_coords = [item[0]+item[1] for item in zip(self.coords, other.coords)]
        return Vector(new_coords)

    def __sub__(self, other: "Vector") -> "Vector":
        if self.dim != other.dim:
            raise DimensionError(
                "It is not possible to perform an subtraction operation for vectors of different dimensions"
            )
        new_coords = [item[0] - item[1] for item in zip(self.coords, other.coords)]
        return Vector(new_coords)

    def __mul__(self, other: "Vector") -> "Vector":
        if (self.dim != 3) or (other.dim != 3):
            raise DimensionError
        x = self.coords[1] * other.coords[2] - self.coords[2] * other.coords[1]
        y = self.coords[0] * other.coords[2] - self.coords[2] * other.coords[0]
        z = self.coords[0] * other.coords[1] - self.coords[1] * other.coords[0]

        return Vector([x, y, z])

    def __eq__(self, other: "Vector") -> bool:
        return self.coords == other.coords

    def __repr__(self) -> str:
        str_coords = ""
        for coord in self.coords:
            str_coords += str(coord) + ", "
        return f"Vector dim = {self.dim} with coordinates: ({str_coords.rstrip(', ')})"


if __name__ == "__main__":
    v = Vector([1, 2, 4])
    v2 = Vector([5, 4, 3])
    print(v + v2)
    print(v2 + v)
