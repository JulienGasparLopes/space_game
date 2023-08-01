class Keyboard:
    _key_pressed: dict[str, bool]

    def __init__(self) -> None:
        self._key_pressed = {}

    def _key_press(self, event) -> None:  # type: ignore[no-untyped-def]
        self._key_pressed[event.keysym] = True

    def _key_release(self, event) -> None:  # type: ignore[no-untyped-def]
        self._key_pressed[event.keysym] = False

    def is_pressed(self, key: str) -> bool:
        return self._key_pressed.get(key, False)
