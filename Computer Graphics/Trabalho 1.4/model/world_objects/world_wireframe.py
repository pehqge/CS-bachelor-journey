from model.world_objects.world_object import WorldObject
from view.graphical_objects.graphical_wireframe import GraphicalWireframe


class WorldWireframe(WorldObject):
    """Classe pertinente a Wireframes no mundo."""

    def __init__(
        self, points: list, name: str, color: tuple, viewport_bounds, is_filled: bool
    ):
        super().__init__(points, name, color, viewport_bounds)
        self.is_filled = is_filled

    def get_clipped_representation(self) -> GraphicalWireframe | None:
        clipped_points = self.sutherland_hodgman_clipping()
        if clipped_points is None:
            return None

        viewport_points = self.transform_normalized_points_to_viewport(clipped_points)
        graphical_representation = GraphicalWireframe(
            viewport_points, self.color, self.is_filled
        )
        return graphical_representation

    def sutherland_hodgman_clipping(self) -> list[tuple[float, float]] | None:
        """
        Algoritmo de Sutherland-Hodgman para recorte de polígonos.
        @return: Lista de listas de pontos, cada uma representando uma parte que foi recortada OU
        None se o polígono estiver fora do Viewport.
        """

        all_inside = True
        for point in self.normalized_points:
            x, y = point
            if not (-1 <= x <= 1 and -1 <= y <= 1):
                all_inside = False
                break

        # Polígono totalmente dentro, dispensa o recorte
        if all_inside:
            return self.normalized_points

        # Define o polígono de recorte (borda do viewport em coordenadas normalizadas)
        clip_window = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        clip_edges = list(zip(clip_window, clip_window[1:] + [clip_window[0]]))

        clipped_polygon = self.normalized_points[:]

        for clip_start, clip_end in clip_edges:
            input_polygon = clipped_polygon
            clipped_polygon = []

            if not input_polygon:
                break

            previous_point = input_polygon[-1]

            for current_point in input_polygon:
                clip_x0, clip_y0 = clip_start
                clip_x1, clip_y1 = clip_end

                # Verifica se o ponto está dentro do semiplano definido pela aresta de recorte
                px, py = current_point
                current_inside = (clip_x1 - clip_x0) * (py - clip_y0) > (
                    clip_y1 - clip_y0
                ) * (px - clip_x0)

                # Verifica se o ponto anterior está dentro do semiplano
                px, py = previous_point
                previous_inside = (clip_x1 - clip_x0) * (py - clip_y0) > (
                    clip_y1 - clip_y0
                ) * (px - clip_x0)

                # Calcula interseção se necessário
                if current_inside != previous_inside:
                    x1, y1 = previous_point
                    x2, y2 = current_point
                    x3, y3 = clip_start
                    x4, y4 = clip_end

                    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

                    if denom != 0:  # Evita divisão por zero (linhas paralelas)
                        px = (
                            (x1 * y2 - y1 * x2) * (x3 - x4)
                            - (x1 - x2) * (x3 * y4 - y3 * x4)
                        ) / denom
                        py = (
                            (x1 * y2 - y1 * x2) * (y3 - y4)
                            - (y1 - y2) * (x3 * y4 - y3 * x4)
                        ) / denom
                        intersection = (px, py)
                        clipped_polygon.append(intersection)

                # Adiciona o ponto atual se estiver dentro
                if current_inside:
                    clipped_polygon.append(current_point)

                previous_point = current_point

        if clipped_polygon:
            return clipped_polygon
        return None
