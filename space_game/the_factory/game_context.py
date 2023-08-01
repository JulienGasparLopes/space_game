from game_logic.entity import Entity


class GameContext:
    _money: int
    _selected_entity: Entity | None = None

    def __init__(self) -> None:
        self._money = 1050

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

    def set_select_entity(self, entity_type: Entity | None = None) -> None:
        self._selected_entity = entity_type

    @property
    def money(self) -> int:
        return self._money

    @property
    def selected_entity(self) -> Entity | None:
        return self._selected_entity


_GAME_CONTEXT: GameContext | None = None
