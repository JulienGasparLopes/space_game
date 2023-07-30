from graphics.renderer import Renderer
from maths.vertex import Vertex2f, Vertex3f
from game_logic.tile import Tile, VOID, TILE_SIZE
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
            for _ in range(self.height):
                self.terrain[x].append(VOID)

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
                Vertex3f(240, 240, 240),
            )

        for y in range(self.height):
            renderer.draw_line(
                Vertex2f(0, y * TILE_SIZE),
                Vertex2f(self.width * TILE_SIZE, y * TILE_SIZE),
                Vertex3f(240, 240, 240),
            )

    def update(self, delta_ms: int) -> None:
        for entity in self.entities:
            entity.update(delta_ms, self)

    def _get_tile(self, position: Vertex2f) -> Tile | None:
        if (
            position.x < 0
            or position.x >= self.width
            or position.y < 0
            or position.y >= self.height
        ):
            return None
        return self.terrain[position.x][position.y]

    def get_entities_at_tile(self, tile_position: Vertex2f) -> list[Entity]:
        return [e for e in self.entities if e.tile_position == tile_position]
