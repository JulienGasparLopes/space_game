import typing
from game_logic.entity import Entity
from game_logic.tile import TILE_SIZE
from maths.vertex import Vertex2f, Vertex3f
from the_wanderer.path import Path

if typing.TYPE_CHECKING:
    from the_wanderer.task import Task
    from the_wanderer.map import Map


class Wanderer(Entity):
    path: Path | None
    current_task: "Task"

    def __init__(self) -> None:
        super().__init__(Vertex3f(255, 0, 0), TILE_SIZE / 2, TILE_SIZE / 2)
        self.set_position(
            Vertex2f(TILE_SIZE / 2, TILE_SIZE / 2), is_center_position=True
        )
        self.path = None
        self.current_task = None

    def update(self, delta_ms: int, map: "Map") -> None:
        if self.current_task:
            self.current_task.update(self)
        else:
            if map.available_tasks:
                task = map.available_tasks[-1]
                if task.on_accept(self):
                    self.current_task = task
                    map.available_tasks.pop()

        if self.path:
            self.set_tile_position(self.path.positions.pop(0), center=True)
