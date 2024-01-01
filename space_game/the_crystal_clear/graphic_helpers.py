from graphics.renderer import Renderer
from maths.vertex import Vertex2f, Vertex3f


def render_gauge(
    renderer: Renderer,
    value: float,
    max_value: float,
    position: Vertex2f,
    show_value: bool = True,
) -> None:
    renderer.draw_rect(
        position,
        Vertex2f(position.x + 100, position.y + 20),
        Vertex3f(255, 0, 0),
    )
    renderer.draw_rect(
        Vertex2f(position.x + 2, position.y + 2),
        Vertex2f(position.x + 98 * value / max_value, position.y + 18),
        Vertex3f(0, 255, 0),
    )
    if show_value:
        renderer.draw_text(
            position.translated(Vertex2f(30, -15)),
            f"{int(value)}/{int(max_value)}",
            Vertex3f(255, 255, 255),
        )
