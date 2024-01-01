from graphics.renderer import Renderer
from maths.vertex import Vertex2f, Vertex3f
from the_crystal_clear.entities.action_point import ActionPointAttribute
from the_crystal_clear.entities.attribute import Attribute
from game_logic.entity import Entity as EntityBase
from game_logic.map import Map
from the_crystal_clear.entities.characteristics import (
    Characteristics,
    MultiplierCharacteristics,
)
from the_crystal_clear.graphic_helpers import render_gauge
from the_crystal_clear.items.equipment import Equipment


class Entity(EntityBase):
    # Base characteristics, equipments and modifiers
    characteristics: Characteristics
    equipment: Equipment

    # Real time attributes values
    action_points: ActionPointAttribute
    will_power: Attribute

    @property
    def attributes(self) -> list[Attribute]:
        return [self.action_points, self.will_power]

    def __init__(self, caracterisitcs: Characteristics) -> None:
        super().__init__(Vertex3f(0, 0, 255))

        self.characteristics = caracterisitcs
        self.equipment = Equipment()

        self.will_power = Attribute(10000, 6)
        self.action_points = ActionPointAttribute(100000, 1.5)
        self.calculate_characteristics()

        self.action_points.current_value = 0

    def calculate_characteristics(self) -> None:
        characteristics = self.characteristics.clone()
        multiplier_characteristics = MultiplierCharacteristics()
        for item in self.equipment.items:
            item.update_characteristics(characteristics, multiplier_characteristics)
        multiplier_characteristics.apply(characteristics)

        self.will_power.set_max_value(characteristics.will_power)
        self.action_points.max_action_points = characteristics.action_points

    def update(self, delta_ms: int, map: "Map") -> None:
        if self.will_power.current_value == 0:
            return

        for attribute in self.attributes:
            attribute.update(delta_ms)

    def render(self, renderer: Renderer, z_index: int = 0) -> None:
        super().render(renderer, z_index)
        render_gauge(
            renderer,
            self.will_power.current_value,
            self.will_power.max_value,
            self.position.translated(Vertex2f(0, -30)),
        )
