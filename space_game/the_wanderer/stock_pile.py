from game_logic.entity import Entity
from game_logic.tile import TILE_SIZE
from graphics.renderer import Renderer
from maths.vertex import Vertex2f, Vertex3f
from the_wanderer.task import TaskGetItemToMove
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from the_wanderer.map import Map


class StockPile(Entity):
    stock: int
    temporary_destination: "StockPile"

    def __init__(self) -> None:
        super().__init__(Vertex3f(0, 255, 255), TILE_SIZE, TILE_SIZE)
        self.set_position(
            Vertex2f(TILE_SIZE / 2, TILE_SIZE / 2), is_center_position=True
        )
        self.stock = 0

    def update(self, delta_ms: int, map: "Map") -> None:
        if self.stock >= 10 and self.temporary_destination:
            map.available_tasks.append(
                TaskGetItemToMove(map, self, self.temporary_destination)
            )

    def render(self, renderer: Renderer, z_index: int = 0) -> None:
        super().render(renderer, z_index)
        renderer.draw_text(self.position, str(self.stock), Vertex3f(0, 0, 0), 322)

    def put_item(self) -> bool:
        self.stock += 1
        return True

    def pop_item(self) -> bool:
        if self.stock > 0:
            self.stock -= 1
            return True
        return False
