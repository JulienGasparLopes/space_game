from dataclasses import dataclass
from typing import Any


@dataclass
class Vertex2f:
    x: float
    y: float

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Vertex2f):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def clone(self) -> "Vertex2f":
        return Vertex2f(self.x, self.y)

    def translated(self, v: "Vertex2f") -> "Vertex2f":
        return Vertex2f(self.x + v.x, self.y + v.y)

    def multiplied(self, mult: float) -> "Vertex2f":
        return Vertex2f(self.x * mult, self.y * mult)


@dataclass
class Vertex3f:
    x: float
    y: float
    z: float
