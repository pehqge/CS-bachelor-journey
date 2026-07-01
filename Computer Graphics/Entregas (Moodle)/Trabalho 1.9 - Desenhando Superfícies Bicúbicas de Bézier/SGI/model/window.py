import numpy as np

from model.transformation_generator import TransformationGenerator
from view.viewport.viewport_bounds import ViewportBounds


class Window:
    """Classe que representa a janela de visualização."""

    def __init__(self, viewport_bounds: ViewportBounds):
        """
        Como o tamanho do viewport é determinado em tempo de execução,
        adequamos o tamanho da janela de visualização para manter a proporção. De
        outra forma, a imagem seria distorcida.
        """

        viewport_width = viewport_bounds.x_lower_right - viewport_bounds.x_upper_left
        viewport_height = viewport_bounds.y_lower_right - viewport_bounds.y_upper_left
        aspect_ratio = viewport_width / viewport_height

        # Pontos de referência da window
        # O centro da Window foi escolhido como o VRP (View Reference Point) por conveniência
        self.window_center = np.array([0.0, 0.0, 0.0, 1.0])
        self.focus_point = np.array([0.0, 0.0, 10.0, 1.0])
        self.center_of_projection = np.array([0.0, 0.0, -10.0, 1.0])

        # Vetores da window: um apontando pra cima, um apontando pra direita e um apontando pra frente
        # Window começa sobre o plano xy, olhando em direção a z positivo
        # O eixo y indica a direção "cima", e o eixo "x" aponta para a esquerda
        # O w foi zerado para não deslocar os vetores na multiplicação matricial
        self.vup = np.array([0.0, 1.0, 0.0, 0.0])
        self.vright = np.array([-1.0, 0.0, 0.0, 0.0])
        self.view_plane_normal = np.array([0.0, 0.0, 1.0, 0.0])

        self.height = 20  # Valor default
        self.width = self.height * aspect_ratio

        self.zoom_level = 1.0
        self.angle_horizontal = 0.0
        self.angle_vertical = 0.0
        self.angle_spin = 0.0

    def apply_zoom(self, zoom_level: float) -> None:
        """Aplica um zoom na janela de visualização com base no nível atual de zoom."""

        zoom_level /= 100

        relative_change = zoom_level / self.zoom_level
        self.zoom_level = zoom_level
        scaling_factor = 1 / relative_change

        self.width *= scaling_factor
        self.height *= scaling_factor

    def apply_pan(self, d_horizontal: float, d_vertical: float, d_depth: float) -> None:
        """
        Aplica um pan na janela de visualização.
        @param d_vertical: Deslocamento vertical
        @param d_horizontal: Deslocamento horizontal
        @param d_depth: Deslocamento em profundidade
        """

        pan_mtx = TransformationGenerator.get_pan_matrix(
            d_vertical,
            d_horizontal,
            d_depth,
            self.vup,
            self.vright,
            self.view_plane_normal,
        )

        self.focus_point = self.focus_point @ pan_mtx
        self.center_of_projection = self.center_of_projection @ pan_mtx
        self.window_center = self.window_center @ pan_mtx

    def apply_rotation(self, angle_degrees: float, rotation_type: str) -> None:
        """
        Aplica uma rotação na janela de visualização em torno do foco.
        @param angle_degrees: Ângulo final da rotação
        @param rotation_type: Tipo de rotação (horizontal, vertical ou em torno de si mesma)
        """

        axis_vector = {
            "horizontal": self.vup,
            "vertical": self.vright,
            "spin": self.view_plane_normal,
        }.get(rotation_type)

        if axis_vector is None:
            return

        angle_attr = f"angle_{rotation_type}"
        angle_delta = angle_degrees - getattr(self, angle_attr)
        setattr(self, angle_attr, angle_degrees)

        # Gera um eixo que passa pelo foco e é paralelo ao vetor de rotação
        p1 = self.focus_point[::]
        p2 = [
            self.focus_point[0] + axis_vector[0],
            self.focus_point[1] + axis_vector[1],
            self.focus_point[2] + axis_vector[2],
            1.0,
        ]

        rotation_matrix = TransformationGenerator.get_arbitrary_rotation_matrix(
            angle_degrees=angle_delta,
            p1=p1,
            p2=p2,
        )

        self.vup = self.vup @ rotation_matrix
        self.vright = self.vright @ rotation_matrix
        self.view_plane_normal = self.view_plane_normal @ rotation_matrix
        self.window_center = self.window_center @ rotation_matrix
        self.center_of_projection = self.center_of_projection @ rotation_matrix

    def get_width(self) -> float:
        """Retorna a largura da janela de visualização."""
        return self.width

    def get_height(self) -> float:
        """Retorna a altura da janela de visualização."""
        return self.height
