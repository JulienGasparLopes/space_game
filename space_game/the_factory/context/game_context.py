from the_factory.context.build_object_info import BuildObjectInfo


class GameContext:
    _money: int
    _build_info: BuildObjectInfo | None = None

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

    def set_build_info(self, build_info: BuildObjectInfo | None = None) -> None:
        self._build_info = build_info

    @property
    def money(self) -> int:
        return self._money

    @property
    def build_info(self) -> BuildObjectInfo | None:
        return self._build_info


_GAME_CONTEXT: GameContext | None = None
