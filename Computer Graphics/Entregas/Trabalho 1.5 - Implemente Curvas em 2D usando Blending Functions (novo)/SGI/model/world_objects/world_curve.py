import numpy as np
from model.clipping_algorithms import ClippingAlgorithms
from model.world_objects.sc_world_object import SCWorldObject
from view.graphical_objects.graphical_curve import GraphicalCurve


class WorldCurve(SCWorldObject):
    """Classe pertinente a curvas de Bézier cúbicas no mundo."""

    def __init__(self, points, name, color, viewport_bounds):
        super().__init__(points, name, color, viewport_bounds)

        self.clipping_mode = ClippingAlgorithms.cohen_sutherland_clipping
        self.clipping_modes = {
            "cohen_sutherland": ClippingAlgorithms.cohen_sutherland_clipping,
            "liang_barsky": ClippingAlgorithms.liang_barsky_clipping,
        }

    def update_normalized_points(self, norm_points: list[tuple[float, float]]):
        """
        Atualiza as coordenadas normalizadas (NCS) dos PONTOS DE CONTROLE do objeto
        e recalcula os pontos da curva para o viewport.
        @param norm_points: Lista de pontos de controle normalizados.
        """

        self.normalized_points = norm_points
        self.curve_points = self._generate_curve_points_normalized()
        self.viewport_points = self.transform_normalized_points_to_viewport(
            self.curve_points
        )

    def _generate_curve_points_normalized(self) -> list[tuple[float, float]]:
        """
        Gera pontos ao longo da curva de Bézier usando a forma matricial em coordenadas normalizadas.
        @return: Lista de pontos (x, y) normalizados ao longo da curva.
        """

        num_steps = 100

        # Faz o tratamento de pontos de controle para C(1)
        pts = list(self.normalized_points)
        for j in range(3, len(pts) - 3, 3):
            P2 = np.array(pts[j - 1])
            P3 = np.array(pts[j])
            pts[j + 1] = (P3 + (P3 - P2)).tolist()

        # Matriz de Bezier
        M = np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]])

        # Gera T e TM
        ts = np.linspace(
            0, 1, num_steps + 1
        )  # vetor com todos os valores de t (de 0 a 1 com num_steps+1 pontos)
        T = np.vstack(
            [ts**3, ts**2, ts, np.ones_like(ts)]
        ).T  # matriz de tamanho num_steps+1 por 4, onde cada linha é um vetor [t^3, t^2, t, 1]
        TM = T @ M

        # Gera os pontos da curva
        curve_points = []
        for i in range(0, len(pts) - 3, 3):
            P = np.array([[pts[x][0], pts[x][1]] for x in range(i, 4 + i)])

            point_coords = TM @ P
            curve_points.extend(tuple(point_coords))

        return curve_points

    def get_clipped_representation(self) -> list:
        """
        Retorna a representação gráfica da curva após dividir em retas e aplicar clipping.
        """

        clipped_parts = ClippingAlgorithms.curve_clipping(
            self.curve_points, self.clipping_mode
        )
        if not clipped_parts:
            return []

        representations = []

        for part in clipped_parts:
            viewport_points = self.transform_normalized_points_to_viewport(part)

            representations.append(
                GraphicalCurve(
                    viewport_points,
                    self.color,
                )
            )

        return representations
