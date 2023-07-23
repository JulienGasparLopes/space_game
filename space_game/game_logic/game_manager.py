from abc import abstractmethod
from graphics.renderer_tk import RendererTk
from graphics.renderer import Renderer
from maths.colors import WHITE
from game_logic.map import Map


class GameManager:
    renderer: Renderer
    current_map: Map | None = None

    def __init__(self) -> None:
        self.renderer = RendererTk()
        self.renderer.set_background_color(WHITE)
        self.renderer.set_button_click_callback(self.on_mouse_click)

    def start(self) -> None:
        self.renderer.start_window(self._internal_loop)

    def set_current_map(self, map: Map) -> None:
        self.current_map = map

    def _internal_loop(self, delta_ms: int) -> None:
        if not self.current_map:
            raise RuntimeError(
                "Current map is null, did you called 'set_current_map' ?"
            )
        self.current_map.render(self.renderer)
        self.current_map.update(delta_ms)

    @abstractmethod
    def on_mouse_click(self, x: float, y: float) -> None:
        ...
