from turtle import distance
from game_logic.entity import Direction
from maths.vertex import Vertex2f


class Path:
    positions: list[Vertex2f]
    destination: Vertex2f
    distance: float

    def __init__(self, positions: list[Vertex2f], destination: Vertex2f) -> None:
        self.positions = positions
        self.destination = destination
        self.distance = self.destination.translated(self.end.inverted()).norm

    @property
    def start(self) -> Vertex2f:
        return self.positions[0]

    @property
    def end(self) -> Vertex2f:
        return self.positions[-1]

    def __len__(self) -> int:
        return len(self.positions)

    def new_path(self, direction: Direction) -> "Path":
        return Path(
            self.positions + [self.end.translated(direction.vertex)], self.destination
        )

    def get_neighbours(self) -> list["Path"]:
        return [self.new_path(direction) for direction in Direction]
