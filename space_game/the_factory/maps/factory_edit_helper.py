from game_logic.entity import Entity
from graphics.button import Button
from graphics.mouse import MouseButton
from graphics.renderer_tk.renderer_tk import RendererTk
from maths.colors import GREY, RED
from maths.rectangle import Rectangle
from maths.vertex import Vertex2f
from the_factory.context.game_context import GameContext
from the_factory.context.recipe_context import RecipeState
from the_factory.entities.factory import (
    Fabricator,
    Factory,
    MaterialChute,
    Transformator,
)
from the_factory.logic.recipe import Recipe


class OptionButton(Button):
    _entity: Factory
    _recipe: Recipe

    def __init__(self, position: Vertex2f, entity: Factory, recipe: Recipe) -> None:
        super().__init__(position, Vertex2f(40, 40), 8002)
        self._entity = entity
        self._recipe = recipe

    def action(self) -> None:
        self._entity.set_recipe(self._recipe)


class FactoryEditHelper:
    _currently_editing_entity: Entity | None = None
    _click_position: Vertex2f | None = None

    _bounds: Vertex2f | None = Vertex2f(140, 140)

    _options: list[OptionButton] = []

    def __init__(self) -> None:
        ...

    def render(self, renderer: RendererTk) -> None:
        if not self._currently_editing_entity or not self._click_position:
            return

        renderer.draw_rect(
            self._click_position,
            self._click_position.translated(self._bounds),
            GREY,
            z_index=800,
        )
        for option in self._options:
            option.render(renderer)

    def on_mouse_click(self, position: Vertex2f, mouse_button: MouseButton) -> bool:
        if self._click_position:
            if not Rectangle(self._click_position, self._bounds).contains(position):
                self.stop_editing()
                return True

        for option in self._options:
            if option.on_mouse_click(position, mouse_button):
                self.stop_editing()
                return True
        return False

    def edit_entity(self, entity: Entity, click_position: Vertex2f) -> None:
        if isinstance(entity, (MaterialChute, Transformator, Fabricator)):
            self._currently_editing_entity = entity
            self._click_position = click_position
            self._options = []
            available_recipes = GameContext.get().recipe_manager.get_recipes(
                type(entity), [RecipeState.AVAILABLE, RecipeState.LOCKED]
            )
            for i, recipe in enumerate(available_recipes):
                x = self._click_position.x + 5 + (i % 3) * 45
                y = self._click_position.y + 5 + (i // 3) * 45
                print(x, y)
                self._options.append(OptionButton(Vertex2f(x, y), entity, recipe))

    def stop_editing(self) -> None:
        self._currently_editing_entity = None
        self._click_position = None
        self._options = []
