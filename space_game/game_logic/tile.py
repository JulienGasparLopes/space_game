from dataclasses import dataclass
from maths.vertex import Vertex2f, Vertex3f
from maths.colors import WHITE, RED

TILE_SIZE = 20


@dataclass
class Tile:
    color: Vertex3f
    is_wall: bool = False


GROUND = Tile(WHITE, False)
WALL = Tile(RED, True)
