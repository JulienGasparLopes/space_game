from typing import Any
from graphics.renderer_tk import RendererTk
from game_logic.game_manager import GameManager


def main() -> None:
    print("Launch app")
    game_manager = GameManager()
    game_manager.start()


if __name__ == "__main__":
    main()
