from abc import ABC, abstractmethod

import numpy as np
from utils.bounds import Bounds
from view.graphical_objects.graphical_object import GraphicalObject


class WorldObject(ABC):
    """Classe pertinente a objetos pertencentes ao modelo interno (mundo)."""

    def __init__(
        self,
        points: list,
        name: str,
        color: tuple[int, int, int],
        viewport_bounds: Bounds,
    ):

        self.world_points: list[np.array] = []
        for point in points:  # Converte os pontos para coordenadas homogêneas
            x, y = point
            self.world_points.append(np.array([x, y, 1]))

        self.normalized_points: list[tuple[float, float]] = []
        self.viewport_points: list[tuple[float, float]] = []
        self.viewport_bounds: Bounds = viewport_bounds

        self.name = name
        self.color = color

    def update_normalized_points(self, norm_points: list[tuple[float, float]]):
        """
        Atualiza as coordenadas normalizadas (NCS) do objeto e converte para as coordenadas do viewport.
        @param norm_points: Lista de pontos normalizados.
        """

        self.normalized_points = norm_points
        self.viewport_points = self.transform_normalized_points_to_viewport(norm_points)

    def transform_normalized_points_to_viewport(
        self, points: tuple[float, float]
    ) -> list[tuple[float, float]]:
        """
        Converte as coordenadas normalizadas (NCS) para as coordenadas do viewport.
        @param points: Lista de pontos normalizados.
        @return: Lista de pontos transformados.
        """

        transformed_points = []
        for point in points:
            nx, ny = point

            vp_width = self.viewport_bounds.x_max - self.viewport_bounds.x_min
            vp_height = self.viewport_bounds.y_max - self.viewport_bounds.y_min

            vx = (nx + 1) / 2 * vp_width + self.viewport_bounds.x_min
            vy = (1 - ny) / 2 * vp_height + self.viewport_bounds.y_min
            transformed_points.append((vx, vy))

        return transformed_points

    def update_coordinates(self, composite_matrix: np.ndarray) -> None:
        """
        Atualiza as coordenadas do objeto no mundo aplicando uma matriz de transformação composta.
        @param composite_matrix: Matriz de transformação composta.
        """
        self.world_points = [point @ composite_matrix for point in self.world_points]

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

        x_sum = sum(point[0] for point in self.world_points)
        y_sum = sum(point[1] for point in self.world_points)
        x_center = x_sum / len(self.world_points)
        y_center = y_sum / len(self.world_points)

        return x_center, y_center

    def get_obj_description(self, last_index: int) -> tuple[str, int]:
        """
        Retorna a descrição do objeto em formato .obj
        @param last_index: Índice do último ponto adicionado ao arquivo .obj.
        @return: Tupla contendo a descrição do objeto e o índice do último ponto adicionado.
        """

        obj_description = ""

        obj_description += f"o {self.name}\n"

        for point in self.world_points:
            obj_description += (
                f"v {point[0]:.1f} {point[1]:.1f} 0.0\n"  # mudar quando implementar 3D
            )

        obj_points = " ".join(
            str(i) for i in range(last_index, last_index + len(self.world_points))
        )

        if len(self.world_points) == 1:  # Ponto
            obj_type = "p"

        elif len(self.world_points) == 2:  # Segmento de reta
            obj_type = "l"

        else:  # Polígono
            if hasattr(self, "is_filled") and self.is_filled:
                obj_type = "f"
            else:
                obj_type = "l"
                obj_points += " " + str(last_index)

        obj_description += f"{obj_type} {obj_points}\n\n"

        return obj_description, last_index + len(self.world_points)

    def __str__(self):
        """
        Retorna uma string no seguinte formato:
        <Tipo_do_objeto> <nome_do_objeto>: (x1, y1), (x2, y2), ...
        """
        formatted_points = ", ".join(
            f"({x:.1f}, {y:.1f})" for x, y, _ in self.world_points
        )
        return f"{self.__class__.__name__.replace("World", "")} {self.name}: {formatted_points}"
