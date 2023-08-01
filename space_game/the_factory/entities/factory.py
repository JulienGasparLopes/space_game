from abc import ABC, abstractmethod, abstractproperty
from typing import TYPE_CHECKING
from maths.colors import GREEN, PURPLE
from maths.vertex import Vertex2f, Vertex3f
from graphics.renderer import Renderer
from game_logic.tile import TILE_SIZE
from maths.colors import BLUE, ORANGE, YELLOW
from space_game.the_factory.entities.belt import Belt
from the_factory.entities.entity import Direction, Entity
from the_factory.entities.material import Material
from the_factory.game_context import GameContext

if TYPE_CHECKING:
    from the_factory.factory_map import Map


class IOFactory(Entity, ABC):
    factory: "Factory"

    _buffer: list[Material]
    _position_offset: Vertex2f

    def __init__(
        self, factory: "Factory", color: Vertex3f, position_offset: Vertex2f
    ) -> None:
        super().__init__(color, 4, 4)
        self.factory = factory
        self._buffer = []
        self._position_offset = position_offset.multiplied(TILE_SIZE)

    def render(self, renderer: Renderer) -> None:
        renderer.draw_rect(
            Vertex2f(self.position.x - 4, self.position.y - 4),
            Vertex2f(self.position.x + 4, self.position.y + 4),
            self.content,
            z_index=2,
        )

    def update_position(self) -> None:
        self.set_position(
            self.factory.position.translated(self._position_offset).translated(
                Vertex2f(TILE_SIZE / 2, TILE_SIZE / 2)
            )
        )

    @abstractproperty
    def is_available(self) -> bool:
        ...


class FactoryInput(IOFactory):
    def __init__(self, factory: "Factory", position_offset: Vertex2f) -> None:
        super().__init__(factory, BLUE, position_offset)

    def update(self, delta_ms: int, map: "Map") -> None:
        if len(self._buffer) == 0:
            target_belt: Belt = map.get_belt_at_tile_position(self.tile_position)
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
    def __init__(self, factory: "Factory", position_offset: Vertex2f) -> None:
        super().__init__(factory, ORANGE, position_offset)

    def update(self, delta_ms: int, map: "Map") -> None:
        if len(self._buffer) > 0:
            material = self._buffer[0]
            target_belt: Belt = map.get_belt_at_tile_position(self.tile_position)
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
            io.update_position()

    def set_position(
        self,
        position: Vertex2f,
        is_center_position: bool = False,
        bound_to_tile: bool = False,
    ) -> None:
        super().set_position(position, is_center_position, bound_to_tile)
        ios: list[IOFactory] = [*self.inputs, *self.outputs]
        for io in ios:
            io.update_position()

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
        super().__init__(1, 1, [], [FactoryOutput(self, direction.vertex)], delay)
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
        super().__init__(1, 1, [FactoryInput(self, direction.vertex)], [], delay)
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
        inputs = [FactoryInput(self, Vertex2f(-1, 1))]
        outputs = [FactoryOutput(self, Vertex2f(3, 1))]
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
            FactoryInput(self, Vertex2f(-1, 1)),
            FactoryInput(self, Vertex2f(-1, 3)),
        ]
        outputs = [
            FactoryOutput(self, Vertex2f(5, 2)),
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
