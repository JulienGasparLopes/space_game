from game_logic.entity import Entity
from game_logic.map import Map
from the_factory.logic.material_type import MaterialType


class Material(Entity):
    _material_type: MaterialType
    _broken: bool

    def __init__(self, material_type: MaterialType) -> None:
        super().__init__(material_type._content, 10, 10)
        self._material_type = material_type
        self._broken = False

    @staticmethod
    def from_type(material_type: MaterialType) -> "Material":
        return Material(material_type)

    def update(self, delta_ms: int, map: Map) -> None:
        return super().update(delta_ms, map)

    @property
    def material_type(self) -> MaterialType:
        return self._material_type
