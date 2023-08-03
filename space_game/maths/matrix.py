from typing import Generic, List, TypeVar

from maths.vertex import Vertex2f

T = TypeVar("T")


class Matrix(Generic[T]):
    _values: List[List[T]]

    @staticmethod
    def from_size(width: int, height: int, initial_value: T) -> "Matrix[T]":
        values: List[List[T]] = []
        for y in range(height):
            values.append([])
            for x in range(width):
                values[y].append(initial_value)
        return Matrix(values)

    def __init__(self, initial_value: List[List[T]]) -> None:
        super().__init__()
        self._values = initial_value

    def get(self, position: Vertex2f) -> T:
        return self._values[position.y][position.x]

    def set(self, position: Vertex2f, value: T) -> None:
        self._values[position.y][position.x] = value

    def get_size(self) -> tuple[int, int]:
        if len(self._values) == 0:
            return 0, 0
        return len(self._values[0]), len(self._values)

    def rotate(self, clockwise: bool = True) -> None:
        width, height = self.get_size()
        new_values: List[List[T]] = []
        if clockwise:
            for x in range(width):
                new_values.append([])
            for x in range(width):
                for y in range(height):
                    new_values[x].append(self._values[height - y - 1][x])
            self._values = new_values
        else:
            for x in range(width):
                new_values.append([])
            for x in range(width):
                for y in range(height):
                    new_values[width - x - 1].append(self._values[y][x])
            self._values = new_values

    def flip(self) -> None:
        # TODO: Implement flip vertically
        new_values: List[List[T]] = []
        for y in range(len(self._values)):
            new_values.append([])
            for x in range(len(self._values[0])):
                new_values[y].append(self._values[y][len(self._values[0]) - x - 1])
        self._values = new_values

    def get_entries(self) -> List[tuple[T, Vertex2f]]:
        values: List[tuple[T, Vertex2f]] = []
        for y in range(len(self._values)):
            for x in range(len(self._values[0])):
                values.append((self._values[y][x], Vertex2f(x, y)))
        return values

    def __str__(self) -> str:
        repr = ""
        for y in range(len(self._values)):
            for x in range(len(self._values[0])):
                repr += f"{self._values[y][x]} "
            repr += "\n"
        return repr
