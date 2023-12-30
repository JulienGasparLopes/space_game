from the_crystal_clear.entities.attribute import Attribute
from the_crystal_clear.items.equipment import Equipment
from the_crystal_clear.entities.entity import Entity


class Wizard(Entity):
    equipment: Equipment

    def __init__(self) -> None:
        super().__init__()
        self.equipment = Equipment()
        self.will_power = Attribute(100)
