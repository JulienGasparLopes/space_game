from typing import cast
from game_logic.map import Map as BaseMap
from graphics.mouse import MouseButton
from graphics.renderer_tk.renderer_tk import RendererTk
from the_factory.entities.base_belt import BaseBelt
from maths.vertex import Vertex2f
from the_factory.maps.build_helper import BuildHelper
from the_factory.maps.factory_edit_helper import FactoryEditHelper


class Map(BaseMap):
    _build_helper: BuildHelper
    _factory_edit_helper: FactoryEditHelper

    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self._build_helper = BuildHelper(self)
        self._factory_edit_helper = FactoryEditHelper()

    def render(self, renderer: RendererTk) -> None:
        super().render(renderer)
        self._build_helper.render(renderer)
        self._factory_edit_helper.render(renderer)

    def get_belt_at_tile_position(self, tile_position: Vertex2f) -> BaseBelt | None:
        possible_targets = [
            e
            for e in self.get_entities_at_tile(tile_position)
            if isinstance(e, BaseBelt)
        ]
        if len(possible_targets) == 1:
            return cast(BaseBelt, possible_targets[0])
        return None

    def on_mouse_click(self, position: Vertex2f, mouse_button: MouseButton) -> bool:
        self._build_helper.on_mouse_click(position, mouse_button)
        if mouse_button == MouseButton.RIGHT:
            if entities := self.get_entities_at_position(position):
                self._factory_edit_helper.edit_entity(entities[0], position)
                return True

        self._factory_edit_helper.on_mouse_click(position, mouse_button)
        return False
