from game_logic.map import Map as MapBase
from game_logic.tile import Tile
from graphics.mouse import MouseButton
from maths.vertex import Vertex2f, Vertex3f
from the_wanderer.path import Path
from the_wanderer.stock_pile import StockPile
from the_wanderer.task import Task
from the_wanderer.wanderer import Wanderer

GROUND = Tile(Vertex3f(0, 255, 0), False)
WALL = Tile(Vertex3f(0, 0, 255), True)


class Map(MapBase):
    available_tasks: list[Task]

    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self.available_tasks = []

        # self._init_10_10_terrain()
        self._init_big_terrain()

    def on_mouse_click(self, position: Vertex2f, mouse_button: MouseButton) -> bool:
        return True
        # entity = self.wanderer
        # if path := self.find_path(
        #     entity.tile_position, position.divided(TILE_SIZE, floor=True)
        # ):
        #     entity.path = path
        # return True

    def find_path(self, start: Vertex2f, end: Vertex2f) -> Path | None:
        visited_positions: set[Vertex2f] = set()
        possible_paths: list[Path] = [Path([start], end)]
        while possible_paths:
            possible_paths.sort(key=lambda path: path.distance * path.distance)
            current_path = possible_paths.pop(0)
            if current_path.end == end:
                return current_path
            for neighbour in current_path.get_neighbours():
                if neighbour.end not in visited_positions:
                    tile = self._get_tile(neighbour.end)
                    if tile and not tile.is_wall:
                        visited_positions.add(neighbour.end)
                        possible_paths.append(neighbour)

        return None

    def _init_big_terrain(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                self.terrain[x][y] = GROUND

        sp1 = StockPile()
        sp1.set_tile_position(Vertex2f(3, 4))
        sp1.stock = 10
        self.entities.append(sp1)

        sp2 = StockPile()
        sp2.set_tile_position(Vertex2f(4, 10))
        self.entities.append(sp2)

        sp3 = StockPile()
        sp3.set_tile_position(Vertex2f(15, 5))
        self.entities.append(sp3)

        sp1.temporary_destination = sp2
        sp2.temporary_destination = sp3
        sp3.temporary_destination = sp1

        wanderer = Wanderer()
        self.entities.append(wanderer)

        wanderer2 = Wanderer()
        self.entities.append(wanderer2)

    def _init_10_10_terrain(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                self.terrain[x][y] = GROUND

        self.terrain[6][3] = WALL
        self.terrain[6][4] = WALL
        self.terrain[6][5] = WALL
        self.terrain[6][6] = WALL
        self.terrain[6][7] = WALL
        self.terrain[6][8] = WALL
        self.terrain[6][9] = WALL

        self.terrain[3][0] = WALL
        self.terrain[3][1] = WALL
        self.terrain[3][2] = WALL
        self.terrain[3][3] = WALL
        self.terrain[3][4] = WALL
        self.terrain[3][5] = WALL
        self.terrain[3][6] = WALL

        # Add impossible path
        self.terrain[4][4] = WALL
        self.terrain[5][4] = WALL
