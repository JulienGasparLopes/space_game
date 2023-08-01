from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from game_logic.tile import TILE_SIZE
from graphics.renderer import Image, Renderer
from maths.rectangle import Rectangle
from maths.vertex import Vertex3f, Vertex2f

if TYPE_CHECKING:
    from game_logic.map import Map


class Entity(ABC):
    content: Vertex3f | Image
    _tile_position: Vertex2f
    _position: Vertex2f
    width: int
    height: int

    def __init__(
        self, content: Vertex3f | Image, width: int = TILE_SIZE, height: int = TILE_SIZE
    ) -> None:
        self.content = content
        self.width = width
        self.height = height
        self.set_tile_position(Vertex2f(0, 0))

    def render(self, renderer: Renderer, z_index: int = 0) -> None:
        renderer.draw_rect(
            Vertex2f(self._position.x, self._position.y),
            Vertex2f(self._position.x + self.width, self._position.y + self.height),
            self.content,
            z_index,
        )

    @abstractmethod
    def update(self, delta_ms: int, map: "Map") -> None:
        ...

    def set_tile_position(self, position: Vertex2f) -> None:
        self._tile_position = position.clone()
        self._position = position.multiplied(TILE_SIZE)

    def set_position(
        self,
        position: Vertex2f,
        is_center_position: bool = False,
        bound_to_tile: bool = False,
    ) -> None:
        new_position = self.position
        new_tile_position = self.tile_position
        if bound_to_tile:
            if is_center_position:
                new_tile_position = position.translated(
                    Vertex2f(
                        -(self.width - TILE_SIZE) / 2, -(self.height - TILE_SIZE) / 2
                    )
                ).divided(TILE_SIZE, floor=True)
            else:
                new_tile_position = position.divided(TILE_SIZE, floor=True)
            new_position = new_tile_position.multiplied(TILE_SIZE)
        else:
            if is_center_position:
                new_position = position.translated(
                    Vertex2f(-self.width / 2, -self.height / 2)
                )
            else:
                new_position = position.clone()
            new_tile_position = new_position.divided(TILE_SIZE, floor=True)

        self._position = new_position
        self._tile_position = new_tile_position

    def collides(self, entity: "Entity") -> bool:
        return self.rectangle.collides(entity.rectangle)

    @property
    def tile_position(self) -> Vertex2f:
        return self._tile_position.clone()

    @property
    def position(self) -> Vertex2f:
        return self._position.clone()

    @property
    def rectangle(self) -> Rectangle:
        return Rectangle(self.position, Vertex2f(self.width, self.height))
