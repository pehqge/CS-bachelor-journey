import numpy as np

from utils.bounds import Bounds
from view.graphical_objects.line import Line
from view.graphical_objects.point import Point
from view.graphical_objects.wireframe import Wireframe


class WorldObject:
    """Classe pertinente a objetos pertencentes ao modelo interno (mundo)."""

    def __init__(
        self,
        points: list,
        name: str,
        color: tuple[int, int, int],
        viewport_bounds: Bounds,
    ):

        self.world_points: list[np.array] = self.get_homogeneous_coordinates(points)
        self.normalized_points: list[tuple[float, float]] = []
        self.viewport_bounds: Bounds = viewport_bounds

        if len(points) == 1:
            self.graphical_representation = Point(color)
        elif len(points) == 2:
            self.graphical_representation = Line(color)
        else:
            self.graphical_representation = Wireframe(color)

        self.name = name

    def update_normalized_points(self, norm_points: list[tuple[float, float]]):
        """Atualiza as coordenadas normalizadas (SCN) e a representação gráfica."""

        self.normalized_points = norm_points
        self.viewport_points = self.transform_normalized_points_to_viewport()
        self.graphical_representation.update_points(self.viewport_points)

    def transform_normalized_points_to_viewport(self) -> list[tuple[float, float]]:
        """Retorna as coordenadas do objeto gráfico para o viewport."""

        transformed_points = []
        for point in self.normalized_points:
            nx, ny = point

            vp_width = self.viewport_bounds.x_max - self.viewport_bounds.x_min
            vp_height = self.viewport_bounds.y_max - self.viewport_bounds.y_min

            vx = (nx + 1) / 2 * vp_width
            vy = (1 - ny) / 2 * vp_height
            transformed_points.append((vx, vy))

        return transformed_points

    def get_homogeneous_coordinates(self, points: list[tuple]) -> list[np.array]:
        """Retorna as coordenadas homogêneas dos pontos do objeto."""

        homogenous_coordinates = []
        for point in points:
            x, y = point
            homogenous_coordinates.append(np.array([x, y, 1]))
        return homogenous_coordinates

    def update_coordinates(self, matrices: list[np.array]) -> None:
        """
        Atualiza as coordenadas do objeto no mundo. Atentar para a ordem das operações, visto
        que isso impactará no resultado final. As multiplicações são feitas na ordem em que as
        matrizes são passadas.
        Ex:
        Suponha que matrices == [T1, T2, T3] e points == [P]
        Então a nova lista de pontos P' será obtida por P' = [P @ T1 @ T2 @ T3]
        """

        for matrix in matrices:
            self.world_points = [point @ matrix for point in self.world_points]

    def get_center(self) -> tuple[float, float]:
        """Retorna o centro geométrico do objeto no mundo."""

        x_sum = sum(point[0] for point in self.world_points)
        y_sum = sum(point[1] for point in self.world_points)
        x_center = x_sum / len(self.world_points)
        y_center = y_sum / len(self.world_points)

        return x_center, y_center

    def get_obj_description(self) -> None:
        """Retorna a descrição do objeto em formato .obj"""

        obj_description = ""

        for point in self.world_points:
            obj_description += f"v {point[0]:.1f} {point[1]:.1f}\n"

        obj_description += f"o {self.name}\n"

        if len(self.world_points) == 1:
            obj_type = "p"
        elif len(self.world_points) == 2:
            obj_type = "l"
        else:
            obj_type = "f"

        obj_description += f"{obj_type} {" ".join(str(i) for i in range(-1, -len(self.world_points) - 1, -1))}\n\n"

        return obj_description

    def __str__(self):

        formatted_points = ", ".join(
            f"({x:.1f}, {y:.1f})" for x, y, _ in self.world_points
        )
        return f"{self.graphical_representation.__class__.__name__} {self.name}: {formatted_points}"
