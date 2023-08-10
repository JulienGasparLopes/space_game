from abc import ABC, abstractmethod
from game_logic.entity import Direction, Entity

from graphics.renderer import Renderer
from the_factory.entities.material import Material
from the_factory.logic.material_type import MaterialType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from the_factory.maps.map import Map


class BaseBelt(Entity, ABC):
    @abstractmethod
    def render(self, renderer: Renderer, z_index: int = 0) -> None:
        super().render(renderer, z_index)

    @abstractmethod
    def accepts_material_from(self, direction: Direction) -> bool:
        ...

    @abstractmethod
    def insert_material(
        self, material: Material, direction: Direction | None = None
    ) -> bool:
        ...

    @abstractmethod
    def pop_material(self) -> Material | None:
        ...

    @abstractmethod
    def get_material_type(self) -> MaterialType | None:
        ...

    @abstractmethod
    def update(self, delta_ms: int, map: "Map") -> None:
        super().update(delta_ms, map)

    @abstractmethod
    def set_direction(self, direction: Direction) -> None:
        super().set_direction(direction)
