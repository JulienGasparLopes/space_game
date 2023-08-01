from typing import List
from maths.vertex import Vertex2f


class Rectangle:
    _p1: Vertex2f
    _p2: Vertex2f
    _bounds = Vertex2f

    def __init__(self, position: Vertex2f, bounds: Vertex2f) -> None:
        self._p1 = position.clone()
        self._p2 = position.translated(bounds)
        self._bounds = bounds

    @staticmethod
    def from_points(p1: Vertex2f, p2: Vertex2f) -> "Rectangle":
        return Rectangle(p1, p2.translated(p1.inverted()))

    def get_all_points(self) -> List[Vertex2f]:
        return [
            self._p1.clone(),
            self._p1.translated(Vertex2f(self._bounds.x, 0)),
            self._p2.clone(),
            self._p1.translated(Vertex2f(0, self._bounds.y)),
        ]

    def contains(self, point: Vertex2f, strict: bool = True) -> bool:
        if strict:
            return (
                self._p1.x <= point.x <= self._p2.x
                and self._p1.y <= point.y <= self._p2.y
            )
        return self._p1.x < point.x < self._p2.x and self._p1.y < point.y < self._p2.y

    def collides(self, rectangle: "Rectangle") -> bool:
        collides = False
        for point in self.get_all_points():
            collides = collides or rectangle.contains(point)
        for point in rectangle.get_all_points():
            collides = collides or self.contains(point)
        return collides
