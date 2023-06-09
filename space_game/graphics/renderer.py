from abc import abstractmethod
from maths.vertex import Vertex2f, Vertex3f


class Renderer:
    @abstractmethod
    def draw_rect(self, p1: Vertex2f, p2: Vertex2f, color: Vertex3f) -> None:
        raise NotImplementedError()

    @abstractmethod
    def draw_line(self, p1: Vertex2f, p2: Vertex2f, color: Vertex3f) -> None:
        raise NotImplementedError()
