from maths.vertex import Vertex2f
from graphics.graphic_component import GraphicComponent


class Mouse:
    _position: Vertex2f

    def __init__(self) -> None:
        self._position = Vertex2f(0, 0)

    def _mouse_move(self, event) -> None:  # type: ignore[no-untyped-def]
        self._position = Vertex2f(event.x, event.y)

    @property
    def position(self) -> Vertex2f:
        return self._position.clone()

    def get_relative_position(self, component: GraphicComponent) -> Vertex2f:
        return self._position.translated(component.offset.multiplied(-1))
