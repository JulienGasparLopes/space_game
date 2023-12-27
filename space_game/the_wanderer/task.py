from abc import ABCMeta, abstractmethod
from the_wanderer.wanderer import Wanderer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from the_wanderer.map import Map
    from the_wanderer.stock_pile import StockPile


class Task(metaclass=ABCMeta):
    map: "Map"

    def __init__(self, map: "Map") -> None:
        self.map = map

    def update(self, wanderer: Wanderer) -> bool:
        if self.is_complete(wanderer):
            self.on_finish(wanderer)
            return True
        return False

    @abstractmethod
    def is_complete(self, wanderer: Wanderer) -> bool:
        ...

    @abstractmethod
    def on_accept(self, wanderer: Wanderer) -> bool:
        ...

    @abstractmethod
    def on_finish(self, wanderer: Wanderer) -> bool:
        ...


class TaskGetItemToMove(Task):
    stock_pile_origin: "StockPile"
    stock_pile_destination: "StockPile"

    def __init__(
        self,
        map: "Map",
        stock_pile_origin: "StockPile",
        stock_pile_destination: "StockPile",
    ) -> None:
        super().__init__(map)
        self.stock_pile_origin = stock_pile_origin
        self.stock_pile_destination = stock_pile_destination

    def is_complete(self, wanderer: Wanderer) -> bool:
        return wanderer.tile_position == self.stock_pile_origin.tile_position

    def on_accept(self, wanderer: Wanderer) -> bool:
        path = self.map.find_path(
            wanderer.tile_position, self.stock_pile_origin.tile_position
        )
        if path:
            wanderer.path = path
            return True
        return False

    def on_finish(self, wanderer: Wanderer) -> bool:
        task = TaskDeliverItemToMove(self.map, self.stock_pile_destination)
        if task.on_accept(wanderer):
            wanderer.current_task = task
            self.stock_pile_origin.pop_item()
            if self.stock_pile_origin.stock > 0:
                self.map.available_tasks.append(
                    TaskGetItemToMove(
                        self.map, self.stock_pile_origin, self.stock_pile_destination
                    )
                )
            return True
        return False


class TaskDeliverItemToMove(Task):
    stock_pile_destination: "StockPile"

    def __init__(
        self,
        map: "Map",
        stock_pile_destination: "StockPile",
    ) -> None:
        super().__init__(map)
        self.stock_pile_destination = stock_pile_destination

    def is_complete(self, wanderer: Wanderer) -> bool:
        return wanderer.tile_position == self.stock_pile_destination.tile_position

    def on_accept(self, wanderer: Wanderer) -> bool:
        path = self.map.find_path(
            wanderer.tile_position, self.stock_pile_destination.tile_position
        )
        if path:
            wanderer.path = path
            return True
        return False

    def on_finish(self, wanderer: Wanderer) -> bool:
        self.stock_pile_destination.put_item()
        wanderer.current_task = None
        return True
