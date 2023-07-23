from the_space.space_game_manager import SpaceGameManager
from the_factory.factory_game_manager import FactoryGameManager


def main() -> None:
    print("Launch app")

    # game_manager = SpaceGameManager()
    # game_manager.start()

    game_manager = FactoryGameManager()
    game_manager.start()


if __name__ == "__main__":
    main()
