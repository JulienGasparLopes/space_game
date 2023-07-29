class GameContext:
    _money: int

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

    @property
    def money(self) -> int:
        return self._money


_GAME_CONTEXT: GameContext | None = None
