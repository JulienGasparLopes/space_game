from abc import ABC, abstractmethod
from typing import List
from game_logic.entity import Entity
from graphics.graphic_component import GraphicComponent
from graphics.renderer import Renderer
from maths.colors import RED
from maths.vertex import Vertex2f
from the_factory.entities.belt import Belt
from the_factory.entities.factory import Transformator
from the_factory.game_context import GameContext


class Button(GraphicComponent, ABC):
    position: Vertex2f
    bounds: Vertex2f

    def __init__(self, position: Vertex2f, bounds: Vertex2f) -> None:
        super().__init__()
        self.position = position
        self.bounds = bounds

    def render(self, renderer: Renderer) -> None:
        renderer.draw_rect(self.position, self.position.translated(self.bounds), RED)

    def on_mouse_click(self, position: Vertex2f) -> bool:
        if (
            self.position.x <= position.x <= self.position.x + self.bounds.x
            and self.position.y <= position.y <= self.position.y + self.bounds.y
        ):
            self.action()
            return True
        return False

    @abstractmethod
    def action(self) -> None:
        ...


class InventoryButton(Button):
    entity_type: type[Entity]

    def __init__(
        self, position: Vertex2f, bounds: Vertex2f, entity_type: type[Entity]
    ) -> None:
        super().__init__(position, bounds)
        self.entity_type = entity_type

    def action(self) -> None:
        GameContext.get().set_select_entity(self.entity_type())


class CurrentInventoryGui(GraphicComponent):
    buttons: List[Button] = []

    def __init__(self) -> None:
        super().__init__()
        self.set_z_index(100)
        self.buttons.append(InventoryButton(Vertex2f(20, 20), Vertex2f(50, 50), Belt))
        self.buttons.append(
            InventoryButton(Vertex2f(90, 20), Vertex2f(50, 50), Transformator)
        )

    def render(self, renderer: Renderer) -> None:
        for button in self.buttons:
            button.render(renderer)

    def on_mouse_click(self, position: Vertex2f) -> bool:
        for button in self.buttons:
            was_clicked = button.on_mouse_click(position)
            if was_clicked:
                return True
        return False
