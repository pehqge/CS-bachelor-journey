import numpy as np
from model.world_objects.world_curve import WorldCurve


class WorldBSplineCurve(WorldCurve):
    """
    Classe pertinente a curvas B-spline no mundo.
    """

    def __init__(self, points, name, color, viewport_bounds):
        super().__init__(points, name, color, viewport_bounds)
        self.obj_type = "bspline"

    def _generate_normalized_curve_points(self) -> list[tuple[float, float]]:
        """
        Gera pontos ao longo da curva B-spline usando a forma matricial em coordenadas normalizadas.
        @return: Lista de pontos (x, y) normalizados ao longo da curva.
        """

        b_spline_matrix = (
            np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]]) / 6
        )

        num_steps = 100
        delta = 1.0 / num_steps
        normalized_points = []

        for i in range(len(self.normalized_points) - 3):
            x0, y0 = self.normalized_points[i]
            x1, y1 = self.normalized_points[i + 1]
            x2, y2 = self.normalized_points[i + 2]
            x3, y3 = self.normalized_points[i + 3]

            coefficients_x = b_spline_matrix @ np.array([x0, x1, x2, x3])
            coefficients_y = b_spline_matrix @ np.array([y0, y1, y2, y3])

            delta_matrix_x = self._find_first_iteration_deltas(delta, coefficients_x)
            x = delta_matrix_x[0]
            delta_x = delta_matrix_x[1]
            delta_x_2 = delta_matrix_x[2]
            delta_x_3 = delta_matrix_x[3]

            delta_matrix_y = self._find_first_iteration_deltas(delta, coefficients_y)
            y = delta_matrix_y[0]
            delta_y = delta_matrix_y[1]
            delta_y_2 = delta_matrix_y[2]
            delta_y_3 = delta_matrix_y[3]

            current_segment = []
            current_segment.append((x, y))

            for _ in range(num_steps - 1):
                x += delta_x
                delta_x += delta_x_2
                delta_x_2 += delta_x_3

                y += delta_y
                delta_y += delta_y_2
                delta_y_2 += delta_y_3

                current_segment.append((x, y))

            normalized_points.extend(current_segment)
            current_segment = []

        return normalized_points

    def _find_first_iteration_deltas(
        self, delta: float, coefficients_mtx: np.array
    ) -> np.array:
        """
        Obtém os valores da primeira iteração no algoritmo de forward differences
        @param delta: o valor do delta no algoritmo
        @param coefficients_mtx: matriz de coeficientes com os coeficientes a, b, c e d
        @return: matriz contendo [f(0), Δf(0), Δ²f(0), Δ³f(0)]
        """

        a, b, c, d = coefficients_mtx
        f0 = d
        delta_f0 = a * delta**3 + b * delta**2 + c * delta
        delta_f0_2 = 6 * a * delta**3 + 2 * b * delta**2
        delta_f0_3 = 6 * a * delta**3

        return np.array([f0, delta_f0, delta_f0_2, delta_f0_3])
