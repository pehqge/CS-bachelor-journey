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
        window_bounds: Bounds,
        viewport_bounds: Bounds,
    ):
        self.world_points = points
        viewport_points = self.transform_points_to_viewport(
            viewport_bounds, window_bounds
        )

        if len(points) == 1:
            self.graphical_representation = Point(viewport_points)
        elif len(points) == 2:
            self.graphical_representation = Line(viewport_points)
        else:
            self.graphical_representation = Wireframe(viewport_points)

        self.name = name

    def transform_points_to_viewport(
        self, viewport_bounds: Bounds, window_bounds: Bounds
    ) -> list[tuple[float, float]]:
        """Retorna as coordenadas do objeto gráfico para o viewport."""

        transformed_points = []

        for point in self.world_points:
            x, y = point

            x_viewport = (
                (x - window_bounds.x_min)
                / (window_bounds.x_max - window_bounds.x_min)
                * (viewport_bounds.x_max - viewport_bounds.x_min)
            )

            y_viewport = (
                1 - (y - window_bounds.y_min)
                / (window_bounds.y_max - window_bounds.y_min)
            ) * (viewport_bounds.y_max - viewport_bounds.y_min)

            transformed_points.append((x_viewport, y_viewport))

        return transformed_points

    def update_representation(self, window_bounds: Bounds, viewport_bounds: Bounds) -> None:
        """Atualiza as coordenadas do objeto gráfico para o viewport."""

        self.graphical_representation.viewport_points = self.transform_points_to_viewport(
            viewport_bounds, window_bounds
        )

    def __str__(self):
        formatted_points = ", ".join(f"({x:.1f}, {y:.1f})" for x, y in self.world_points)
        return f"{self.graphical_representation.__class__.__name__} {self.name}: {formatted_points}"
