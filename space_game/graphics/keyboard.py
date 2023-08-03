# Todo: add compatibility for other keyboard layouts
SPECIAL_KEY_TO_KEYSYM = {
    "ampersand": "1",
    "eacute": "2",
    "quotedbl": "3",
    "apostrophe": "4",
    "parenleft": "5",
    "minus": "6",
    "egrave": "7",
    "underscore": "8",
    "ccedilla": "9",
    "agrave": "0",
}


class Keyboard:
    _key_pressed: dict[str, bool]

    def __init__(self) -> None:
        self._key_pressed = {}

    def _key_press(self, event) -> None:  # type: ignore[no-untyped-def]
        self._key_pressed[event.keysym] = True
        if event.keysym in SPECIAL_KEY_TO_KEYSYM:
            self._key_pressed[SPECIAL_KEY_TO_KEYSYM[event.keysym]] = True

    def _key_release(self, event) -> None:  # type: ignore[no-untyped-def]
        self._key_pressed[event.keysym] = False
        if event.keysym in SPECIAL_KEY_TO_KEYSYM:
            self._key_pressed[SPECIAL_KEY_TO_KEYSYM[event.keysym]] = False

    def is_pressed(self, key: str) -> bool:
        return self._key_pressed.get(key, False)

    def consume_key(self, key: str) -> bool:
        was_pressed = self.is_pressed(key)
        self._key_pressed[key] = False
        return was_pressed
