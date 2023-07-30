from abc import ABC, abstractmethod
from maths.vertex import Vertex2f, Vertex3f


class Image(ABC):
    ...


class Renderer(ABC):
    @abstractmethod
    def draw_line(self, p1: Vertex2f, p2: Vertex2f, color: Vertex3f) -> None:
        raise NotImplementedError()

    @abstractmethod
    def draw_rect(self, p1: Vertex2f, p2: Vertex2f, content: Vertex3f | Image) -> None:
        raise NotImplementedError()
