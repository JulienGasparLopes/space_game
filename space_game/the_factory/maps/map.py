from typing import cast
from game_logic.map import Map as BaseMap
from graphics.mouse import MouseButton
from graphics.renderer_tk.renderer_tk import RendererTk
from the_factory.entities.belt import Belt
from maths.vertex import Vertex2f
from the_factory.maps.build_helper import BuildHelper


class Map(BaseMap):
    _build_helper: BuildHelper

    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self._build_helper = BuildHelper(self)

    def render(self, renderer: RendererTk) -> None:
        super().render(renderer)
        self._build_helper.render(renderer)

    def get_belt_at_tile_position(self, tile_position: Vertex2f) -> Belt | None:
        possible_targets = [
            e for e in self.get_entities_at_tile(tile_position) if type(e) == Belt
        ]
        if len(possible_targets) == 1:
            return cast(Belt, possible_targets[0])
        return None

    def on_mouse_click(self, position: Vertex2f, mouse_button: MouseButton) -> bool:
        self._build_helper.on_mouse_click(position, mouse_button)
        if mouse_button == MouseButton.RIGHT:
            if entities := self.get_entities_at_position(position):
                print(entities)
        return False
