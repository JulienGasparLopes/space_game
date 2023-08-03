from game_logic.tile import TILE_SIZE
from graphics.renderer_tk.renderer_tk import RendererTk
from maths.vertex import Vertex2f
from the_factory.entities.belt import Belt
from the_factory.entities.delete_plot import DeletePlot
from the_factory.entities.entity import Direction, Entity
from the_factory.context.game_context import GameContext
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from the_factory.maps.map import Map

PATH_LOGIC_ENTITIES = [Belt]
AREA_LOGIC_ENTITIES = [DeletePlot]


def _get_drag_tile_info(
    drag_origin: Vertex2f, current_pos: Vertex2f
) -> tuple[Vertex2f, Vertex2f, Direction, Direction, list[int], list[int]]:
    drag_tile_origin = drag_origin.divided(TILE_SIZE, floor=True)
    current_tile_pos = current_pos.divided(TILE_SIZE, floor=True)
    x_dir = Direction.EAST if drag_origin.x < current_pos.x else Direction.WEST
    y_dir = Direction.SOUTH if drag_origin.y < current_pos.y else Direction.NORTH
    xs = range(drag_tile_origin.x, current_tile_pos.x + x_dir.vertex.x, x_dir.vertex.x)
    ys = range(drag_tile_origin.y, current_tile_pos.y + y_dir.vertex.y, y_dir.vertex.y)
    return drag_tile_origin, current_tile_pos, x_dir, y_dir, list(xs), list(ys)


class BuildHelper:
    _map: "Map"
    _build_ghosts: list[Entity] = []

    def __init__(self, map: "Map") -> None:
        self._map = map

    def update_ghosts(self, renderer: RendererTk) -> None:
        build_entity_type = GameContext.get().selected_build_entity_type
        if not build_entity_type:
            return
        self._build_ghosts = []

        current_pos = renderer.mouse.get_relative_position(self._map)
        drag_origin = renderer.mouse.get_relative_drag_origin(self._map)

        if PATH_LOGIC_ENTITIES.count(build_entity_type) > 0 and drag_origin is not None:
            (tile_orig, tile_target, x_dir, y_dir, xs, ys) = _get_drag_tile_info(
                drag_origin, current_pos
            )
            for x in xs[:-1] if len(ys) > 1 else xs:
                entity = build_entity_type()
                entity.set_tile_position(Vertex2f(x, tile_orig.y))
                entity.set_direction(x_dir)
                self._build_ghosts.append(entity)
            if len(ys) > 1:
                for y in ys:
                    entity = build_entity_type()
                    entity.set_tile_position(Vertex2f(tile_target.x, y))
                    entity.set_direction(y_dir)
                    self._build_ghosts.append(entity)
        elif (
            AREA_LOGIC_ENTITIES.count(build_entity_type) > 0 and drag_origin is not None
        ):
            (tile_orig, tile_target, x_dir, y_dir, xs, ys) = _get_drag_tile_info(
                drag_origin, current_pos
            )
            for x in xs:
                for y in ys:
                    entity = build_entity_type()
                    entity.set_tile_position(Vertex2f(x, y))
                    self._build_ghosts.append(entity)
        else:
            if len(self._build_ghosts) == 0:
                self._build_ghosts.append(build_entity_type())
            self._build_ghosts[0].set_position(
                current_pos, is_center_position=True, bound_to_tile=True
            )

    def render(self, renderer: RendererTk) -> None:
        self.update_ghosts(renderer)

        last_z_index = renderer.z_index
        renderer.set_z_index(last_z_index + 10)
        for entity in self._build_ghosts:
            entity.render(renderer)
        renderer.set_z_index(last_z_index)

    def on_mouse_click(self, position: Vertex2f) -> bool:
        if len(self._build_ghosts) == 0:
            return False

        elif isinstance(self._build_ghosts[0], DeletePlot):
            for delete_plot in self._build_ghosts:
                for entity in self._map.entities:
                    if entity.collides(delete_plot, strict=False):
                        self._map.entities.remove(entity)
                        GameContext.get().select_build_entity_type()
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
                    GameContext.get().select_build_entity_type()

        self._build_ghosts = []
        return False
