from maths.vertex import Vertex2f
from the_factory.entities.belt import Belt
from game_logic.entity import Direction
from the_factory.entities.factory import (
    Fabricator,
    MaterialChute,
    MaterialSeller,
    Transformator,
)
from the_factory.maps.map import Map
from the_factory.logic.recipe import BOLT_BASIC, SHEET_BASIC, HEAVY_PLATE_BASIC


class MapTest(Map):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        # self.minimal_map()
        self.full_map()

    def minimal_map(self) -> None:
        chute1 = MaterialChute(250)
        chute1.set_tile_position(Vertex2f(0, 3))
        self.entities.append(chute1)

        def create_belt(direction: Direction, position: Vertex2f) -> None:
            belt = Belt(direction)
            belt.set_tile_position(position)
            self.entities.append(belt)

        create_belt(Direction.EAST, Vertex2f(1, 3))
        create_belt(Direction.EAST, Vertex2f(2, 3))
        create_belt(Direction.EAST, Vertex2f(3, 3))

        transfo1 = Transformator()
        transfo1.set_recipe(BOLT_BASIC)
        transfo1.set_tile_position(Vertex2f(4, 2))
        self.entities.append(transfo1)

    def full_map(self) -> None:
        chute1 = MaterialChute(250)
        chute1.set_tile_position(Vertex2f(0, 3))
        self.entities.append(chute1)

        chute2 = MaterialChute(400)
        chute2.set_tile_position(Vertex2f(1, 9))
        self.entities.append(chute2)

        chute3 = MaterialChute(250)
        chute3.set_tile_position(Vertex2f(1, 12))
        self.entities.append(chute3)

        chute4 = MaterialChute(350)
        chute4.set_tile_position(Vertex2f(1, 15))
        self.entities.append(chute4)

        seller1 = MaterialSeller(300, Direction.WEST)
        seller1.set_tile_position(Vertex2f(20, 12))
        self.entities.append(seller1)

        transfo1 = Transformator()
        transfo1.set_recipe(BOLT_BASIC)
        transfo1.set_tile_position(Vertex2f(6, 2))
        self.entities.append(transfo1)

        transfo2 = Transformator()
        transfo2.set_recipe(SHEET_BASIC)
        transfo2.set_tile_position(Vertex2f(6, 8))
        self.entities.append(transfo2)

        fab1 = Fabricator()
        fab1.set_recipe(HEAVY_PLATE_BASIC)
        fab1.set_tile_position(Vertex2f(14, 4))
        self.entities.append(fab1)

        def create_belt(direction: Direction, position: Vertex2f) -> None:
            belt = Belt(direction)
            belt.set_tile_position(position)
            self.entities.append(belt)

        # chute1 to transfo1
        for i in range(1, 6):
            create_belt(Direction.EAST, Vertex2f(i, 3))

        # chute2 to transfo2
        for i in range(2, 6):
            create_belt(Direction.EAST, Vertex2f(i, 9))

        # transfo1 to fab1
        create_belt(Direction.SOUTH, Vertex2f(9, 3))
        create_belt(Direction.SOUTH, Vertex2f(9, 4))
        for i in range(9, 14):
            create_belt(Direction.EAST, Vertex2f(i, 5))

        # transfo2 to fab1
        create_belt(Direction.NORTH, Vertex2f(9, 8))
        create_belt(Direction.NORTH, Vertex2f(9, 9))
        for i in range(9, 14):
            create_belt(Direction.EAST, Vertex2f(i, 7))

        # fab1 to seller1
        for i in range(6, 13):
            create_belt(Direction.SOUTH, Vertex2f(19, i))
