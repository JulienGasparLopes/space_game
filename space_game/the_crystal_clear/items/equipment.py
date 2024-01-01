from the_crystal_clear.items.item import Item


class Equipment:
    helmet: Item | None = None
    chestplate: Item | None = None

    @property
    def items(self) -> list[Item]:
        return [i for i in [self.helmet, self.chestplate] if i is not None]
