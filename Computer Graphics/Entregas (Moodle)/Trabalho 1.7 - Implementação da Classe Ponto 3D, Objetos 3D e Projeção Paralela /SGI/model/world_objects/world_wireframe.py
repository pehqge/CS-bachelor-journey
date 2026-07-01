from model.world_objects.sc_world_object import SCWorldObject
from view.graphical_objects.graphical_line import GraphicalLine


class WorldWireframe(SCWorldObject):
    """Classe pertinente a Wireframes no mundo."""

    def __init__(
        self,
        points: list,
        name: str,
        color: tuple,
        viewport_bounds,
        is_filled: bool,
        edges: list,
    ):
        super().__init__(points, name, color, viewport_bounds)
        self.is_filled = is_filled

        self.obj_type = "l"

        self.edges = edges

    def get_clipped_representation(self) -> list:
        clipped_representations = []

        for index_1, index_2 in self.edges:
            p1 = self.projection_points[index_1]
            p2 = self.projection_points[index_2]
            clipped_points = self.clipping_mode(p1, p2)

            if clipped_points is not None:
                viewport_points = self.transform_projection_points_to_viewport(
                    clipped_points
                )
                graphical_representation = GraphicalLine(viewport_points, self.color)
                clipped_representations.append(graphical_representation)

        return clipped_representations
    
    def get_edges_obj_file(self, last_index) -> list:
        edges_obj_file = []
        for index_1, index_2 in self.edges:
            edges_obj_file.append(f"l {index_1+last_index} {index_2+last_index}")
        return edges_obj_file
