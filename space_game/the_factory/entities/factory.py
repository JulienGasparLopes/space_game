from abc import ABC
from typing import TYPE_CHECKING
from typing_extensions import override
from maths.matrix import Matrix
from maths.vertex import Vertex2f, Vertex3f
from graphics.renderer import Renderer
from game_logic.tile import TILE_SIZE
from maths.colors import GREEN
from game_logic.entity import Direction, Entity
from the_factory.entities.io_factory import FactoryInput, FactoryOutput, IOFactory
from the_factory.entities.material import Material
from the_factory.context.game_context import GameContext
from the_factory.logic.material_type import ANY_MATERIAL, IRON
from the_factory.logic.recipe import Recipe, RecipeLine

if TYPE_CHECKING:
    from the_factory.maps.map import Map


class Factory(Entity, ABC):
    inputs: list[FactoryInput]
    outputs: list[FactoryOutput]

    _io_mapping: Matrix[IOFactory]

    _process_counter: int
    _processing: bool

    _recipe: Recipe | None = None

    def __init__(
        self,
        width: int,
        height: int,
        inputs: list[FactoryInput],
        outputs: list[FactoryOutput],
    ) -> None:
        self.inputs = inputs
        self.outputs = outputs

        self._io_mapping = Matrix.from_size(width, height, initial_value=None)
        for input in inputs:
            self._io_mapping.set(input._factory_position_offset, input)
        for output in outputs:
            self._io_mapping.set(output._factory_position_offset, output)

        self._process_counter = 999999999
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
        if not self._recipe:
            return

        # Update IOs
        ios: list[IOFactory] = [*self.inputs, *self.outputs]
        for io in ios:
            io.update(delta_ms, map)

        # Update internal counter
        if self.is_processing and self._process_counter > 0:
            self._process_counter -= delta_ms

        # Check process avancement
        if self.is_processing and self._process_counter <= 0:
            processed = self.process_done()
            if processed:
                self._process_counter = self._recipe.processing_time_ms
                self._processing = False

        # Check if process can start
        if not self.is_processing:
            if self.should_start_processing():
                self.start_processing()

    def should_start_processing(self) -> bool:
        if not self.is_processing and self._recipe is not None:
            may_start_processing = True
            for idx, input in enumerate(self.inputs):
                if not input.is_available(self._recipe.get_input_line(idx).amount):
                    may_start_processing = False

            for idx, output in enumerate(self.outputs):
                if not output.is_available(self._recipe.get_output_line(idx).amount):
                    may_start_processing = False

            return may_start_processing
        return False

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
        if self._recipe:
            for idx, input in enumerate(self.inputs):
                input.get_materials(self._recipe.get_input_line(idx).amount)
            self._process_counter = self._recipe.processing_time_ms
        self._processing = True

    def set_recipe(self, recipe: Recipe) -> None:
        self._recipe = recipe
        self._process_counter = self._recipe.processing_time_ms
        self._processing = False

        for idx, input in enumerate(self.inputs):
            recipe_line = self._recipe.get_input_line(idx)
            input.set_material_info(recipe_line.material_type, recipe_line.amount)

        for idx, output in enumerate(self.outputs):
            recipe_line = self._recipe.get_output_line(idx)
            output.set_material_info(recipe_line.material_type, recipe_line.amount)

    def process_done(self) -> bool:
        if not self._recipe:
            return False

        may_end_processing = True
        for idx, output in enumerate(self.outputs):
            if not output.is_available(self._recipe.get_output_line(idx).amount):
                may_end_processing = False
        if may_end_processing:
            for idx, output in enumerate(self.outputs):
                output.insert_material(
                    Material.from_type(self._recipe.get_output_line(idx).material_type)
                )
            return True

        return False

    @property
    def is_processing(self) -> bool:
        return self._processing

    @property
    def is_blocked(self) -> bool:
        return self.is_processing and self._process_counter <= 0


class MaterialChute(Factory):
    def __init__(self, delay: int, direction: Direction = Direction.EAST) -> None:
        super().__init__(1, 1, [], [FactoryOutput(Vertex2f(0, 0), direction)])
        self._direction = direction
        self.set_recipe(Recipe([], [RecipeLine(IRON, 1)], delay))

    @override
    def should_start_processing(self) -> bool:
        should_start = super().should_start_processing()
        return should_start and GameContext.get().money_transaction(-20)


class MaterialSeller(Factory):
    def __init__(self, delay: int, direction: Direction = Direction.EAST) -> None:
        super().__init__(1, 1, [FactoryInput(Vertex2f(0, 0), direction)], [])
        self._direction = direction
        self.set_recipe(Recipe([RecipeLine(ANY_MATERIAL, 1)], [], delay))

    def process_done(self) -> bool:
        return GameContext.get().money_transaction(100)


class Transformator(Factory):
    def __init__(self) -> None:
        inputs = [FactoryInput(Vertex2f(0, 1), direction=Direction.WEST)]
        outputs = [FactoryOutput(Vertex2f(2, 1), direction=Direction.EAST)]
        super().__init__(3, 3, inputs, outputs)


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
