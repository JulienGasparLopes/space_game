import time
from graphics.renderer_tk import RendererTk
from maths.vertex import Vertex2f
from maths.colors import RED, WHITE, BLACK
from game_logic.map import Map, TILE_SIZE
from game_logic.tile import WALL, GROUND


class GameManager:
    def __init__(self) -> None:
        self.running = True
        self.renderer = RendererTk()
        self.renderer.set_background_color(WHITE)
        self.renderer.set_button_click_callback(self._on_mouse_click)

        self.map = Map(12, 12)
        self.map.terrain[2][4] = WALL

    def start(self) -> None:
        self.renderer.start_window(self._internal_loop)

    def _internal_loop(self, delta_ms: float) -> None:
        self.map.render(self.renderer)

    def _on_mouse_click(self, x: float, y: float) -> None:
        tile_x = x // TILE_SIZE
        tile_y = y // TILE_SIZE

        self.map.terrain[tile_x][tile_y] = (
            WALL if self.map.terrain[tile_x][tile_y] == GROUND else GROUND
        )
        self.map._update_rooms()
