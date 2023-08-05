from abc import ABC, abstractmethod
from graphics.mouse import MouseButton

from graphics.renderer import Renderer
from maths.vertex import Vertex2f


class GraphicComponent(ABC):
    _z_index: int = 0
    _position: Vertex2f = Vertex2f(0, 0)

    def __init__(self, position: Vertex2f = Vertex2f(0, 0), z_index: int = 0) -> None:
        self._position = position.clone()
        self._z_index = z_index
        super().__init__()

    def set_position(self, position: Vertex2f) -> None:
        self._position = position.clone()

    def set_z_index(self, z_index: int) -> None:
        self._z_index = z_index

    @property
    def position(self) -> Vertex2f:
        return self._position

    @property
    def z_index(self) -> int:
        return self._z_index

    @abstractmethod
    def render(self, renderer: Renderer) -> None:
        ...

    @abstractmethod
    def on_mouse_click(self, position: Vertex2f, mouse_button: MouseButton) -> bool:
        ...
