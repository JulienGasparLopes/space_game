from typing import List
from graphics.button import Button
from graphics.graphic_component import GraphicComponent
from graphics.renderer import Renderer
from maths.vertex import Vertex2f
from the_factory.context.build_object_info import BuildObjectInfo
from the_factory.context.game_context import GameContext
from the_factory.entities.belt import Belt
from the_factory.entities.delete_plot import DeletePlot
from the_factory.entities.factory import Fabricator, Transformator


class InventoryButton(Button):
    _build_object_info: BuildObjectInfo

    def __init__(
        self, position: Vertex2f, bounds: Vertex2f, build_object_info: BuildObjectInfo
    ) -> None:
        super().__init__(position, bounds)
        self._build_object_info = build_object_info

    @property
    def build_object_info(self) -> BuildObjectInfo:
        return self._build_object_info

    def action(self) -> None:
        GameContext.get().set_build_info(self._build_object_info)


BELT_BUILD_INFO = BuildObjectInfo(Belt, mono_build=False)
TRANSFORMATOR_BUILD_INFO = BuildObjectInfo(Transformator)
FABRICATOR_BUILD_INFO = BuildObjectInfo(Fabricator)
DELETE_PLOT_BUILD_INFO = BuildObjectInfo(DeletePlot)


class CurrentInventoryGui(GraphicComponent):
    buttons: List[Button] = []

    def __init__(self, position: Vertex2f = Vertex2f(0, 0), z_index: int = 0) -> None:
        super().__init__(position, z_index)
        button_size = Vertex2f(50, 50)
        gap_size = 20
        x = 20
        for build_info in [
            BELT_BUILD_INFO,
            TRANSFORMATOR_BUILD_INFO,
            FABRICATOR_BUILD_INFO,
            DELETE_PLOT_BUILD_INFO,
        ]:
            self.buttons.append(
                InventoryButton(Vertex2f(x, 20), button_size, build_info)
            )
            x += button_size.x + gap_size

    def render(self, renderer: Renderer) -> None:
        for button in self.buttons:
            button.render(renderer)

    def on_mouse_click(self, position: Vertex2f) -> bool:
        for button in self.buttons:
            was_clicked = button.on_mouse_click(position)
            if was_clicked:
                return True
        return False
