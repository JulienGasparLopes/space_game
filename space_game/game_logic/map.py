from graphics.renderer import Renderer
from maths.vertex import Vertex2f
from maths.colors import WHITE, BLACK, BLUE
from game_logic.tile import Tile, GROUND, WALL, TILE_SIZE
from game_logic.entity import Entity
from game_logic.room import Room


class Map:
    width: int
    height: int
    terrain: list[list[Tile]]
    entities: list[Entity]
    rooms: list[Room]

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.entities = []
        self.terrain = []
        self.rooms = []

        for x in range(self.width):
            self.terrain.append([])
            for y in range(self.height):
                self.terrain[x].append(GROUND)

        workbench = Entity(BLUE)
        workbench.tile_position = Vertex2f(6, 3)
        self.entities.append(workbench)

    def render(self, renderer: Renderer) -> None:
        for x, tile_column in enumerate(self.terrain):
            for y, tile in enumerate(tile_column):
                renderer.draw_rect(
                    Vertex2f(x * TILE_SIZE, y * TILE_SIZE),
                    Vertex2f((x + 1) * TILE_SIZE, (y + 1) * TILE_SIZE),
                    tile.color,
                )

        for entity in self.entities:
            entity.render(renderer)

        for room in self.rooms:
            room.render(renderer)

        for x in range(self.width):
            renderer.draw_line(
                Vertex2f(x * TILE_SIZE, 0),
                Vertex2f(x * TILE_SIZE, self.height * TILE_SIZE),
                BLACK,
            )

        for y in range(self.height):
            renderer.draw_line(
                Vertex2f(0, y * TILE_SIZE),
                Vertex2f(self.width * TILE_SIZE, y * TILE_SIZE),
                BLACK,
            )

    def _get_tile(self, position: Vertex2f) -> Tile | None:
        if (
            position.x < 0
            or position.x >= self.width
            or position.y < 0
            or position.y >= self.height
        ):
            return None
        return self.terrain[position.x][position.y]

    def _update_rooms(self) -> None:
        self.rooms = []
        for workbench in self.entities:
            room_closed = False
            room_tiles: list[Vertex2f] = []
            tiles_to_check = [workbench.tile_position]
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
