from abc import ABC, abstractmethod
from graphics.graphic_manager import GraphicManager
from graphics.renderer_tk.renderer_tk import RendererTk
from graphics.renderer import Renderer
from maths.colors import WHITE
from game_logic.map import Map


class GameManager(ABC):
    renderer: Renderer
    graphic_manager: GraphicManager
    current_map: Map | None = None

    def __init__(self) -> None:
        self.renderer = RendererTk()
        self.renderer.set_background_color(WHITE)

        self.graphic_manager = GraphicManager(self.renderer)
        self.renderer.set_button_click_callback(self.graphic_manager.on_mouse_click)

    def start(self) -> None:
        self.renderer.start_window(self._internal_loop)

    def set_current_map(self, map: Map) -> None:
        if self.current_map is not None:
            self.graphic_manager.remove_component(self.current_map)
        self.current_map = map
        self.graphic_manager.add_component(map)

    def _internal_loop(self, delta_ms: int) -> None:
        self.update(delta_ms)
        if not self.current_map:
            raise RuntimeError(
                "Current map is null, did you called 'set_current_map' ?"
            )
        self.graphic_manager.render()
        self.current_map.update(delta_ms)

    @abstractmethod
    def update(self, delta_ms: int) -> None:
        ...
