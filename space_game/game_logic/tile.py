from dataclasses import dataclass
from maths.vertex import Vertex3f
from maths.colors import BLACK

TILE_SIZE = 60


@dataclass
class Tile:
    color: Vertex3f
    is_wall: bool = False


VOID = Tile(BLACK, False)
