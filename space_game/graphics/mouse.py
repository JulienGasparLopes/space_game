from enum import Enum
from maths.vertex import Vertex2f
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from graphics.graphic_component import GraphicComponent


class MouseButton(Enum):
    LEFT = 1
    RIGHT = 2


class Mouse:
    _position: Vertex2f

    _drag_origin: Vertex2f | None = None
    _drag_mouse_button: MouseButton | None = None

    def __init__(self) -> None:
        self._position = Vertex2f(0, 0)

    def _mouse_move(self, position: Vertex2f) -> None:
        self._position = position.clone()

    def _mouse_drag_move(self, position: Vertex2f, mouse_button: MouseButton) -> None:
        self._position = position.clone()
        if self._drag_origin is None:
            self._drag_origin = position.clone()
            self._drag_button = mouse_button

    def _mouse_release(self, mouse_button: MouseButton) -> None:
        self._drag_origin = None
        self._drag_mouse_button = None

    @property
    def position(self) -> Vertex2f:
        return self._position.clone()

    @property
    def is_dragging(self) -> bool:
        return self._drag_origin is not None

    @property
    def drag_origin(self) -> Vertex2f | None:
        return self._drag_origin.clone() if self._drag_origin else None

    @property
    def drag_button(self) -> MouseButton | None:
        return self._drag_mouse_button

    def get_relative_position(self, component: "GraphicComponent") -> Vertex2f:
        return self._position.translated(component.position.multiplied(-1))

    def get_relative_drag_origin(
        self, component: "GraphicComponent"
    ) -> Vertex2f | None:
        if not self._drag_origin:
            return None
        return self._drag_origin.translated(component.position.multiplied(-1))
