from time import process_time
from typing import Any
from maths.colors import GREEN
from maths.vertex import Vertex2f, Vertex3f
from graphics.renderer import Renderer
from game_logic.tile import TILE_SIZE
from maths.colors import BLUE, ORANGE, YELLOW
from space_game.the_factory.entities.belt import Belt
from the_factory.entities.entity import Direction, Entity
from the_factory.entities.material import Material


class IOFactory(Entity):
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
        )

    def update_position(self):
        self.set_position(
            self.factory.position.translated(self._position_offset).translated(
                Vertex2f(TILE_SIZE / 2, TILE_SIZE / 2)
            )
        )

    def update(self, delta_ms: int, map: Any) -> None:
        ...


class FactoryInput(IOFactory):
    def __init__(self, factory: "Factory", position_offset: Vertex2f) -> None:
        super().__init__(factory, BLUE, position_offset)

    def update(self, delta_ms: int, map: Any) -> None:
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


class FactoryOutput(IOFactory):
    def __init__(self, factory: "Factory", position_offset) -> None:
        super().__init__(factory, ORANGE, position_offset)

    def update(self, delta_ms: int, map: Any) -> None:
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

    def available(self) -> bool:
        return len(self._buffer) == 0


class Factory(Entity):
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
        super().render(renderer)
        ios: list[IOFactory] = [*self.inputs, *self.outputs]
        for io in ios:
            io.render(renderer)

    def update(self, delta_ms: int, map: Any) -> None:
        ios: list[IOFactory] = [*self.inputs, *self.outputs]
        for io in ios:
            io.update(delta_ms, map)
            
        if self._processing and self._process_counter > 0:
            self._process_counter -= delta_ms

        if self._processing and self._process_counter <= 0:
            processed = self.process_done()
            if processed:
                self._process_counter = self.process_time_ms
                self._processing = False

    def set_tile_position(self, position: Vertex2f) -> None:
        super().set_tile_position(position)
        ios: list[IOFactory] = [*self.inputs, *self.outputs]
        for io in ios:
            io.update_position()
            
    def start_processing(self) -> None:
        self._processing = True

    def process_done(self) -> bool:
        return False

class MaterialChute(Factory):
    _new_material_delay: int
    _new_material_counter: int

    def __init__(self, delay: int, direction: Direction = Direction.EAST) -> None:
        super().__init__(1, 1, [], [FactoryOutput(self, direction.vertex)], delay)
        self._direction = direction
        self.start_processing()
            
    def process_done(self) -> bool:
        return self.outputs[0].insert_material(Material(YELLOW))

    def update(self, delta_ms: int, map: Any) -> None:
        super().update(delta_ms, map)
        self._processing = True


class Transformator(Factory):
    def __init__(self) -> None:
        inputs = [FactoryInput(self, Vertex2f(-1, 1))]
        outputs = [FactoryOutput(self, Vertex2f(3, 1))]
        super().__init__(3, 3, inputs, outputs)

    def update(self, delta_ms: int, map: Any) -> None:
        super().update(delta_ms, map)
        
        if not self._processing and self.outputs[0].available():
            material = self.inputs[0].get_material()
            if material:
                material.content = ORANGE
                self.start_processing()
                
    def process_done(self) -> bool:
        if self.outputs[0].available():
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
