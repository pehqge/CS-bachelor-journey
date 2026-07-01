import numpy as np

from model.transformation_generator import TransformationGenerator
from model.world_objects.world_point import WorldObject
from view.viewport.viewport_bounds import ViewportBounds


class Window:
    """
    Classe que representa a janela de visualização no mundo. O sistema gráfico funciona com a
    câmera estática; sendo assim, movimentá-la é equivalente a movimentar os objetos do mundo. Cada
    movimento da janela de visualização altera a matriz de conversão, que é usada para
    converter as coordenadas percebidas pelo usuário em coordenadas reais do mundo.

    No sistema real:
    1 - A janela está centrada na origem do mundo.
    2 - O foco da janela se desloca sobre a parte negativa do eixo Z
    3 - O foco permanece fixo em (0, 0, 10)
    4 - y é positivo para cima, x é positivo para a esquerda e z é positivo para frente
    """

    def __init__(self, viewport_bounds: ViewportBounds):
        # Como o tamanho do viewport é determinado em tempo de execução,
        # adequamos o tamanho da janela de visualização para manter a proporção. De
        # outra forma, a imagem seria distorcida.
        viewport_width = viewport_bounds.x_lower_right - viewport_bounds.x_upper_left
        viewport_height = viewport_bounds.y_lower_right - viewport_bounds.y_upper_left
        aspect_ratio = viewport_width / viewport_height

        # Pontos de referência da window
        # O foco é um ponto em torno do qual a window gira
        # O centro de projeção é o ponto onde todos os raios de projeção convergem
        self.focus_point = np.array([0.0, 0.0, 10.0, 1.0])
        self.center_of_projection = np.array([0.0, 0.0, -10.0, 1.0])

        # Matriz que converte as coordenadas percebidas pelo usuário pelas coordenadas
        # reais do mundo
        self.conversion_mtx: np.array = np.eye(4)

        # Observadores que assinam a janela de visualização para receber atualizações
        # quando a percepção do usuário muda (janela de visualização é movida)
        self.subscribers = []

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

        translation_mtx = TransformationGenerator.get_translation_matrix(
            dx=d_horizontal,  # Positivo é para a esquerda
            dy=-d_vertical,
            dz=-d_depth,
        )
        self.conversion_mtx = self.conversion_mtx @ translation_mtx
        self.notify_perception_change()

    def apply_rotation(self, angle_degrees: float, rotation_type: str) -> None:
        """
        Aplica uma rotação na janela de visualização em torno do foco.
        @param angle_degrees: Ângulo final da rotação
        @param rotation_type: Tipo de rotação (horizontal, vertical ou em torno de si mesma)
        """

        axis_vector = {
            "horizontal": np.array([0.0, 1.0, 0.0, 1.0]),
            "vertical": np.array([1.0, 0.0, 0.0, 1.0]),
            "spin": np.array([0.0, 0.0, 1.0, 1.0]),
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

        self.conversion_mtx = self.conversion_mtx @ rotation_matrix
        self.notify_perception_change()

    def change_cop_distance(self, distance: float) -> None:
        """
        Altera a distância do centro de projeção (COP) em relação ao plano de projeção.
        @param distance: Valor da nova distância do COP
        """

        self.center_of_projection = np.array(
            [
                0.0,
                0.0,
                -distance,
                1.0,
            ]
        )

    def get_width(self) -> float:
        """Retorna a largura da janela de visualização."""
        return self.width

    def get_height(self) -> float:
        """Retorna a altura da janela de visualização."""
        return self.height

    def add_subscriber(self, subscriber: WorldObject) -> None:
        """
        Adiciona um assinante à janela de visualização.
        @param subscriber: O objeto que deseja se inscrever para receber atualizações de
        mudanças na percepção do usuário.
        """
        self.subscribers.append(subscriber)
        subscriber.update_world_coordinates(self.conversion_mtx)

    def remove_subscriber(self, index: int) -> None:
        """
        Remove um assinante da janela de visualização.
        @param index: Índice do assinante a ser removido.
        """
        self.subscribers.pop(index)

    def notify_perception_change(self) -> None:
        """
        Notifica todos os assinantes sobre uma mudança na percepção do usuário (pan ou rotação)
        """
        for subscriber in self.subscribers:
            subscriber.update_world_coordinates(self.conversion_mtx)
