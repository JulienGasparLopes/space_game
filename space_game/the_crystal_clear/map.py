from game_logic.map import Map as MapBase
from game_logic.tile import Tile
from graphics.mouse import MouseButton
from graphics.renderer import Renderer
from maths.vertex import Vertex2f, Vertex3f
from the_crystal_clear.entities.crystal import Crystal
from the_crystal_clear.entities.wizard import Wizard
from the_crystal_clear.graphic_helpers import render_gauge
from the_crystal_clear.items.affixe import PrefixWillPowerT2
from the_crystal_clear.items.item import Item

GROUND = Tile(Vertex3f(0, 255, 0), False)
WALL = Tile(Vertex3f(0, 0, 255), True)


class Map(MapBase):
    player: Wizard
    crystal: Crystal

    def __init__(self) -> None:
        super().__init__(0, 0)
        wizard = Wizard()
        wizard.set_position(Vertex2f(200, 300))
        helmet = Item()
        helmet.prefixes.append(PrefixWillPowerT2())
        wizard.equipment.helmet = helmet
        wizard.calculate_characteristics()

        self.crystal = Crystal()
        self.crystal.set_position(Vertex2f(200, 100))

        self.player = wizard
        self.entities.append(wizard)
        self.entities.append(self.crystal)

    def on_mouse_click(self, position: Vertex2f, mouse_button: MouseButton) -> bool:
        return False

    def render(self, renderer: Renderer) -> None:
        super().render(renderer)
        position = Vertex2f(50, 400)
        render_gauge(
            renderer,
            self.player.action_points.current_value,
            self.player.action_points.max_value,
            position,
            show_value=False,
        )
        renderer.draw_text(
            position.translated(Vertex2f(5, 30)),
            str(self.player.action_points.available_points),
            Vertex3f(255, 255, 255),
        )
