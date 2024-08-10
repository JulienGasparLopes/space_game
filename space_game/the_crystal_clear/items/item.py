from enum import Enum
from the_crystal_clear.entities.characteristics import (
    Characteristics,
    MultiplierCharacteristics,
)
from the_crystal_clear.items.affixe import Affixe


class Rarity(Enum):
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    EPIC = 4
    LEGENDARY = 5


class Item:
    suffixes: list[Affixe] = []
    prefixes: list[Affixe] = []

    rarity: Rarity

    @property
    def affixes(self) -> list[Affixe]:
        return self.suffixes + self.prefixes

    def update_characteristics(
        self,
        characteristics: Characteristics,
        multiplier_characteristics: MultiplierCharacteristics,
    ) -> None:
        for affixe in self.affixes:
            affixe.update_characteristics(characteristics, multiplier_characteristics)
