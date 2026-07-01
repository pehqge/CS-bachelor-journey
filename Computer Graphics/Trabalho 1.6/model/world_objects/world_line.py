from model.clipping_algorithms import ClippingAlgorithms
from model.world_objects.sc_world_object import SCWorldObject
from utils.bounds import Bounds
from view.graphical_objects.graphical_line import GraphicalLine


class WorldLine(SCWorldObject):
    """Classe pertinente a linhas no mundo."""

    def __init__(
        self,
        points: list,
        name: str,
        color: tuple[int, int, int],
        viewport_bounds: Bounds,
    ):
        super().__init__(points, name, color, viewport_bounds)
        self.clipping_modes = {
            "cohen_sutherland": ClippingAlgorithms.cohen_sutherland_clipping,
            "liang_barsky": ClippingAlgorithms.liang_barsky_clipping,
        }
        self.clipping_mode = ClippingAlgorithms.cohen_sutherland_clipping
        self.obj_type = "l"

    def get_clipped_representation(self) -> list:
        p1 = self.normalized_points[0]
        p2 = self.normalized_points[1]
        clipped_points = self.clipping_mode(p1, p2)

        if clipped_points is None:
            return []

        viewport_points = self.transform_normalized_points_to_viewport(clipped_points)
        graphical_representation = GraphicalLine(viewport_points, self.color)
        return [graphical_representation]
