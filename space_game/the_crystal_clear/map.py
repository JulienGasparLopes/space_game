from game_logic.map import Map as MapBase
from game_logic.tile import Tile
from graphics.mouse import MouseButton
from maths.vertex import Vertex2f, Vertex3f

GROUND = Tile(Vertex3f(0, 255, 0), False)
WALL = Tile(Vertex3f(0, 0, 255), True)


class Map(MapBase):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self._init_10_10_terrain()

    def on_mouse_click(self, position: Vertex2f, mouse_button: MouseButton) -> bool:
        return True

    def _init_10_10_terrain(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                self.terrain[x][y] = GROUND
