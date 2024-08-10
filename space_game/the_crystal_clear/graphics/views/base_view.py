from the_crystal_clear.graphics.menus.base_menu import Menu


class View:
    menus: list[Menu]

    def render(self) -> None:
        for menu in self.menus:
            menu.render()
