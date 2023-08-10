from game_logic.entity import Direction
from graphics.renderer_tk.renderer_tk import Image
from the_factory.entities.belt import Belt, BeltIOInfo, BeltIOType
from the_factory.entities.material import Material
from the_factory.logic.material_type import MaterialType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from the_factory.maps.map import Map

_DIVIDER_IMAGE_PATH = "space_game/the_factory/entities/images/divider.png"

_DIVIDER_DIRECTION_TO_IMAGE = {
    Direction.NORTH: Image(_DIVIDER_IMAGE_PATH, 180),
    Direction.EAST: Image(_DIVIDER_IMAGE_PATH, 90),
    Direction.SOUTH: Image(_DIVIDER_IMAGE_PATH, 0),
    Direction.WEST: Image(_DIVIDER_IMAGE_PATH, 270),
}


class Divider(Belt):
    def set_direction(self, direction: Direction) -> None:
        super().set_direction(direction)
        self._io_configurations = {}
        for dir in Direction:
            _type = BeltIOType.INPUT if dir == direction.opposite else BeltIOType.OUTPUT
            self._io_configurations[dir] = BeltIOInfo(_type, self._time_ms_per_segment)
        self._io_configurations[None] = BeltIOInfo(
            BeltIOType.NONE, self._time_ms_per_segment
        )
        self.content = _DIVIDER_DIRECTION_TO_IMAGE.get(direction)
        self._init_direction_priorities()

    def pop_material(self) -> Material | None:
        return None

    def get_material_type(self) -> MaterialType | None:
        return None
