from typing import List
from graphics.graphic_component import GraphicComponent
from graphics.renderer import Renderer
from maths.vertex import Vertex2f


class GraphicManager:
    _components: List[GraphicComponent]
    _renderer: Renderer

    def __init__(self, renderer: Renderer) -> None:
        self._renderer = renderer
        self._components = []

    def add_component(self, component: GraphicComponent) -> None:
        self._components.append(component)

    def remove_component(self, component: GraphicComponent) -> None:
        self._components.remove(component)

    def render(self) -> None:
        self._renderer.render_start()
        for component in self._components:
            self._renderer.set_z_index(component.z_index)
            self._renderer.set_offset(component.offset)
            component.render(self._renderer)
        self._renderer.render_end()

    def on_mouse_click(self, position: Vertex2f) -> None:
        for component in self._components:
            click_position = position.translated(component.offset.inverted())
            was_clicked = component.on_mouse_click(click_position)
            if was_clicked:
                return
