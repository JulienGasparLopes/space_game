from abc import ABC, abstractmethod
from maths.vertex import Vertex2f, Vertex3f


class Image(ABC):
    ...


class Renderer(ABC):
    _current_z_index: int = 0
    _current_offset: Vertex2f = Vertex2f(0, 0)

    @abstractmethod
    def render_start(self) -> None:
        ...

    @abstractmethod
    def render_end(self) -> None:
        ...

    @abstractmethod
    def draw_line(
        self, p1: Vertex2f, p2: Vertex2f, color: Vertex3f, z_index: int = 0
    ) -> None:
        ...

    @abstractmethod
    def draw_rect(
        self, p1: Vertex2f, p2: Vertex2f, content: Vertex3f | Image, z_index: int = 0
    ) -> None:
        ...

    @abstractmethod
    def draw_text(
        self, p: Vertex2f, text: str, color: Vertex3f, z_index: int = 0
    ) -> None:
        ...

    @property
    def z_index(self) -> int:
        return self._current_z_index

    def set_z_index(self, z_index: int) -> None:
        self._current_z_index = z_index

    @property
    def offset(self) -> Vertex2f:
        return self._current_offset.clone()

    def set_offset(self, offset: Vertex2f | None) -> None:
        self._current_offset = offset or Vertex2f(0, 0)
