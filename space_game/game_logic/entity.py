from dataclasses import dataclass
from graphics.renderer import Renderer
from maths.vertex import Vertex3f, Vertex2f
from game_logic.map import TILE_SIZE


class Entity:
    color: Vertex3f
    tile_position: Vertex2f

    def __init__(self, color: Vertex3f) -> None:
        self.color = color
        self.tile_position = Vertex2f(0, 0)

    def render(self, renderer: Renderer) -> None:
        renderer.draw_rect(
            Vertex2f(
                self.tile_position.x * TILE_SIZE + 4,
                self.tile_position.y * TILE_SIZE + 4,
            ),
            Vertex2f(
                (self.tile_position.x + 1) * TILE_SIZE - 4,
                (self.tile_position.y + 1) * TILE_SIZE - 4,
            ),
            self.color,
        )
