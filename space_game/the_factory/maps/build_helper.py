from game_logic.tile import TILE_SIZE
from graphics.renderer_tk.renderer_tk import RendererTk
from maths.vertex import Vertex2f
from the_factory.entities.delete_plot import DeletePlot
from the_factory.entities.entity import Direction, Entity
from the_factory.context.game_context import GameContext
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from the_factory.maps.map import Map


class BuildHelper:
    _map: "Map"
    _build_ghosts: list[Entity] = []

    def __init__(self, map: "Map") -> None:
        self._map = map

    def update_ghosts(self, renderer: RendererTk) -> None:
        build_info = GameContext.get().build_info
        if not build_info:
            return
        self._build_ghosts = []

        current_pos = renderer.mouse.get_relative_position(self._map)
        drag_origin = renderer.mouse.get_relative_drag_origin(self._map)
        if build_info.mono_build or not drag_origin:
            if len(self._build_ghosts) == 0:
                self._build_ghosts.append(build_info.entity_type())
            self._build_ghosts[0].set_position(
                current_pos, is_center_position=True, bound_to_tile=True
            )
        else:
            x_dir = Direction.EAST if drag_origin.x < current_pos.x else Direction.WEST
            y_dir = (
                Direction.SOUTH if drag_origin.y < current_pos.y else Direction.NORTH
            )
            drag_tile_origin = drag_origin.divided(TILE_SIZE, floor=True)
            current_tile_pos = current_pos.divided(TILE_SIZE, floor=True)
            xs = range(
                drag_tile_origin.x, current_tile_pos.x + x_dir.vertex.x, x_dir.vertex.x
            )
            ys = range(
                drag_tile_origin.y, current_tile_pos.y + y_dir.vertex.y, y_dir.vertex.y
            )
            for x in xs[:-1] if len(ys) > 1 else xs:
                entity = build_info.entity_type()
                entity.set_tile_position(Vertex2f(x, drag_origin.y // TILE_SIZE))
                entity.set_direction(x_dir)
                self._build_ghosts.append(entity)
            if len(ys) > 1:
                for y in ys:
                    entity = build_info.entity_type()
                    entity.set_tile_position(Vertex2f(current_tile_pos.x, y))
                    entity.set_direction(y_dir)
                    self._build_ghosts.append(entity)

    def render(self, renderer: RendererTk) -> None:
        self.update_ghosts(renderer)
        if renderer.mouse._drag_origin:
            print("coucou")

        last_z_index = renderer.z_index
        renderer.set_z_index(last_z_index + 10)
        for entity in self._build_ghosts:
            entity.render(renderer)
        renderer.set_z_index(last_z_index)

    def on_mouse_click(self, position: Vertex2f) -> bool:
        if len(self._build_ghosts) == 0:
            return False

        elif isinstance(self._build_ghosts[0], DeletePlot):
            for entity in self._map.entities:
                if entity.collides(self._build_ghosts[0], strict=False):
                    self._map.entities.remove(entity)
                    GameContext.get().set_build_info()
        else:
            for entity in self._build_ghosts:
                collides = any(
                    [
                        e.collides(entity, strict=False)
                        for e in self._map.entities
                        if e != entity
                    ]
                )
                if not collides:
                    self._map.entities.append(entity)
                    GameContext.get().set_build_info()

        self._build_ghosts = []
        return False
