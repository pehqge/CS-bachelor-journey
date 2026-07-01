from model.clipping_algorithms import ClippingAlgorithms
from model.world_objects.world_object import WorldObject
from view.graphical_objects.graphical_wireframe import GraphicalWireframe


class WorldPolygon(WorldObject):
    """Classe pertinente a Wireframes no mundo."""

    def __init__(
        self, points: list, name: str, color: tuple, viewport_bounds, is_filled: bool
    ):
        super().__init__(points, name, color, viewport_bounds)
        self.is_filled = is_filled

        if is_filled:
            self.obj_type = "f"
        else:
            self.obj_type = "y"

    def get_clipped_representation(self) -> list:
        clipped_points = ClippingAlgorithms.sutherland_hodgman_clipping(
            self.projection_points
        )
        if clipped_points is None:
            return []

        viewport_points = self.transform_projection_points_to_viewport(clipped_points)
        graphical_representation = GraphicalWireframe(
            viewport_points, self.color, self.is_filled
        )
        return [graphical_representation]
