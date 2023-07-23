from game_logic.map import Map as BaseMap
from maths.vertex import Vertex2f
from maths.colors import BLUE
from game_logic.room import Room
from game_logic.entity import Entity


class Map(BaseMap):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)

        workbench = Entity(BLUE)
        workbench._tile_position = Vertex2f(6, 3)
        self.entities.append(workbench)

    def _update_rooms(self) -> None:
        self.rooms = []
        for workbench in self.entities:
            room_closed = False
            room_tiles: list[Vertex2f] = []
            tiles_to_check = [workbench._tile_position]
            while len(room_tiles) < 20:
                tile_to_check = tiles_to_check.pop()
                room_tiles.append(tile_to_check)

                new_tile_positions: list[Vertex2f] = [
                    Vertex2f(tile_to_check.x - 1, tile_to_check.y),
                    Vertex2f(tile_to_check.x + 1, tile_to_check.y),
                    Vertex2f(tile_to_check.x, tile_to_check.y - 1),
                    Vertex2f(tile_to_check.x, tile_to_check.y + 1),
                ]
                for new_tile_position in new_tile_positions:
                    new_tile = self._get_tile(new_tile_position)
                    if (
                        new_tile is not None
                        and (not new_tile.is_wall)
                        and (new_tile_position not in room_tiles)
                        and (new_tile_position not in tiles_to_check)
                    ):
                        tiles_to_check.append(new_tile_position)

                if not tiles_to_check:
                    room_closed = True
                    break

            if room_closed:
                self.rooms.append(Room(room_tiles))
