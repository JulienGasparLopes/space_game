from maths.vertex import Vertex2f
from graphics.graphic_component import GraphicComponent


class Mouse:
    _position: Vertex2f

    _drag_origin: Vertex2f | None = None

    def __init__(self) -> None:
        self._position = Vertex2f(0, 0)

    def _mouse_move(self, event) -> None:  # type: ignore[no-untyped-def]
        self._position = Vertex2f(event.x, event.y)

    def _mouse_drag_move(self, event) -> None:  # type: ignore[no-untyped-def]
        self._position = Vertex2f(event.x, event.y)
        if self._drag_origin is None:
            self._drag_origin = Vertex2f(event.x, event.y)

    def _mouse_release(self, event) -> None:  # type: ignore[no-untyped-def]
        self._drag_origin = None

    @property
    def position(self) -> Vertex2f:
        return self._position.clone()

    @property
    def is_dragging(self) -> bool:
        return self._drag_origin is not None

    @property
    def drag_origin(self) -> Vertex2f | None:
        return self._drag_origin.clone() if self._drag_origin else None

    def get_relative_position(self, component: GraphicComponent) -> Vertex2f:
        return self._position.translated(component.position.multiplied(-1))

    def get_relative_drag_origin(self, component: GraphicComponent) -> Vertex2f | None:
        if not self._drag_origin:
            return None
        return self._drag_origin.translated(component.position.multiplied(-1))
