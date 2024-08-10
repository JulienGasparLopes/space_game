from the_crystal_clear.entities.attribute import Attribute
from the_crystal_clear.entities.characteristics import Characteristics
from the_crystal_clear.items.equipment import Equipment
from the_crystal_clear.entities.entity import Entity


class Wizard(Entity):
    def __init__(self) -> None:
        characteristics = Characteristics()
        characteristics.will_power = 100
        characteristics.action_points = 3
        super().__init__(characteristics)
