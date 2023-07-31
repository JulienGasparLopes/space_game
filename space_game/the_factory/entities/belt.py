from typing import TYPE_CHECKING
from game_logic.entity import Entity
from game_logic.tile import TILE_SIZE
from graphics.renderer_tk import Image
from graphics.renderer import Renderer
from maths.vertex import Vertex2f
from the_factory.entities.entity import Direction
from the_factory.entities.material import Material

if TYPE_CHECKING:
    from the_factory.factory_map import Map

BELT_IMAGE_PATH = "space_game/the_factory/entities/images/belt.png"

DIRECTION_TO_IMAGE = {
    Direction.NORTH: Image(BELT_IMAGE_PATH, 180),
    Direction.EAST: Image(BELT_IMAGE_PATH, 90),
    Direction.SOUTH: Image(BELT_IMAGE_PATH, 0),
    Direction.WEST: Image(BELT_IMAGE_PATH, 270),
}


class Belt(Entity):
    _material_on_input: Material | None = None
    _material_on_belt: Material | None = None
    _material_on_output: Material | None = None

    _material_per_minute: int

    _time_ms_on_input: int = 0
    _time_ms_on_belt: int = 0

    _intput_direction_origin: Direction | None

    def __init__(
        self, direction: Direction = Direction.NORTH, material_per_minute: int = 60
    ) -> None:
        super().__init__(DIRECTION_TO_IMAGE.get(direction))
        self._direction = direction
        self._material_per_minute = material_per_minute
        self._time_ms_per_segment = (60 * 1000 // 2) // self._material_per_minute
        self._time_ms_on_belt = self._time_ms_per_segment
        self._time_ms_on_input = self._time_ms_per_segment

    def render(self, renderer: Renderer) -> None:
        super().render(renderer)
        if self._material_on_input:
            self._material_on_input.render(renderer, 1)
        if self._material_on_belt:
            self._material_on_belt.render(renderer, 1)
        if self._material_on_output:
            self._material_on_output.render(renderer, 1)

    def insert_material(
        self, material: Material, direction: Direction | None = None
    ) -> bool:
        """direction == None -> add directly on belt"""
        if direction is None and not (
            self._material_on_input or self._material_on_belt
        ):
            self._material_on_belt = material
            self._time_ms_on_belt = self._time_ms_per_segment
            self._update_materials_position()
            return True
        elif (
            direction != self._direction
            and not self._material_on_input
            and not (self._material_on_belt and self._material_on_output)
        ):  # Cant add to output
            self._material_on_input = material
            self._intput_direction_origin = direction
            self._time_ms_on_input = self._time_ms_per_segment
            self._update_materials_position()
            return True

        return False

    def get_material(self) -> Material | None:
        if self._material_on_belt:
            material = self._material_on_belt
            self._material_on_belt = None
            self._time_ms_on_belt = self._time_ms_per_segment
            return material
        return None

    def update(self, delta_ms: int, map: "Map") -> None:
        if self._material_on_belt and not self._material_on_output:
            self._time_ms_on_belt -= delta_ms
            if self._time_ms_on_belt <= 0:
                self._material_on_output = self._material_on_belt
                self._material_on_belt = None
                self._time_ms_on_belt = self._time_ms_per_segment

        if self._material_on_input:
            expected = self._time_ms_on_input - delta_ms
            min_authorized = self._time_ms_on_belt if self._material_on_belt else 0
            self._time_ms_on_input = max(expected, min_authorized)
            if self._time_ms_on_input <= 0:
                self._material_on_belt = self._material_on_input
                self._material_on_input = None
                self._intput_direction_origin = None
                self._time_ms_on_input = self._time_ms_per_segment

        if self._material_on_output:
            target = map.get_belt_at_tile_position(
                self.tile_position.translated(self._direction.value.vertex)
            )
            if target:
                added = target.insert_material(
                    self._material_on_output, self._direction.opposite
                )
                if added:
                    self._material_on_output = None

        self._update_materials_position()

    def _update_materials_position(self) -> None:
        center = self.position.translated(Vertex2f(TILE_SIZE // 2, TILE_SIZE // 2))

        if self._material_on_belt:
            ratio = self._time_ms_on_belt / self._time_ms_per_segment
            offset = (1 - ratio) * TILE_SIZE // 2
            pos = center.translated(self._direction.vertex.multiplied(offset))
            self._material_on_belt.set_position(pos, is_center_position=True)

        if self._material_on_input and self._intput_direction_origin:
            # self._intput_direction_origin should be True in this case
            ratio = self._time_ms_on_input / self._time_ms_per_segment
            offset = (-ratio) * TILE_SIZE // 2
            pos = center.translated(
                self._intput_direction_origin.opposite.vertex.multiplied(offset)
            )
            self._material_on_input.set_position(pos, is_center_position=True)

        if self._material_on_output:
            offset = -TILE_SIZE // 2
            pos = center.translated(self._direction.opposite.vertex.multiplied(offset))
            self._material_on_output.set_position(pos, is_center_position=True)
