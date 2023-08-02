from the_factory.entities.entity import Entity


class BuildObjectInfo:
    _entity_type: type[Entity]
    _mono_build: bool

    def __init__(self, entity_type: type[Entity], mono_build: bool = True) -> None:
        self._entity_type = entity_type
        self._mono_build = mono_build

    @property
    def entity_type(self) -> type[Entity]:
        return self._entity_type

    @property
    def mono_build(self) -> bool:
        return self._mono_build
