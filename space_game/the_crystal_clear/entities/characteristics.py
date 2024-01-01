class Characteristics:
    will_power: float = 0
    mana: float = 0

    action_points: int = 0

    def clone(self) -> "Characteristics":
        caracteristics = Characteristics()
        caracteristics.will_power = self.will_power
        caracteristics.mana = self.mana
        caracteristics.action_points = self.action_points
        return caracteristics


class MultiplierCharacteristics:
    increased_will_power: float = 1
    increased_mana: float = 1

    more_will_power: float = 1
    more_mana: float = 1

    def apply(self, characteristics: Characteristics) -> None:
        characteristics.will_power *= self.increased_will_power
        characteristics.will_power *= self.more_will_power

        characteristics.mana *= self.increased_mana
        characteristics.mana *= self.more_mana
