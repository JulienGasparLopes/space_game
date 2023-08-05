from the_factory.logic.material_type import SHEET, MaterialType, IRON, BOLT, HEAVY_PLATE


class RecipeLine:
    _material_type: MaterialType
    _amount: int

    def __init__(self, material_type: MaterialType, amount: int) -> None:
        self._material_type = material_type
        self._amount = amount

    @property
    def material_type(self) -> MaterialType:
        return self._material_type

    @property
    def amount(self) -> int:
        return self._amount


class Recipe:
    _inputs: list[RecipeLine]
    _outputs: list[RecipeLine]
    _processing_time_ms: int

    def __init__(
        self, input: list[RecipeLine], output: list[RecipeLine], processing_time_ms: int
    ) -> None:
        self._inputs = input
        self._outputs = output
        self._processing_time_ms = processing_time_ms

    @property
    def processing_time_ms(self) -> int:
        return self._processing_time_ms

    def get_input_line(self, index: int) -> RecipeLine:
        return self._inputs[index]

    def get_output_line(self, index: int) -> RecipeLine:
        return self._outputs[index]


BOLT_BASIC = Recipe([RecipeLine(IRON, 1)], [RecipeLine(BOLT, 1)], 200)
SHEET_BASIC = Recipe([RecipeLine(IRON, 1)], [RecipeLine(SHEET, 1)], 300)

HEAVY_PLATE_BASIC = Recipe(
    [RecipeLine(BOLT, 2), RecipeLine(SHEET, 1)],
    [RecipeLine(HEAVY_PLATE, 1)],
    600,
)
