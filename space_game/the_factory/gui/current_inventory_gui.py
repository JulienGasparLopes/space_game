from typing import List
from game_logic.entity import Entity
from graphics.button import Button
from graphics.graphic_component import GraphicComponent
from graphics.renderer import Renderer
from maths.vertex import Vertex2f
from the_factory.context.game_context import GameContext
from the_factory.entities.belt import Belt
from the_factory.entities.delete_plot import DeletePlot
from the_factory.entities.factory import Fabricator, Transformator


class InventoryButton(Button):
    _entity_type: type[Entity]

    def __init__(
        self, position: Vertex2f, bounds: Vertex2f, entity_type: type[Entity]
    ) -> None:
        super().__init__(position, bounds)
        self._entity_type = entity_type

    def action(self) -> None:
        GameContext.get().select_build_entity_type(self._entity_type)


class CurrentInventoryGui(GraphicComponent):
    buttons: List[Button] = []

    def __init__(self, position: Vertex2f = Vertex2f(0, 0), z_index: int = 0) -> None:
        super().__init__(position, z_index)
        button_size = Vertex2f(50, 50)
        gap_size = 20
        x = 20
        for entity_type in [Belt, Transformator, Fabricator, DeletePlot]:
            self.buttons.append(
                InventoryButton(Vertex2f(x, 20), button_size, entity_type)
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
