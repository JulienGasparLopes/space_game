from typing import cast
from game_logic.map import Map as BaseMap
from the_factory.entities.belt import Belt, Direction
from the_factory.entities.factory import MaterialChute, Transformator, Fabricator
from maths.vertex import Vertex2f
from graphics.renderer import Renderer
from the_factory.entities.material import Material
from maths.colors import RED


class Map(BaseMap):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)

        chute1 = MaterialChute(250)
        chute1.set_tile_position(Vertex2f(0, 3))
        self.entities.append(chute1)

        chute2 = MaterialChute(1500)
        chute2.set_tile_position(Vertex2f(1, 6))
        self.entities.append(chute2)

        transfo1 = Transformator()
        transfo1.set_tile_position(Vertex2f(6, 2))
        self.entities.append(transfo1)

        transfo2 = Transformator()
        transfo2.set_tile_position(Vertex2f(6, 8))
        self.entities.append(transfo2)

        fab1 = Fabricator()
        fab1.set_tile_position(Vertex2f(14, 4))
        self.entities.append(fab1)

        def create_belt(direction: Direction, position: Vertex2f) -> None:
            belt = Belt(direction, 60 * 5)
            belt.set_tile_position(position)
            self.entities.append(belt)

        create_belt(Direction.SOUTH, Vertex2f(1, 3))
        create_belt(Direction.SOUTH, Vertex2f(1, 4))
        create_belt(Direction.EAST, Vertex2f(1, 5))
        create_belt(Direction.EAST, Vertex2f(2, 5))
        create_belt(Direction.NORTH, Vertex2f(3, 5))
        create_belt(Direction.WEST, Vertex2f(3, 4))
        create_belt(Direction.NORTH, Vertex2f(2, 4))

        for i in range(2, 6):
            create_belt(Direction.EAST, Vertex2f(i, 3))

    def render(self, renderer: Renderer) -> None:
        self.entities.sort(key=lambda e: 0 if type(e) == Belt else 1)
        return super().render(renderer)

    def get_belt_at_tile_position(self, tile_position: Vertex2f) -> Belt | None:
        possible_targets = [
            e for e in self.get_entities_at_tile(tile_position) if type(e) == Belt
        ]
        if len(possible_targets) == 1:
            return cast(Belt, possible_targets[0])
        return None
