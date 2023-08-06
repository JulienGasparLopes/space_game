from game_logic.game_manager import GameManager
from graphics.renderer_tk.renderer_tk import RendererTk
from maths.vertex import Vertex2f
from the_factory.context.game_context import GameContext
from the_factory.entities.factory import Fabricator, Transformator
from the_factory.factory_tile import GROUND
from the_factory.gui.current_inventory_gui import CurrentInventoryGui
from the_factory.gui.game_info_gui import GameInfoGui
from the_factory.logic.recipe import BOLT_BASIC, HEAVY_PLATE_BASIC, SHEET_BASIC
from the_factory.maps.map_test import MapTest


class FactoryGameManager(GameManager):
    renderer: RendererTk

    _camera_direction: Vertex2f = Vertex2f(0, 0)

    def __init__(self) -> None:
        super().__init__()
        self.graphic_manager.add_component(CurrentInventoryGui(Vertex2f(0, 0), 500))
        self.graphic_manager.add_component(GameInfoGui(Vertex2f(850, 20), 1000))

        map = MapTest(40, 25)
        for x in range(map.width):
            for y in range(map.height):
                map.terrain[x][y] = GROUND

        self.set_current_map(map)

        recipe_manager = GameContext.get().recipe_manager
        recipe_manager.add_recipe(Transformator, BOLT_BASIC)
        recipe_manager.add_recipe(Transformator, SHEET_BASIC)
        recipe_manager.add_recipe(Fabricator, HEAVY_PLATE_BASIC)

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

        self.current_map.set_position(
            self.current_map.position.translated(self._camera_direction)
        )

    def on_mouse_click(self, position: Vertex2f) -> None:
        ...
