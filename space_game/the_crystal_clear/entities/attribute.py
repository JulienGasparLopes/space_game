class Attribute:
    max_value: float
    current_value: float

    regen_per_second: float

    def __init__(self, max_value: float, regen_per_second: float = 0) -> None:
        self.max_value = max_value
        self.current_value = max_value

        self.regen_per_second = regen_per_second

    def add(self, value: float) -> None:
        self.current_value += value
        if self.current_value > self.max_value:
            self.current_value = self.max_value
        if self.current_value < 0:
            self.current_value = 0

        if self.current_value == self.max_value:
            self._on_max_value()

    def set_max_value(self, max_value: float) -> None:
        self.max_value = max_value
        if self.current_value > max_value:
            self.current_value = max_value

    def update(self, delta_ms: int) -> None:
        self.add(self.regen_per_second * delta_ms / 1000.0)

    def _on_max_value(self) -> None:
        pass
