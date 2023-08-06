from abc import ABC, abstractmethod
from graphics.graphic_component import GraphicComponent
from graphics.mouse import MouseButton
from graphics.renderer import Renderer
from maths.colors import RED
from maths.vertex import Vertex2f


class Button(GraphicComponent, ABC):
    bounds: Vertex2f

    def __init__(self, position: Vertex2f, bounds: Vertex2f, z_index: int = 0) -> None:
        super().__init__(position, z_index)
        self.bounds = bounds

    def render(self, renderer: Renderer) -> None:
        renderer.draw_rect(
            self.position,
            self.position.translated(self.bounds),
            RED,
            z_index=self.z_index,
        )

    def on_mouse_click(self, position: Vertex2f, mouse_button: MouseButton) -> bool:
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
