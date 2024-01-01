from abc import ABCMeta, abstractmethod
from enum import Enum
from random import random
from the_crystal_clear.entities.characteristics import (
    Characteristics,
    MultiplierCharacteristics,
)


class AffixeType(Enum):
    SUFFIX = 1
    PREFIX = 2


class Affixe(metaclass=ABCMeta):
    affixe_type: AffixeType
    tier: int
    min_value: float
    max_value: float
    name: str
    description: str

    precision: int = 0

    value: float

    def __init__(self) -> None:
        self.value = (
            int(
                (self.min_value + random() * (self.max_value - self.min_value))
                * 10**self.precision
            )
            / 10**self.precision
        )
        print(f"Created {self.name} with value {self.value}")

    @abstractmethod
    def update_characteristics(
        self,
        caracteristics: Characteristics,
        multiplier_characteristics: MultiplierCharacteristics,
    ) -> None:
        ...


class PrefixWillPowerT1(Affixe):
    affixe_type = AffixeType.PREFIX
    tier = 1
    min_value = 40
    max_value = 50
    name = "Will Power T1"
    description = "Flat will power"

    def update_characteristics(
        self,
        caracteristics: Characteristics,
        multiplier_characteristics: MultiplierCharacteristics,
    ) -> None:
        caracteristics.will_power += self.value


class PrefixWillPowerT2(Affixe):
    affixe_type = AffixeType.PREFIX
    tier = 2
    min_value = 30
    max_value = 39
    name = "Will Power T2"
    description = "Flat will power"

    def update_characteristics(
        self,
        caracteristics: Characteristics,
        multiplier_characteristics: MultiplierCharacteristics,
    ) -> None:
        caracteristics.will_power += self.value


class SuffixIncreasedWillPowerT1(Affixe):
    affixe_type = AffixeType.SUFFIX
    tier = 1
    min_value = 10
    max_value = 15
    name = "Increased Will Power T1"
    description = "Increased will power"

    def update_characteristics(
        self,
        caracteristics: Characteristics,
        multiplier_characteristics: MultiplierCharacteristics,
    ) -> None:
        multiplier_characteristics.increased_will_power += self.value
