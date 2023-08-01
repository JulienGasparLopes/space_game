from abc import ABC, abstractmethod

from graphics.renderer import Renderer
from maths.vertex import Vertex2f


class GraphicComponent(ABC):
    _z_index: int = 0
    _offset: Vertex2f = Vertex2f(0, 0)

    def set_z_index(self, z_index: int) -> None:
        self._z_index = z_index

    @property
    def z_index(self) -> int:
        return self._z_index

    def set_offset(self, offset: Vertex2f) -> None:
        self._offset = offset.clone()

    @property
    def offset(self) -> Vertex2f:
        return self._offset

    @abstractmethod
    def render(self, renderer: Renderer) -> None:
        ...

    @abstractmethod
    def on_mouse_click(self, position: Vertex2f) -> bool:
        ...
