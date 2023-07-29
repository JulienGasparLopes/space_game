from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from game_logic.tile import TILE_SIZE
from graphics.renderer import Image, Renderer
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

    def render(self, renderer: Renderer) -> None:
        renderer.draw_rect(
            Vertex2f(self._position.x, self._position.y),
            Vertex2f(self._position.x + self.width, self._position.y + self.height),
            self.content,
        )

    @abstractmethod
    def update(self, delta_ms: int, map: "Map") -> None:
        ...

    def set_tile_position(self, position: Vertex2f) -> None:
        self._tile_position = position.clone()
        self._position = position.multiplied(TILE_SIZE)

    def set_position(
        self, position: Vertex2f, is_center_position: bool = False
    ) -> None:
        if is_center_position:
            self._position = Vertex2f(
                position.x - self.width / 2, position.y - self.height / 2
            )
        else:
            self._position = position.clone()

        self._tile_position = Vertex2f(
            self._position.x // TILE_SIZE, self._position.y // TILE_SIZE
        )

    @property
    def tile_position(self) -> Vertex2f:
        return self._tile_position.clone()

    @property
    def position(self) -> Vertex2f:
        return self._position.clone()
