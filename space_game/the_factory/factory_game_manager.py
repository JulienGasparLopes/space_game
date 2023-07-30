from game_logic.game_manager import GameManager
from graphics.renderer_tk import RendererTk
from maths.vertex import Vertex2f
from the_factory.factory_map import Map
from the_factory.factory_tile import GROUND


class FactoryGameManager(GameManager):
    renderer: RendererTk

    _camera_direction: Vertex2f = Vertex2f(0, 0)

    def __init__(self) -> None:
        super().__init__()

        map = Map(40, 25)
        for x in range(map.width):
            for y in range(map.height):
                map.terrain[x][y] = GROUND

        self.set_current_map(map)

    def update(self, delta_ms: int) -> None:
        ratio = 20
        offset = Vertex2f(0, 0)
        if self.renderer.keyboard.is_pressed("z"):
            offset = offset.translated(Vertex2f(0, ratio))
        if self.renderer.keyboard.is_pressed("q"):
            offset = offset.translated(Vertex2f(ratio, 0))
        if self.renderer.keyboard.is_pressed("s"):
            offset = offset.translated(Vertex2f(0, -ratio))
        if self.renderer.keyboard.is_pressed("d"):
            offset = offset.translated(Vertex2f(-ratio, 0))
        self._camera_direction = offset

        self.renderer.set_offset(
            self.renderer.offset.translated(self._camera_direction)
        )

    def on_mouse_click(self, x: float, y: float) -> None:
        ...
