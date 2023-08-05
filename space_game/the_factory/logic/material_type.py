from graphics.renderer import Image
from maths.colors import BLUE, CYAN, GREY, YELLOW
from maths.vertex import Vertex3f

_ANY_MATERIAL_NAME = "Any"


class MaterialType:
    _name: str
    _content: Vertex3f | Image

    def __init__(self, name: str, content: Vertex3f | Image) -> None:
        self._name = name
        self._content = content

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, MaterialType):
            return False
        if self._name == _ANY_MATERIAL_NAME or __value._name == _ANY_MATERIAL_NAME:
            return True
        return self._name == __value._name

    def __hash__(self) -> int:
        return hash(self._name)


ANY_MATERIAL = MaterialType("Any", GREY)

IRON = MaterialType("Iron", GREY)

BOLT = MaterialType("Bolt", BLUE)
SHEET = MaterialType("Sheet", YELLOW)

HEAVY_PLATE = MaterialType("Heavy Plate", CYAN)
