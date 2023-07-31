from typing import List
from graphics.graphic_component import GraphicComponent
from graphics.renderer import Renderer
from maths.colors import RED
from maths.vertex import Vertex2f


class Button(GraphicComponent):
    position: Vertex2f
    bounds: Vertex2f

    def __init__(self, position: Vertex2f, bounds: Vertex2f) -> None:
        super().__init__()
        self.position = position
        self.bounds = bounds

    def render(self, renderer: Renderer) -> None:
        renderer.draw_rect(self.position, self.position.translated(self.bounds), RED)

    def on_mouse_click(self, x: float, y: float) -> bool:
        if (
            self.position.x <= x <= self.position.x + self.bounds.x
            and self.position.y <= y <= self.position.y + self.bounds.y
        ):
            print("Button clicked")
            return True
        return False


class CurrentInventoryGui(GraphicComponent):
    buttons: List[Button] = []

    def __init__(self) -> None:
        super().__init__()
        self.set_z_index(100)
        self.buttons.append(Button(Vertex2f(20, 20), Vertex2f(100, 100)))
        self.buttons.append(Button(Vertex2f(140, 20), Vertex2f(100, 100)))

    def render(self, renderer: Renderer) -> None:
        for button in self.buttons:
            button.render(renderer)

    def on_mouse_click(self, x: float, y: float) -> bool:
        for button in self.buttons:
            was_clicked = button.on_mouse_click(x, y)
            if was_clicked:
                return True
        return False
