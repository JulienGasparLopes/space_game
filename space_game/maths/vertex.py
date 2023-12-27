from dataclasses import dataclass


@dataclass
class Vertex2f:
    _x: float
    _y: float

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vertex2f):
            return self._x == other._x and self._y == other._y
        return False

    def __hash__(self) -> int:
        return hash((self._x, self._y))

    def clone(self) -> "Vertex2f":
        return Vertex2f(self._x, self._y)

    def translated(self, v: "Vertex2f") -> "Vertex2f":
        return Vertex2f(self._x + v._x, self._y + v._y)

    def multiplied(self, mult: float) -> "Vertex2f":
        return Vertex2f(self._x * mult, self._y * mult)

    def divided(self, div: float, floor: bool = False) -> "Vertex2f":
        if floor:
            return Vertex2f(self._x // div, self._y // div)
        return Vertex2f(self._x / div, self._y / div)

    def inverted(self) -> "Vertex2f":
        return Vertex2f(-self._x, -self._y)

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def norm(self) -> float:
        return (self._x**2 + self._y**2) ** 0.5


@dataclass
class Vertex3f:
    x: float
    y: float
    z: float

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vertex3f):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def clone(self) -> "Vertex3f":
        return Vertex3f(self.x, self.y, self.z)

    def translated(self, v: "Vertex3f") -> "Vertex3f":
        return Vertex3f(self.x + v.x, self.y + v.y, self.z + v.z)

    def multiplied(self, mult: float) -> "Vertex3f":
        return Vertex3f(self.x * mult, self.y * mult, self.z * mult)
