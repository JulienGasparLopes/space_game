from enum import Enum
from typing import Dict, List
from typing import TYPE_CHECKING
from the_factory.logic.recipe import Recipe

if TYPE_CHECKING:
    from the_factory.entities.factory import Factory


class RecipeState(Enum):
    AVAILABLE = 0
    LOCKED = 1
    HIDDEN = 2


class RecipeManager:
    _all_recipes: Dict["Factory", List[tuple[Recipe, RecipeState]]]

    def __init__(self) -> None:
        self._all_recipes = {}

    def get_recipes(
        self, factory_type: type["Factory"], states: List[RecipeState] | None
    ) -> list[Recipe]:
        states = states or [RecipeState.AVAILABLE]
        recipe_info_list = (
            self._all_recipes[factory_type] if factory_type in self._all_recipes else []
        )
        return [recipe for recipe, state in recipe_info_list if state in states]

    def add_recipe(
        self,
        factory_type: type["Factory"],
        recipe: Recipe,
        state: RecipeState = RecipeState.AVAILABLE,
    ) -> None:
        if factory_type not in self._all_recipes:
            self._all_recipes[factory_type] = []

        self._all_recipes[factory_type].append((recipe, state))
