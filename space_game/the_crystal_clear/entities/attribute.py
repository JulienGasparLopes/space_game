class Attribute:
    max_value: float
    current_value: float

    def __init__(self, max_value: float) -> None:
        self.max_value = max_value
        self.current_value = max_value

    def add(self, value: float) -> None:
        self.current_value += value
        if self.current_value > self.max_value:
            self.current_value = self.max_value
        if self.current_value < 0:
            self.current_value = 0
