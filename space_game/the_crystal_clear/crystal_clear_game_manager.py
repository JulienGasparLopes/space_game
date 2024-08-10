from graphics.button import Button
from maths.vertex import Vertex2f
from the_crystal_clear.graphics.views.base_view import View
from the_crystal_clear.map import Map
from game_logic.game_manager import GameManager


class CrystalClearGameManager(GameManager):
    current_map: Map
    current_view: View

    def __init__(self) -> None:
        super().__init__()

        map = Map()
        self.set_current_map(map)

        self.graphic_manager.add_component(
            SkillButton(Vertex2f(20, 250), map, Skill(1, 90))
        )
        self.graphic_manager.add_component(
            SkillButton(Vertex2f(50, 250), map, Skill(3, 560))
        )

    def set_current_view(self, view: View) -> None:
        self.graphic_manager.clear()
        for menu in view.menus:
            for component in menu.components:
                self.graphic_manager.add_component(component)

    def update(self, delta_ms: int) -> None:
        ...


class Skill:
    cost: int
    damages: int

    def __init__(self, cost: int, damages: int) -> None:
        self.cost = cost
        self.damages = damages


class SkillButton(Button):
    map: Map
    skill: Skill

    def __init__(self, position: Vertex2f, map: Map, skill: Skill) -> None:
        super().__init__(position, Vertex2f(40, 40))
        self.map = map
        self.skill = skill

    def action(self) -> None:
        if self.map.player.action_points.available_points >= self.skill.cost:
            self.map.player.action_points.available_points -= self.skill.cost
            self.map.crystal.will_power.add(-self.skill.damages)
