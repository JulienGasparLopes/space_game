from dataclasses import dataclass
from graphics.keyboard_tk import Keyboard
from graphics.renderer import Renderer, Image as BaseImage
import tkinter as tk
from PIL import Image as PilImage, ImageTk
from tkinter import Canvas

from maths.vertex import Vertex2f, Vertex3f
from typing import Callable, List

from space_game.game_logic.tile import TILE_SIZE


def _v3f_to_hex(color: Vertex3f) -> str:
    return "#{:02x}{:02x}{:02x}".format(color.x, color.y, color.z)


class Image(BaseImage):
    tk_image: ImageTk
    image: ImageTk.PhotoImage | None = None

    def __init__(self, path: str, rotation_angle: int | None = None) -> None:
        self.tk_image = PilImage.open(path).resize((TILE_SIZE, TILE_SIZE))
        if rotation_angle:
            self.tk_image = self.tk_image.rotate(rotation_angle)

    def render(self, canvas: Canvas, position: Vertex2f) -> None:
        if not self.image:
            self.image = ImageTk.PhotoImage(self.tk_image)
        canvas.create_image(position.x, position.y, image=self.image, anchor="nw")


@dataclass
class _RenderInfo:
    p1: Vertex2f
    p2: Vertex2f
    content: Image | Vertex2f
    z_index: int
    is_line: bool


MouseClickCallback = Callable[[float, float], None]
KeyPressedCallback = Callable[[str, bool], None]
KeyRealseCallback = Callable[[str], None]


class RendererTk(Renderer):
    _update_callback: Callable[[float], bool]

    _handle_mouse_click: MouseClickCallback | None
    _keyboard: Keyboard

    _render_info_list: List[_RenderInfo] = []

    FPS = 50

    def __init__(self) -> None:
        self.window = tk.Tk()
        self.canvas = tk.Canvas(
            self.window, width=900, height=600, highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.__handle_mouse_click)
        self._keyboard = Keyboard(self)
        self.window.bind("<KeyPress>", self._keyboard._key_press)
        self.window.bind("<KeyRelease>", self._keyboard._key_release)

    def set_background_color(self, color: Vertex3f) -> None:
        self.window.configure(bg=_v3f_to_hex(color))

    def set_button_click_callback(self, callback: MouseClickCallback) -> None:
        self._handle_mouse_click = callback

    def set_key_press_callback(self, callback: KeyPressedCallback) -> None:
        self._handle_key_press = callback

    def set_key_release_callback(self, callback: Callable[[str], None]) -> None:
        self._handle_key_release = callback

    def render_start(self) -> None:
        self._render_info_list = []

    def render_end(self) -> None:
        self._render_info_list.sort(key=lambda ri: ri.z_index)
        for ri in self._render_info_list:
            if ri.is_line:
                self.canvas.create_line(
                    ri.p1.x,
                    ri.p1.y,
                    ri.p2.x,
                    ri.p2.y,
                    fill=_v3f_to_hex(ri.content),
                    width=2,
                )
            else:
                if type(ri.content) == Vertex3f:
                    points = [
                        ri.p1.x,
                        ri.p1.y,
                        ri.p1.x,
                        ri.p2.y,
                        ri.p2.x,
                        ri.p2.y,
                        ri.p2.x,
                        ri.p1.y,
                    ]
                    self.canvas.create_polygon(points, fill=_v3f_to_hex(ri.content))
                else:
                    ri.content.render(self.canvas, ri.p1)

    def draw_line(
        self, p1: Vertex2f, p2: Vertex2f, content: Vertex3f, z_index: int = 0
    ) -> None:
        p1_t = p1.translated(self.offset)
        p2_t = p2.translated(self.offset)
        self._render_info_list.append(
            _RenderInfo(p1_t, p2_t, content, self.z_index + z_index, True)
        )

    def draw_rect(
        self, p1: Vertex2f, p2: Vertex2f, content: Vertex3f | Image, z_index: int = 0
    ) -> None:
        p1_t = p1.translated(self.offset)
        p2_t = p2.translated(self.offset)
        self._render_info_list.append(
            _RenderInfo(p1_t, p2_t, content, self.z_index + z_index, False)
        )

    def _internal_loop(self) -> None:
        self.canvas.delete("all")
        should_destroy_window = self._update_callback(1000 // self.FPS)
        self.canvas.update()
        if not should_destroy_window:
            self.window.after(1000 // self.FPS, self._internal_loop)
        else:
            self.window.destroy()

    def start_window(self, update_callback: Callable[[float], bool]) -> None:
        self._update_callback = update_callback
        self._internal_loop()
        self.window.mainloop()

    @property
    def keyboard(self) -> Keyboard:
        return self._keyboard

    def __handle_mouse_click(self, event) -> object:  # type: ignore[no-untyped-def]
        if not self._handle_mouse_click:
            raise Exception("Mouse click callback is not bound")
        else:
            self._handle_mouse_click(event.x, event.y)
        return {}
