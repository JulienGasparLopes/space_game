from game_logic.entity import Entity
from game_logic.map import Map
from maths.vertex import Vertex3f


class Material(Entity):
    def __init__(self, color: Vertex3f, width: int = 10, height: int = 10) -> None:
        super().__init__(color, width, height)

    def update(self, delta_ms: int, map: Map) -> None:
        return super().update(delta_ms, map)
