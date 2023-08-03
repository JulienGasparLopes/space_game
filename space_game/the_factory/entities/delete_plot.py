from typing import TYPE_CHECKING
from maths.colors import RED
from the_factory.entities.entity import Entity

if TYPE_CHECKING:
    from the_factory.maps.map import Map


class DeletePlot(Entity):
    def __init__(self) -> None:
        super().__init__(RED)

    def update(self, delta_ms: int, map: "Map") -> None:
        ...
