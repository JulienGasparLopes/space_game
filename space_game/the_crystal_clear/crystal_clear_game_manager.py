from the_crystal_clear.map import Map
from game_logic.game_manager import GameManager


class WandererGameManager(GameManager):
    current_map: Map

    def __init__(self) -> None:
        super().__init__()
        map = Map(10, 10)
        self.set_current_map(map)

    def update(self, delta_ms: int) -> None:
        ...
