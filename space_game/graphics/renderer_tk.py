from graphics.renderer import Renderer
import tkinter as tk

from maths.vertex import Vertex2f, Vertex3f
from typing import Callable


def _v3f_to_hex(color: Vertex3f) -> str:
    return "#{:02x}{:02x}{:02x}".format(color.x, color.y, color.z)


class RendererTk(Renderer):
    _update_callback: Callable[[float], bool]
    _handle_mouse_click: Callable[[float, float], None] | None

    def __init__(self) -> None:
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=400, height=400)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.__handle_mouse_click)

    def set_background_color(self, color: Vertex3f) -> None:
        self.window.configure(bg=_v3f_to_hex(color))

    def set_button_click_callback(
        self, callback: Callable[[float, float], None]
    ) -> None:
        self._handle_mouse_click = callback

    def draw_line(self, p1: Vertex2f, p2: Vertex2f, color: Vertex3f) -> None:
        self.canvas.create_line(
            p1.x, p1.y, p2.x, p2.y, fill=_v3f_to_hex(color), width=2
        )

    def draw_rect(self, p1: Vertex2f, p2: Vertex2f, color: Vertex3f) -> None:
        points = [p1.x, p1.y, p1.x, p2.y, p2.x, p2.y, p2.x, p1.y]
        self.canvas.create_polygon(points, fill=_v3f_to_hex(color))

    def _internal_loop(self) -> None:
        self.canvas.delete("all")
        should_destroy_window = self._update_callback(20)
        self.canvas.update()
        if not should_destroy_window:
            self.window.after(20, self._internal_loop)
        else:
            self.window.destroy()

    def start_window(self, update_callback: Callable[[float], bool]) -> None:
        self._update_callback = update_callback
        self._internal_loop()
        self.window.mainloop()

    def __handle_mouse_click(self, event) -> object:  # type: ignore[no-untyped-def]
        if self._handle_mouse_click:
            self._handle_mouse_click(event.x, event.y)
        return {}
