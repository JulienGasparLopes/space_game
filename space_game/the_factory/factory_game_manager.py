from game_logic.game_manager import GameManager
from the_factory.factory_map import Map
from the_factory.factory_tile import GROUND


class FactoryGameManager(GameManager):
    def __init__(self) -> None:
        super().__init__()

        map = Map(40, 25)
        for x in range(map.width):
            for y in range(map.height):
                map.terrain[x][y] = GROUND

        self.set_current_map(map)
