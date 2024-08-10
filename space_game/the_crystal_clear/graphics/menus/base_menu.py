from graphics.graphic_component import GraphicComponent


class Menu:
    components: list[GraphicComponent]

    def render(self) -> None:
        for component in self.components:
            component.render()
