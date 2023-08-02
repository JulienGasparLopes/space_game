from graphics.graphic_component import GraphicComponent
from graphics.renderer_tk.renderer_tk import RendererTk
from maths.colors import BLACK
from maths.vertex import Vertex2f
from the_factory.game_context import GameContext


class GameInfoGui(GraphicComponent):
    def __init__(self) -> None:
        super().__init__()
        self.set_z_index(100)
        self.set_offset(Vertex2f(850, 20))

    def render(self, renderer: RendererTk) -> None:
        text = "Money: " + str(GameContext.get().money)
        renderer.draw_text(Vertex2f(0, 0), text, BLACK)

    def on_mouse_click(self, position: Vertex2f) -> bool:
        return False
