from model.world_objects.world_object import WorldObject
from view.graphical_objects.graphical_point import GraphicalPoint


class WorldPoint(WorldObject):
    """Classe pertinente a pontos no mundo."""

    def __init__(self, points, name, color, viewport_bounds):
        super().__init__(points, name, color, viewport_bounds)
        self.obj_type = "p"

    def get_clipped_representation(self) -> list:
        """
        Apenda o ponto apenas se estiver dentro dos limites do Viewport
        """

        x, y = self.normalized_points[0]
        if x < -1 or x > 1 or y < -1 or y > 1:
            return []

        graphical_representation = GraphicalPoint(self.viewport_points, self.color)
        return [graphical_representation]
