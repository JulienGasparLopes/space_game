from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

from game_logic.entity import Direction, Entity
from game_logic.tile import TILE_SIZE
from graphics.renderer import Renderer
from maths.colors import BLUE, ORANGE
from maths.vertex import Vertex2f, Vertex3f
from the_factory.logic.material_type import MaterialType
from the_factory.entities.material import Material

from space_game.the_factory.entities.belt import Belt

if TYPE_CHECKING:
    from the_factory.maps.map import Map


class IOFactory(Entity, ABC):
    _buffer: list[Material]
    _max_amount: int = 0
    _target_material_type: MaterialType | None = None

    _factory_position: Vertex2f = Vertex2f(0, 0)
    _factory_position_offset: Vertex2f
    _target_belt_position: Vertex2f = Vertex2f(0, 0)

    def __init__(
        self,
        color: Vertex3f,
        factory_tile_position_offset: Vertex2f,
        direction: Direction,
    ) -> None:
        super().__init__(color, 4, 4)
        self._buffer = []
        self.set_direction(direction)
        self._factory_position_offset = factory_tile_position_offset

    def render(self, renderer: Renderer) -> None:
        renderer.draw_rect(
            Vertex2f(
                self._target_belt_position.x - 4, self._target_belt_position.y - 4
            ),
            Vertex2f(
                self._target_belt_position.x + 4, self._target_belt_position.y + 4
            ),
            self.content,
            z_index=2,
        )

    def update_position(self, factory_position: Vertex2f) -> None:
        self._factory_position = factory_position
        self.set_position(
            factory_position.translated(
                self._factory_position_offset.multiplied(TILE_SIZE)
            )
        )
        self._target_belt_position = self.position.translated(
            self.direction.vertex.multiplied(TILE_SIZE)
        ).translated(Vertex2f(TILE_SIZE / 2, TILE_SIZE / 2))

    def update_factory_tile_position_offset(
        self, factory_tile_position_offset: Vertex2f
    ) -> None:
        self._factory_position_offset = factory_tile_position_offset
        self.set_position(
            self._factory_position.translated(
                self._factory_position_offset.multiplied(TILE_SIZE)
            )
        )
        self._target_belt_position = self.position.translated(
            self.direction.vertex.multiplied(TILE_SIZE)
        ).translated(Vertex2f(TILE_SIZE / 2, TILE_SIZE / 2))

    def rotate(self, clockwise: bool = True) -> None:
        super().rotate(clockwise)
        self._target_belt_position = self.position.translated(
            self.direction.vertex.multiplied(TILE_SIZE)
        ).translated(Vertex2f(TILE_SIZE / 2, TILE_SIZE / 2))

    def set_material_info(self, material_type: MaterialType, max_mount: int) -> None:
        self._target_material_type = material_type
        self._max_amount = max_mount

    @property
    def target_belt_tile_position(self) -> Vertex2f:
        return self._target_belt_position.divided(TILE_SIZE, floor=True)

    @abstractmethod
    def is_available(self, amount: int) -> bool:
        ...


class FactoryInput(IOFactory):
    def __init__(self, position_offset: Vertex2f, direction: Direction) -> None:
        super().__init__(BLUE, position_offset, direction)

    def update(self, delta_ms: int, map: "Map") -> None:
        if not self._target_material_type:
            return

        if len(self._buffer) < self._max_amount:
            target_belt: Belt = map.get_belt_at_tile_position(
                self.target_belt_tile_position
            )
            if target_belt:
                if target_belt.get_material_type() == self._target_material_type:
                    material = target_belt.pop_material()
                    if material:
                        self._buffer.append(material)

    def get_materials(self, amount: int = 1) -> List[Material]:
        materials: List[Material] = []
        if not self.is_available(amount):
            return materials

        for _ in range(amount):
            material = self._buffer.pop(0)
            if material:
                materials.append(material)
        return materials

    def is_available(self, amount: int) -> bool:
        return len(self._buffer) >= amount


class FactoryOutput(IOFactory):
    def __init__(self, position_offset: Vertex2f, direction: Direction) -> None:
        super().__init__(ORANGE, position_offset, direction)

    def update(self, delta_ms: int, map: "Map") -> None:
        if len(self._buffer) > 0:
            material = self._buffer[0]
            target_belt: Belt = map.get_belt_at_tile_position(
                self.target_belt_tile_position
            )
            if target_belt:
                inserted = target_belt.insert_material(material)
                if inserted:
                    self._buffer.pop(0)

    def insert_material(self, material: Material) -> bool:
        if self.is_available(1):
            self._buffer.append(material)
            return True
        return False

    def is_available(self, amount: int) -> bool:
        return self._max_amount - len(self._buffer) >= amount
