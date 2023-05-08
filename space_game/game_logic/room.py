from dataclasses import dataclass
from maths.vertex import Vertex2f
from graphics.renderer import Renderer
from game_logic.tile import TILE_SIZE
from maths.colors import GREEN


class Room:
    tile_positions: list[Vertex2f]

    def __init__(self, tile_positions: list[Vertex2f]) -> None:
        self.tile_positions = tile_positions

    def render(self, renderer: Renderer) -> None:
        for tile_position in self.tile_positions:
            renderer.draw_rect(
                Vertex2f(
                    tile_position.x * TILE_SIZE + 8, tile_position.y * TILE_SIZE + 8
                ),
                Vertex2f(
                    (tile_position.x + 1) * TILE_SIZE - 8,
                    (tile_position.y + 1) * TILE_SIZE - 8,
                ),
                GREEN,
            )
