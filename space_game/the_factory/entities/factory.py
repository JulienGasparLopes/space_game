from typing import Any
from maths.colors import GREEN, RED
from maths.vertex import Vertex2f, Vertex3f
from graphics.renderer import Renderer
from game_logic.tile import TILE_SIZE
from maths.colors import BLUE, ORANGE, YELLOW
from the_factory.entities.entity import Direction, Entity
from the_factory.entities.material import Material


class IOFactory:
    factory: "Factory"
    position: Vertex2f
    color: Vertex3f
    is_input: bool
    is_output: bool

    def __init__(
        self, factory: "Factory", is_input: bool, is_output: bool, position: Vertex2f
    ) -> None:
        self.factory = factory
        self.color = (
            YELLOW if (is_input and is_output) else BLUE if is_input else ORANGE
        )
        self.position = position

    def render(self, renderer: Renderer) -> None:
        pos = self.factory.tile_position.translated(self.position)
        renderer.draw_rect(
            Vertex2f(
                pos.x * TILE_SIZE + (TILE_SIZE // 2 - 8),
                pos.y * TILE_SIZE + (TILE_SIZE // 2 - 8),
            ),
            Vertex2f(
                (pos.x + 1) * TILE_SIZE - (TILE_SIZE // 2 - 8),
                (pos.y + 1) * TILE_SIZE - (TILE_SIZE // 2 - 8),
            ),
            self.color,
        )


class Factory(Entity):
    ios: list[IOFactory]

    def __init__(self, width: int, height: int, ios: list[IOFactory]) -> None:
        super().__init__(GREEN, width * TILE_SIZE, height * TILE_SIZE)
        self.ios = ios

    def render(self, renderer: Renderer) -> None:
        super().render(renderer)
        for io in self.ios:
            io.render(renderer)


class MaterialChute(Factory):
    _new_material_delay: int
    _new_material_counter: int

    def __init__(self, delay: int, direction: Direction = Direction.EAST) -> None:
        super().__init__(1, 1, [IOFactory(self, True, False, direction.vertex)])
        self._direction = direction
        self._new_material_delay = delay
        self._new_material_counter = self._new_material_delay

    def update(self, delta_ms: int, map: Any) -> None:  # TODO: type this
        if self._new_material_counter > 0:
            self._new_material_counter -= delta_ms

        if self._new_material_counter <= 0:
            target_belt = map.get_belt_at_tile_position(
                self.tile_position.translated(self._direction.vertex)
            )
            if target_belt:
                added = target_belt.add_material_to_belt(Material(RED))
                if added:
                    self._new_material_counter = self._new_material_delay

        return super().update(delta_ms, map)


class Transformator(Factory):
    def __init__(self) -> None:
        ios = [
            IOFactory(self, True, False, Vertex2f(-1, 1)),
            IOFactory(self, False, True, Vertex2f(3, 1)),
        ]
        super().__init__(3, 3, ios)


class Fabricator(Factory):
    def __init__(self) -> None:
        ios = [
            IOFactory(self, True, False, Vertex2f(-1, 1)),
            IOFactory(self, True, False, Vertex2f(-1, 3)),
            IOFactory(self, False, True, Vertex2f(5, 2)),
        ]
        super().__init__(5, 5, ios)
