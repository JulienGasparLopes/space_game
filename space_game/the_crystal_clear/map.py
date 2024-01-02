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
from graphics.renderer_tk.renderer_tk import Image

GROUND = Tile(Vertex3f(0, 255, 0), False)
WALL = Tile(Vertex3f(0, 0, 255), True)

BIG_TREE = Image("space_game/the_crystal_clear/images/tree.png", width=300, height=300)
MEDIUM_TREE = Image(
    "space_game/the_crystal_clear/images/tree.png", width=230, height=230
)
CRYSTAL = Image(
    "space_game/the_crystal_clear/images/crystal.png", width=150, height=250
)


class Map(MapBase):
    player: Wizard
    crystal: Crystal

    def __init__(self) -> None:
        super().__init__(0, 0)
        wizard = Wizard()
        wizard.set_position(Vertex2f(550, 450))
        helmet = Item()
        helmet.prefixes.append(PrefixWillPowerT2())
        wizard.equipment.helmet = helmet
        wizard.calculate_characteristics()

        self.crystal = Crystal()
        self.crystal.set_position(Vertex2f(350, 200))
        self.crystal.content = CRYSTAL

        self.player = wizard
        self.entities.append(wizard)
        self.entities.append(self.crystal)

    def on_mouse_click(self, position: Vertex2f, mouse_button: MouseButton) -> bool:
        return False

    def render(self, renderer: Renderer) -> None:
        position = Vertex2f(600, 540)
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
        renderer.draw_rect(Vertex2f(0, 0), Vertex2f(0, 0), MEDIUM_TREE)
        renderer.draw_rect(Vertex2f(200, 50), Vertex2f(0, 0), MEDIUM_TREE)
        renderer.draw_rect(Vertex2f(320, 30), Vertex2f(0, 0), MEDIUM_TREE)
        renderer.draw_rect(Vertex2f(540, 70), Vertex2f(0, 0), MEDIUM_TREE)

        renderer.draw_rect(Vertex2f(680, 170), Vertex2f(0, 0), BIG_TREE)
        renderer.draw_rect(Vertex2f(-10, 170), Vertex2f(0, 0), BIG_TREE)
        renderer.draw_rect(Vertex2f(40, 380), Vertex2f(0, 0), BIG_TREE)

        super().render(renderer)
