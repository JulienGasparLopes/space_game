from game_logic.entity import Entity
from the_factory.context.recipe_context import RecipeManager


class GameContext:
    _money: int
    _selected_build_entity_type: type[Entity] | None = None

    _recipe_manager: RecipeManager

    def __init__(self) -> None:
        self._money = 1000
        self._recipe_manager = RecipeManager()

    @staticmethod
    def get() -> "GameContext":
        global _GAME_CONTEXT
        if _GAME_CONTEXT is None:
            _GAME_CONTEXT = GameContext()
        return _GAME_CONTEXT

    def money_transaction(self, amount: int) -> bool:
        if amount >= 0:
            self._money += amount
            return True
        else:
            if self._money + amount >= 0:
                self._money += amount
                return True
        return False

    def select_build_entity_type(
        self, build_entity_type: type[Entity] | None = None
    ) -> None:
        self._selected_build_entity_type = build_entity_type

    @property
    def money(self) -> int:
        return self._money

    @property
    def selected_build_entity_type(self) -> type[Entity] | None:
        return self._selected_build_entity_type

    @property
    def recipe_manager(self) -> RecipeManager:
        return self._recipe_manager


_GAME_CONTEXT: GameContext | None = None
