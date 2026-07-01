import numpy as np
from model.world_objects.world_curve import WorldCurve


class WorldBezierCurve(WorldCurve):
    """Classe pertinente a curvas de Bézier cúbicas no mundo."""

    def __init__(self, points, name, color, viewport_bounds):
        super().__init__(points, name, color, viewport_bounds)
        self.obj_type = "bezier"

    def _generate_normalized_curve_points(self) -> list[tuple[float, float]]:
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
