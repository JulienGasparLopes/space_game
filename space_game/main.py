from game_logic import game_manager
from the_space.space_game_manager import SpaceGameManager
from the_factory.factory_game_manager import FactoryGameManager
from the_wanderer.wanderer_game_manager import WandererGameManager
from the_crystal_clear.crystal_clear_game_manager import CrystalClearGameManager


def main() -> None:
    print("Launch app")

    # game_manager = SpaceGameManager()
    # game_manager = FactoryGameManager()
    # game_manager = WandererGameManager()
    game_manager = CrystalClearGameManager()

    game_manager.start()


if __name__ == "__main__":
    main()
