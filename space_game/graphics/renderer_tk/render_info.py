from abc import ABC, abstractmethod
from dataclasses import dataclass
from tkinter import Canvas
from graphics.renderer_tk.helpers import v3f_to_hex
from typing import TYPE_CHECKING
from maths.vertex import Vertex2f, Vertex3f

if TYPE_CHECKING:
    from graphics.renderer_tk.renderer_tk import Image


@dataclass
class RenderInfo(ABC):
    p1: Vertex2f
    p2: Vertex2f
    content: "Image | Vertex3f"
    z_index: int

    @abstractmethod
    def render(self, canvas: Canvas) -> None:
        ...


class RenderInfoLine(RenderInfo):
    def render(self, canvas: Canvas) -> None:
        canvas.create_line(
            self.p1.x,
            self.p1.y,
            self.p2.x,
            self.p2.y,
            fill=v3f_to_hex(self.content),
            width=2,
        )


class RenderInfoRect(RenderInfo):
    def render(self, canvas: Canvas) -> None:
        if isinstance(self.content, Vertex3f):
            points = [
                self.p1.x,
                self.p1.y,
                self.p1.x,
                self.p2.y,
                self.p2.x,
                self.p2.y,
                self.p2.x,
                self.p1.y,
            ]
            canvas.create_polygon(points, fill=v3f_to_hex(self.content))
        else:
            self.content.render(canvas, self.p1)


class RenderInfoText(RenderInfo):
    text: str

    def __init__(
        self, p1: Vertex2f, p2: Vertex2f, text: str, color: Vertex3f, z_index: int
    ):
        super().__init__(p1, p2, color, z_index)
        self.text = text

    def render(self, canvas: Canvas) -> None:
        canvas.create_text(
            self.p1.x, self.p1.y, text=self.text, fill=v3f_to_hex(self.content)
        )
