from utils.bounds import Bounds


class Window:
    """Classe que representa a janela de visualização."""

    def __init__(self, viewport_bounds: Bounds):
        """
        Como o tamanho do viewport é determinado em tempo de execução,
        adequamos o tamanho da janela de visualização para manter a proporção. De
        outra forma, a imagem seria distorcida.
        """

        viewport_width = viewport_bounds.x_max - viewport_bounds.x_min
        viewport_height = viewport_bounds.y_max - viewport_bounds.y_min
        aspect_ratio = viewport_width / viewport_height

        default_height = 200
        default_width = default_height * aspect_ratio

        self.window_bounds = Bounds(
            x_min=-default_width / 2,
            x_max=default_width / 2,
            y_min=-default_height / 2,
            y_max=default_height / 2
        )

    def apply_zoom(self, factor: float) -> None:
        """Aplica um zoom na janela de visualização."""
        self.window_bounds.x_min *= factor
        self.window_bounds.x_max *= factor
        self.window_bounds.y_min *= factor
        self.window_bounds.y_max *= factor

    def apply_pan(self, dx: float, dy: float) -> None:
        """Aplica um pan na janela de visualização."""
        self.window_bounds.x_min += dx
        self.window_bounds.x_max += dx
        self.window_bounds.y_min += dy
        self.window_bounds.y_max += dy
