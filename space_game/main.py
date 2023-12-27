from game_logic import game_manager
from the_space.space_game_manager import SpaceGameManager
from the_factory.factory_game_manager import FactoryGameManager
from the_wanderer.wanderer_game_manager import WandererGameManager


def main() -> None:
    print("Launch app")

    # game_manager = SpaceGameManager()
    # game_manager = FactoryGameManager()
    game_manager = WandererGameManager()

    game_manager.start()


if __name__ == "__main__":
    main()
