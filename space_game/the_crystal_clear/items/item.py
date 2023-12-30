from enum import Enum
from the_crystal_clear.items.affixe import Affixe


class Rarity(Enum):
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    EPIC = 4
    LEGENDARY = 5


class Item:
    suffixes: list[Affixe]
    prefixes: list[Affixe]

    rarity: Rarity
