from typing import cast
from game_logic.map import Map as BaseMap
from graphics.renderer_tk import RendererTk
from the_factory.entities.belt import Belt, Direction
from the_factory.entities.factory import (
    MaterialChute,
    MaterialSeller,
    Transformator,
    Fabricator,
)
from maths.vertex import Vertex2f
from the_factory.game_context import GameContext


class Map(BaseMap):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)

        chute1 = MaterialChute(250)
        chute1.set_tile_position(Vertex2f(0, 3))
        self.entities.append(chute1)

        chute2 = MaterialChute(400)
        chute2.set_tile_position(Vertex2f(1, 9))
        self.entities.append(chute2)

        seller1 = MaterialSeller(300, Direction.WEST)
        seller1.set_tile_position(Vertex2f(20, 12))
        self.entities.append(seller1)

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

        # chute1 to transfo1
        create_belt(Direction.SOUTH, Vertex2f(1, 3))
        create_belt(Direction.SOUTH, Vertex2f(1, 4))
        create_belt(Direction.EAST, Vertex2f(1, 5))
        create_belt(Direction.EAST, Vertex2f(2, 5))
        create_belt(Direction.NORTH, Vertex2f(3, 5))
        create_belt(Direction.WEST, Vertex2f(3, 4))
        create_belt(Direction.NORTH, Vertex2f(2, 4))
        for i in range(2, 6):
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

    def render(self, renderer: RendererTk) -> None:
        if selected_entity := GameContext.get().selected_entity:
            last_z_index = renderer.z_index
            selected_entity.set_position(
                renderer.mouse.get_relative_position(self),
                is_center_position=True,
                bound_to_tile=True,
            )
            renderer.set_z_index(last_z_index + 10)
            selected_entity.render(renderer)
            renderer.set_z_index(last_z_index)
        return super().render(renderer)

    def get_belt_at_tile_position(self, tile_position: Vertex2f) -> Belt | None:
        possible_targets = [
            e for e in self.get_entities_at_tile(tile_position) if type(e) == Belt
        ]
        if len(possible_targets) == 1:
            return cast(Belt, possible_targets[0])
        return None

    def on_mouse_click(self, position: Vertex2f) -> bool:
        game_context = GameContext.get()
        if selected_entity := game_context.selected_entity:
            collides = any(
                [
                    e.collides(selected_entity, strict=False)
                    for e in self.entities
                    if e != selected_entity
                ]
            )
            if not collides:
                self.entities.append(selected_entity)
                game_context.set_select_entity()
        return False
