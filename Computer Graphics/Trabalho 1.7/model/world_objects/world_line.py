from model.clipping_algorithms import ClippingAlgorithms
from model.world_objects.sc_world_object import SCWorldObject
from view.graphical_objects.graphical_line import GraphicalLine
from view.viewport.viewport_bounds import ViewportBounds


class WorldLine(SCWorldObject):
    """Classe pertinente a linhas no mundo."""

    def __init__(
        self,
        points: list,
        name: str,
        color: tuple[int, int, int],
        viewport_bounds: ViewportBounds,
    ):
        super().__init__(points, name, color, viewport_bounds)
        self.obj_type = "l"

    def get_clipped_representation(self) -> list:
        p1 = self.projection_points[0]
        p2 = self.projection_points[1]
        clipped_points = self.clipping_mode(p1, p2)

        if clipped_points is None:
            return []

        viewport_points = self.transform_projection_points_to_viewport(clipped_points)
        graphical_representation = GraphicalLine(viewport_points, self.color)
        return [graphical_representation]
