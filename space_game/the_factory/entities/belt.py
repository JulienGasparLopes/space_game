from enum import Enum
from typing import Dict, List

from game_logic.entity import Direction
from game_logic.tile import TILE_SIZE
from graphics.renderer import Renderer
from graphics.renderer_tk.renderer_tk import Image
from maths.vertex import Vertex2f
from the_factory.entities.base_belt import BaseBelt
from the_factory.entities.material import Material
from the_factory.logic.material_type import MaterialType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from the_factory.maps.map import Map

_BELT_IMAGE_PATH = "space_game/the_factory/entities/images/belt.png"

_BELT_DIRECTION_TO_IMAGE = {
    Direction.NORTH: Image(_BELT_IMAGE_PATH, 180),
    Direction.EAST: Image(_BELT_IMAGE_PATH, 90),
    Direction.SOUTH: Image(_BELT_IMAGE_PATH, 0),
    Direction.WEST: Image(_BELT_IMAGE_PATH, 270),
}


class BeltIOType(Enum):
    NONE = 0
    INPUT = 1
    OUTPUT = 2
    INOUT = 3

    @property
    def is_input(self) -> bool:
        return self == BeltIOType.INPUT or self == BeltIOType.INOUT

    @property
    def is_output(self) -> bool:
        return self == BeltIOType.OUTPUT or self == BeltIOType.INOUT


class BeltIOInfo:
    _type: BeltIOType
    _segment_time_ms: int
    _counter_ms: int
    _material: Material | None

    def __init__(self, type: BeltIOType, segment_time_ms: int) -> None:
        self._type = type
        self._segment_time_ms = segment_time_ms
        self._counter_ms = 0
        self._material = None


class Belt(BaseBelt):
    _material_per_minute: int
    _time_ms_per_segment: int

    _io_configurations: Dict[Direction | None, BeltIOInfo]
    _output_direction_priorities: List[Direction]
    # TODO: input priorities (use a list of entities that asked for insertion, remove after X updates)

    def __init__(
        self, direction: Direction = Direction.NORTH, material_per_minute: int = 300
    ) -> None:
        super().__init__(_BELT_DIRECTION_TO_IMAGE[direction])
        self._material_per_minute = material_per_minute
        self._time_ms_per_segment = (60 * 1000 // 2) // self._material_per_minute
        self.set_direction(direction)

    def set_direction(self, direction: Direction) -> None:
        super().set_direction(direction)
        self._io_configurations = {}
        for dir in Direction:
            _type = BeltIOType.OUTPUT if dir == direction else BeltIOType.INPUT
            self._io_configurations[dir] = BeltIOInfo(_type, self._time_ms_per_segment)
        self._io_configurations[None] = BeltIOInfo(
            BeltIOType.INOUT, self._time_ms_per_segment
        )
        self.content = _BELT_DIRECTION_TO_IMAGE.get(direction)
        self._init_direction_priorities()

    def _init_direction_priorities(self) -> None:
        self._output_direction_priorities = []
        for dir, _ in self._outputs:
            self._output_direction_priorities.append(dir)

    def render(self, renderer: Renderer, z_index: int = 0) -> None:
        super().render(renderer)
        for dir, info in self._io_configurations.items():
            if material := info._material:
                origin = self._position.translated(
                    Vertex2f(TILE_SIZE // 2, TILE_SIZE // 2)
                )
                ratio = (
                    (1 - info._counter_ms / info._segment_time_ms)
                    if info._type.is_output
                    else info._counter_ms / info._segment_time_ms
                )
                offset = (
                    dir.vertex.multiplied(ratio * (TILE_SIZE / 2))
                    if dir
                    else Vertex2f(0, 0)
                )
                material.set_position(
                    origin.translated(offset), is_center_position=True
                )
                material.render(renderer, 1)

    def accepts_material_from(self, direction: Direction | None) -> bool:
        return self._io_configurations[direction]._type.is_input

    def insert_material(
        self, material: Material, direction: Direction | None = None
    ) -> bool:
        if not self.accepts_material_from(direction):
            return False

        for _, input_info in self._inputs:
            if input_info._material is not None:
                return False

        if self._io_configurations[None]._material is None:
            belt_io_info = self._io_configurations[direction]
            if belt_io_info._type.is_input and belt_io_info._material is None:
                belt_io_info._material = material
                belt_io_info._counter_ms = self._time_ms_per_segment
                return True
        return False

    def pop_material(self) -> Material | None:
        belt_info = self._io_configurations[None]
        if belt_info._material and belt_info._counter_ms <= 0:
            material = belt_info._material
            belt_info._material = None
            return material
        return None

    def get_material_type(self) -> MaterialType | None:
        belt_info = self._io_configurations[None]
        if belt_info._material and belt_info._counter_ms <= 0:
            return belt_info._material.material_type
        return None

    def update(self, delta_ms: int, map: "Map") -> None:
        # Send center_material to outputs
        if current_material := self._io_configurations[None]._material:
            for output_dir in self._output_direction_priorities:
                output_info = self._io_configurations.get(output_dir)
                if not output_info:
                    continue
                if output_info._material is None:
                    target = map.get_belt_at_tile_position(
                        self.tile_position.translated(output_dir.vertex)
                    )
                    if target and target.accepts_material_from(output_dir.opposite):
                        output_info._material = current_material
                        output_info._counter_ms = self._time_ms_per_segment
                        self._io_configurations[None]._material = None
                        # Add back priority to the end of the list
                        self._output_direction_priorities.remove(output_dir)
                        self._output_direction_priorities.append(output_dir)
                        break

        # Update outputs
        for output_dir, output_info in self._outputs:
            if output_info._material and output_info._counter_ms > 0:
                output_info._counter_ms -= delta_ms
                if output_info._counter_ms <= 0:
                    output_info._counter_ms = 0
            if output_info._counter_ms <= 0:
                target = map.get_belt_at_tile_position(
                    self.tile_position.translated(output_dir.vertex)
                )
                if target:
                    added = target.insert_material(
                        output_info._material, output_dir.opposite
                    )
                    if added:
                        output_info._material = None

        # Update inputs
        if self._io_configurations[None]._material is None:
            for input_dir, input_info in self._inputs:
                if input_info._material and input_info._counter_ms > 0:
                    input_info._counter_ms -= delta_ms
                    if input_info._counter_ms <= 0:
                        input_info._counter_ms = 0
                if input_info._counter_ms <= 0:
                    if self._io_configurations[None]._material is None:
                        self._io_configurations[None]._material = input_info._material
                        input_info._material = None

    @property
    def _inputs(self) -> List[tuple[Direction, BeltIOInfo]]:
        return [
            (dir, info)
            for dir, info in self._io_configurations.items()
            if info._type == BeltIOType.INPUT
        ]

    @property
    def _outputs(self) -> List[tuple[Direction, BeltIOInfo]]:
        return [
            (dir, info)
            for dir, info in self._io_configurations.items()
            if info._type == BeltIOType.OUTPUT
        ]
