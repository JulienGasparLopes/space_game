from enum import Enum
from typing import NamedTuple
from game_logic.entity import Entity as BaseEntity
from graphics.renderer import Image
from maths.vertex import Vertex2f, Vertex3f

DirectionValue = NamedTuple("DirectionValue", [("vertex", Vertex2f)])


class Direction(Enum):
    NORTH = DirectionValue(Vertex2f(0, -1))
    EAST = DirectionValue(Vertex2f(1, 0))
    SOUTH = DirectionValue(Vertex2f(0, 1))
    WEST = DirectionValue(Vertex2f(-1, 0))

    @property
    def opposite(self) -> "Direction":
        return {
            Direction.NORTH: Direction.SOUTH,
            Direction.EAST: Direction.WEST,
            Direction.SOUTH: Direction.NORTH,
            Direction.WEST: Direction.EAST,
        }.get(
            self, Direction.NORTH
        )  # Default only for typing

    @property
    def vertex(self) -> Vertex2f:
        return self.value.vertex


class Entity(BaseEntity):
    _direction: Direction

    def __init__(
        self, content: Vertex3f | Image, width: int = 1, height: int = 1
    ) -> None:
        super().__init__(content, width, height)
        self._direction = Direction.NORTH
