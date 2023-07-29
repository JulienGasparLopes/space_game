from dataclasses import dataclass


@dataclass
class Vertex2f:
    x: float
    y: float

    def __eq__(self, other: object) -> bool:
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
