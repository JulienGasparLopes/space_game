from abc import ABC, abstractmethod, abstractproperty
from typing import TYPE_CHECKING
from maths.colors import GREEN, PURPLE
from maths.matrix import Matrix
from maths.vertex import Vertex2f, Vertex3f
from graphics.renderer import Renderer
from game_logic.tile import TILE_SIZE
from maths.colors import BLUE, ORANGE, YELLOW
from space_game.the_factory.entities.belt import Belt
from game_logic.entity import Direction, Entity
from the_factory.entities.material import Material
from the_factory.context.game_context import GameContext

if TYPE_CHECKING:
    from the_factory.maps.map import Map


class IOFactory(Entity, ABC):
    _buffer: list[Material]

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

    @property
    def target_belt_tile_position(self) -> Vertex2f:
        return self._target_belt_position.divided(TILE_SIZE, floor=True)

    @abstractproperty
    def is_available(self) -> bool:
        ...


class FactoryInput(IOFactory):
    def __init__(self, position_offset: Vertex2f, direction: Direction) -> None:
        super().__init__(BLUE, position_offset, direction)

    def update(self, delta_ms: int, map: "Map") -> None:
        if len(self._buffer) == 0:
            target_belt: Belt = map.get_belt_at_tile_position(
                self.target_belt_tile_position
            )
            if target_belt:
                material = target_belt.get_material()
                if material:
                    self._buffer.append(material)

    def get_material(self) -> Material | None:
        if len(self._buffer) > 0:
            return self._buffer.pop(0)
        return None

    @property
    def is_available(self) -> bool:
        return len(self._buffer) > 0


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
        if len(self._buffer) == 0:
            self._buffer.append(material)
            return True
        return False

    @property
    def is_available(self) -> bool:
        return len(self._buffer) == 0


class Factory(Entity, ABC):
    inputs: list[FactoryInput]
    outputs: list[FactoryOutput]

    _io_mapping: Matrix[IOFactory]

    process_time_ms: int
    _process_counter: int
    _processing: bool

    def __init__(
        self,
        width: int,
        height: int,
        inputs: list[FactoryInput],
        outputs: list[FactoryOutput],
        process_time_ms: int = 1000,
    ) -> None:
        self.inputs = inputs
        self.outputs = outputs

        self._io_mapping = Matrix.from_size(width, height, initial_value=None)
        for input in inputs:
            self._io_mapping.set(input._factory_position_offset, input)
        for output in outputs:
            self._io_mapping.set(output._factory_position_offset, output)

        self.process_time_ms = process_time_ms
        self._process_counter = process_time_ms
        self._processing = False
        super().__init__(GREEN, width * TILE_SIZE, height * TILE_SIZE)

    def render(self, renderer: Renderer) -> None:
        self.content = GREEN
        if self.is_blocked:
            self.content = Vertex3f(160, 140, 0)
        elif self.is_processing:
            self.content = Vertex3f(0, 200, 50)
        super().render(renderer)
        ios: list[IOFactory] = [*self.inputs, *self.outputs]
        for io in ios:
            io.render(renderer)

    def update(self, delta_ms: int, map: "Map") -> None:
        ios: list[IOFactory] = [*self.inputs, *self.outputs]
        for io in ios:
            io.update(delta_ms, map)

        if self.is_processing and self._process_counter > 0:
            self._process_counter -= delta_ms

        if self.is_processing and self._process_counter <= 0:
            processed = self.process_done()
            if processed:
                self._process_counter = self.process_time_ms
                self._processing = False

    def set_tile_position(self, position: Vertex2f) -> None:
        super().set_tile_position(position)
        ios: list[IOFactory] = [*self.inputs, *self.outputs]
        for io in ios:
            io.update_position(self.position)

    def set_position(
        self,
        position: Vertex2f,
        is_center_position: bool = False,
        bound_to_tile: bool = False,
    ) -> None:
        super().set_position(position, is_center_position, bound_to_tile)
        ios: list[IOFactory] = [*self.inputs, *self.outputs]
        for io in ios:
            io.update_position(self.position)

    def set_direction(self, direction: Direction) -> None:
        rotation_number = {
            Direction.NORTH: 0,
            Direction.EAST: 1,
            Direction.SOUTH: 2,
            Direction.WEST: 3,
        }.get(direction, 0)
        for _ in range(rotation_number):
            self.rotate()

    def rotate(self, clockwise: bool = True) -> None:
        super().rotate(clockwise)
        self._io_mapping.rotate(clockwise)
        for io, pos in self._io_mapping.get_entries():
            if io:
                io.update_factory_tile_position_offset(pos)
                io.rotate(clockwise)

    def start_processing(self) -> None:
        self._processing = True

    @abstractmethod
    def process_done(self) -> bool:
        ...

    @property
    def is_processing(self) -> bool:
        return self._processing

    @property
    def is_blocked(self) -> bool:
        return self.is_processing and self._process_counter <= 0


class MaterialChute(Factory):
    def __init__(self, delay: int, direction: Direction = Direction.EAST) -> None:
        super().__init__(1, 1, [], [FactoryOutput(Vertex2f(0, 0), direction)], delay)
        self._direction = direction

    def process_done(self) -> bool:
        return self.outputs[0].insert_material(Material(YELLOW))

    def update(self, delta_ms: int, map: "Map") -> None:
        super().update(delta_ms, map)
        if not self.is_processing:
            if GameContext.get().money_transaction(-20):
                self.start_processing()


class MaterialSeller(Factory):
    def __init__(self, delay: int, direction: Direction = Direction.EAST) -> None:
        super().__init__(1, 1, [FactoryInput(Vertex2f(0, 0), direction)], [], delay)
        self._direction = direction

    def process_done(self) -> bool:
        return GameContext.get().money_transaction(100)

    def update(self, delta_ms: int, map: "Map") -> None:
        super().update(delta_ms, map)
        if not self.is_processing:
            material = self.inputs[0].get_material()
            if material:
                self.start_processing()


class Transformator(Factory):
    def __init__(self) -> None:
        inputs = [FactoryInput(Vertex2f(0, 1), direction=Direction.WEST)]
        outputs = [FactoryOutput(Vertex2f(2, 1), direction=Direction.EAST)]
        super().__init__(3, 3, inputs, outputs)

    def update(self, delta_ms: int, map: "Map") -> None:
        super().update(delta_ms, map)

        if not self.is_processing and self.outputs[0].is_available:
            material = self.inputs[0].get_material()
            if material:
                self.start_processing()

    def process_done(self) -> bool:
        if self.outputs[0].is_available:
            return self.outputs[0].insert_material(Material(ORANGE))
        return False


class Fabricator(Factory):
    def __init__(self) -> None:
        inputs = [
            FactoryInput(Vertex2f(0, 1), direction=Direction.WEST),
            FactoryInput(Vertex2f(0, 3), direction=Direction.WEST),
        ]
        outputs = [
            FactoryOutput(Vertex2f(4, 2), direction=Direction.EAST),
        ]
        super().__init__(5, 5, inputs, outputs)

    def update(self, delta_ms: int, map: "Map") -> None:
        super().update(delta_ms, map)

        if not self.is_processing and self.outputs[0].is_available:
            if self.inputs[0].is_available and self.inputs[1].is_available:
                self.inputs[0].get_material()
                self.inputs[1].get_material()
                self.start_processing()

    def process_done(self) -> bool:
        if self.outputs[0].is_available:
            return self.outputs[0].insert_material(Material(PURPLE))
        return False
