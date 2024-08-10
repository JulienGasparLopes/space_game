from game_logic.game_manager import GameManager
from the_wanderer.map import Map


class WandererGameManager(GameManager):
    current_map: Map

    def __init__(self) -> None:
        super().__init__()
        map = Map(30, 30)
        self.set_current_map(map)

    def update(self, delta_ms: int) -> None:
        ...
