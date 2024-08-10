from game_logic.game_manager import GameManager as BaseGameManager
from game_logic.tile import TILE_SIZE
from maths.vertex import Vertex2f
from the_space.space_tile import GROUND, WALL
from the_space.space_map import Map


class SpaceGameManager(BaseGameManager):
    current_map: Map

    def __init__(self) -> None:
        super().__init__()

        map = Map(12, 12)
        for x in range(map.width):
            for y in range(map.height):
                map.terrain[x][y] = GROUND

        map.terrain[2][4] = WALL

        self.set_current_map(map)

    def update(self, delta_ms: int) -> None:
        self.current_map.update(delta_ms)
