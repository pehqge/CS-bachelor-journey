from abc import ABC, abstractmethod

import numpy as np

from view.graphical_objects.graphical_object import GraphicalObject
from view.viewport.viewport_bounds import ViewportBounds


class WorldObject(ABC):
    """Classe pertinente a objetos pertencentes ao modelo interno (mundo)."""

    def __init__(
        self,
        points: list,
        name: str,
        color: tuple[int, int, int],
        viewport_bounds: ViewportBounds,
    ):

        self.perceived_points: list[np.array] = []  # Lista de pontos percebidos
        self.world_points: list[np.array] = []  # Lista de pontos reais

        if points and isinstance(points[0], list) and isinstance(points[0][0], list):
            pass
        else:
            for point in points:  # Converte os pontos para coordenadas homogêneas
                x, y, z = point
                self.perceived_points.append(np.array([x, y, z, 1]))

        self.projection_points: list[tuple[float, float]] = (
            []
        )  # Lista de pontos projetados no plano da window em coordenadas normalizadas
        self.viewport_bounds: ViewportBounds = viewport_bounds

        self.name = name
        self.color = color
        self.dirty = True  # Booleano para indicar se o objeto precisa ser atualizado

    def update_projection_points(
        self, projection_points: list[tuple[float, float]]
    ) -> None:
        """
        Atualiza as coordenadas projetadas do objeto.
        @param projection_points: Lista de pontos projetados em coordenadas normalizadas.
        """

        self.projection_points = projection_points

    def transform_projection_points_to_viewport(
        self, points: tuple[float, float]
    ) -> list[tuple[float, float]]:
        """
        Converte as coordenadas da projeção para as coordenadas do viewport.
        @param points: Lista de pontos projetados.
        @return: Lista de pontos transformados para o viewport.
        """

        transformed_points = []
        for point in points:
            normalized_x, normalized_y = point

            vp_width = (
                self.viewport_bounds.x_lower_right - self.viewport_bounds.x_upper_left
            )
            vp_height = (
                self.viewport_bounds.y_lower_right - self.viewport_bounds.y_upper_left
            )

            vx = (normalized_x + 1) / 2 * vp_width + self.viewport_bounds.x_upper_left
            vy = (1 - normalized_y) / 2 * vp_height + self.viewport_bounds.y_upper_left
            transformed_points.append((vx, vy))

        return transformed_points

    def update_perceived_coordinates(self, composite_matrix: np.ndarray) -> None:
        """
        Atualiza as coordenadas percebidas do objeto aplicando uma matriz de transformação composta.
        @param composite_matrix: Matriz de transformação composta.
        """
        self.perceived_points = [
            point @ composite_matrix for point in self.perceived_points
        ]

    def update_world_coordinates(self, conversion_mtx: np.ndarray) -> None:
        """
        Atualiza as coordenadas do mundo aplicando a matriz de conversão.
        @param conversion_mtx: Matriz de conversão para coordenadas do mundo.
        """
        self.world_points = [point @ conversion_mtx for point in self.perceived_points]

    @abstractmethod
    def get_clipped_representation(self) -> list[GraphicalObject]:
        """
        Executa o clipping do objeto e retorna a representação gráfica.
        @return: lista de objetos gráficos representando o objeto no Viewport. Pode ser vazia, se o
        objeto estiver fora, ou conter um ou mais objetos gráficos (dependendo da clipagem)
        """

    def get_center(self) -> tuple[float, float]:
        """
        Retorna o centro geométrico do objeto no mundo.
        @return: Coordenadas (x, y) do centro geométrico.
        """

        x_sum = sum(point[0] for point in self.perceived_points)
        y_sum = sum(point[1] for point in self.perceived_points)
        z_sum = sum(point[2] for point in self.perceived_points)
        x_center = x_sum / len(self.perceived_points)
        y_center = y_sum / len(self.perceived_points)
        z_center = z_sum / len(self.perceived_points)

        return x_center, y_center, z_center

    def get_obj_description(self, last_index: int) -> tuple[str, int]:
        """
        Retorna a descrição do objeto em formato .obj
        @param last_index: Índice do último ponto adicionado ao arquivo .obj.
        @return: Tupla contendo a descrição do objeto e o índice do último ponto adicionado.
        """

        obj_description = f"o {self.name}\n"

        for point in self.perceived_points:
            obj_description += f"v {point[0]:.1f} {point[1]:.1f} {point[2]:.1f}\n"

        obj_points = " ".join(
            str(i) for i in range(last_index, last_index + len(self.perceived_points))
        )

        if self.__class__.__name__ == "WorldWireframe":
            for edge in self.get_edges_obj_file(last_index):
                obj_description += edge + "\n"
            obj_description += "\n"
        else:
            obj_description += f"{self.obj_type} {obj_points}\n\n"

        return obj_description, last_index + len(self.perceived_points)

    def __str__(self):
        """
        Retorna uma string no seguinte formato:
        <Tipo_do_objeto> <nome_do_objeto>: (x1, y1, z1), (x2, y2, z2), ...
        """
        formatted_points = ", ".join(
            f"({x:.1f}, {y:.1f}, {z:.1f})" for x, y, z, _ in self.perceived_points
        )
        return f"{self.__class__.__name__.replace("World", "")} {self.name}: {formatted_points}"
