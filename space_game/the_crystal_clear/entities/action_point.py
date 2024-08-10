from the_crystal_clear.entities.attribute import Attribute


class ActionPointAttribute(Attribute):
    max_action_points: int
    available_points: int

    def __init__(self, max_action_points: int, regen_per_second: float) -> None:
        super().__init__(1, regen_per_second)
        self.max_action_points = max_action_points
        self.available_points = 0

    def _on_max_value(self) -> None:
        if self.available_points < self.max_action_points:
            self.available_points += 1
            self.current_value = 0
