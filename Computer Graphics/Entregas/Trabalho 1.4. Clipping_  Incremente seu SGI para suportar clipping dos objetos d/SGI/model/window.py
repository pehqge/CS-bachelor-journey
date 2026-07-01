import numpy as np

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
            y_max=default_height / 2,
        )

        self.angle = 0.0
        self.vup = np.array([0.0, 1.0])

    def get_center(self) -> tuple[float, float]:
        """Retorna o centro da janela de visualização. (WCx, WCy)"""

        return (self.window_bounds.x_min + self.window_bounds.x_max) / 2, (
            self.window_bounds.y_min + self.window_bounds.y_max
        ) / 2

    def get_width_height(self) -> tuple[float, float]:
        """Retorna a largura e a altura da janela de visualização. (Wx, Wy)"""

        return (
            self.window_bounds.x_max - self.window_bounds.x_min,
            self.window_bounds.y_max - self.window_bounds.y_min,
        )

    def apply_zoom(self, factor: float) -> None:
        """Aplica um zoom na janela de visualização"""

        self.window_bounds.x_min *= factor
        self.window_bounds.x_max *= factor
        self.window_bounds.y_min *= factor
        self.window_bounds.y_max *= factor

    def apply_pan(self, dx: float, dy: float) -> None:
        """Aplica um pan na janela de visualização."""

        # Rotaciona dx e dy pelo ângulo atual da window
        dx_world = dx * np.cos(self.angle) - dy * np.sin(self.angle)
        dy_world = dx * np.sin(self.angle) + dy * np.cos(self.angle)

        self.window_bounds.x_min += dx_world
        self.window_bounds.x_max += dx_world
        self.window_bounds.y_min += dy_world
        self.window_bounds.y_max += dy_world

    def apply_rotation(self, angle_degrees: float) -> None:
        """Aplica uma rotação na janela de visualização."""

        self.angle = np.radians(angle_degrees)

        # Rotaciona o vup para o novo ângulo
        rotation_matrix = np.array(
            [
                [np.cos(self.angle), -np.sin(self.angle)],
                [np.sin(self.angle), np.cos(self.angle)],
            ]
        )

        self.vup = rotation_matrix @ np.array([0.0, 1.0])
