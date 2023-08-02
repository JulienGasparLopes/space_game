from collections import namedtuple
from enum import Enum
from typing import cast
from game_logic.entity import Entity as BaseEntity
from game_logic.map import Map
from graphics.renderer import Image
from maths.vertex import Vertex2f, Vertex3f
from space_game.game_logic.tile import TILE_SIZE
from abc import ABC, abstractmethod

DirectionValue = namedtuple("DirectionValue", ["vertex"])


class Direction(Enum):
    NORTH = DirectionValue(vertex=Vertex2f(0, -1))
    EAST = DirectionValue(vertex=Vertex2f(1, 0))
    SOUTH = DirectionValue(vertex=Vertex2f(0, 1))
    WEST = DirectionValue(vertex=Vertex2f(-1, 0))

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
        return self.value[0]


class Entity(BaseEntity, ABC):
    _direction: Direction

    def __init__(
        self, content: Vertex3f | Image, width: int = TILE_SIZE, height: int = TILE_SIZE
    ) -> None:
        super().__init__(content, width, height)
        self._direction = Direction.NORTH

    def set_direction(self, direction: Direction) -> None:
        self._direction = direction
