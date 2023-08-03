from typing import TYPE_CHECKING
from game_logic.entity import Entity
from maths.colors import RED

if TYPE_CHECKING:
    from the_factory.maps.map import Map


class DeletePlot(Entity):
    def __init__(self) -> None:
        super().__init__(RED)

    def update(self, delta_ms: int, map: "Map") -> None:
        ...
