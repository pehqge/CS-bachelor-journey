from model.world_objects.world_object import WorldObject
from utils.bounds import Bounds
from view.graphical_objects.graphical_line import GraphicalLine


class WorldLine(WorldObject):
    """Classe pertinente a linhas no mundo."""

    def __init__(
        self,
        points: list,
        name: str,
        color: tuple[int, int, int],
        viewport_bounds: Bounds,
    ):
        super().__init__(points, name, color, viewport_bounds)
        self.inside = 0b0000
        self.left = 0b0001
        self.right = 0b0010
        self.bottom = 0b0100
        self.top = 0b1000
        self.clipping_mode = self.cohen_sutherland_clipping

    def get_clipped_representation(self) -> GraphicalLine | None:
        clipped_points = self.clipping_mode()

        if clipped_points is None:
            return None

        viewport_points = self.transform_normalized_points_to_viewport(clipped_points)
        graphical_representation = GraphicalLine(viewport_points, self.color)
        return graphical_representation

    def _get_region_code(
        self, x: float, y: float, x_min: float, y_min: float, x_max: float, y_max: float
    ) -> int:
        """
        Retorna o código da região para o ponto (x, y).
        @param x: Coordenada x do ponto.
        @param y: Coordenada y do ponto.
        @return: Código da região.
        """

        code = self.inside

        if x < x_min:
            code |= self.left
        elif x > x_max:
            code |= self.right
        if y < y_min:
            code |= self.bottom
        elif y > y_max:
            code |= self.top

        return code

    def cohen_sutherland_clipping(self) -> tuple | None:
        """
        Algoritmo de Cohen-Sutherland para recorte de linhas.
        @return: Tupla com os pontos recortados da linha em coordenadas normalizadas ou NONE se a linha
        estiver fora do Viewport.
        """

        y_min, y_max = -1, 1
        x_min, x_max = -1, 1
        x1, y1 = self.normalized_points[0]
        x2, y2 = self.normalized_points[1]

        code1 = self._get_region_code(x1, y1, x_min, y_min, x_max, y_max)
        code2 = self._get_region_code(x2, y2, x_min, y_min, x_max, y_max)

        accepted = False  # Inicialmente, a linha é considerada fora do viewport

        while True:
            if code1 == 0 and code2 == 0:  # Ambos os pontos estão dentro do viewport
                accepted = True
                break

            if code1 & code2 != 0:  # Ambos os pontos estão fora do viewport
                break

            # Se chegou aqui, então é possível que a linha intercepte a borda do viewport
            code_outside = code1 if code1 != 0 else code2
            intersection_x = 0.0
            intersection_y = 0.0

            if code_outside & self.top:
                intersection_x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                intersection_y = y_max

            elif code_outside & self.bottom:
                intersection_x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                intersection_y = y_min

            elif code_outside & self.right:
                intersection_y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                intersection_x = x_max

            elif code_outside & self.left:
                intersection_y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                intersection_x = x_min

            if code_outside == code1:
                x1, y1 = intersection_x, intersection_y
                code1 = self._get_region_code(x1, y1, x_min, y_min, x_max, y_max)
            else:
                x2, y2 = intersection_x, intersection_y
                code2 = self._get_region_code(x2, y2, x_min, y_min, x_max, y_max)

        if accepted:
            return [(x1, y1), (x2, y2)]
        return None

    def liang_barsky_clipping(self) -> tuple | None:
        """
        Algoritmo de Liang-Barsky para recorte de linhas.
        @return: Tupla com os pontos recortados da linha em coordenadas normalizadas ou None se a linha
        estiver fora do Viewport.
        """

        x_min, x_max = -1, 1
        y_min, y_max = -1, 1

        start_x, start_y = self.normalized_points[0]
        end_x, end_y = self.normalized_points[1]

        delta_x = end_x - start_x
        delta_y = end_y - start_y

        # Componentes de direção e distâncias até as bordas
        directions = [-delta_x, delta_x, -delta_y, delta_y]
        distances = [start_x - x_min, x_max - start_x, start_y - y_min, y_max - start_y]

        t_enter = 0.0  # Limite inferior máximo para t
        t_exit = 1.0  # Limite superior mínimo para t

        for direction_component, distance_to_edge in zip(directions, distances):
            if direction_component == 0:
                if distance_to_edge < 0:
                    return None  # Linha paralela e fora do limite, deve ser descartada
            else:
                t = distance_to_edge / direction_component
                if direction_component < 0:
                    t_enter = max(t_enter, t)  # Atualiza limite inferior
                else:
                    t_exit = min(t_exit, t)  # Atualiza limite superior

        if t_enter > t_exit:
            return None

        clipped_start_x = start_x + t_enter * delta_x
        clipped_start_y = start_y + t_enter * delta_y
        clipped_end_x = start_x + t_exit * delta_x
        clipped_end_y = start_y + t_exit * delta_y

        return [(clipped_start_x, clipped_start_y), (clipped_end_x, clipped_end_y)]

    def change_clipping_mode(self, mode: str) -> None:
        """
        Muda o modo de clipping.
        @param mode: Modo de clipping.
        """

        if mode == "cohen_sutherland":
            self.clipping_mode = self.cohen_sutherland_clipping
        elif mode == "liang_barsky":
            self.clipping_mode = self.liang_barsky_clipping
        else:
            raise ValueError(f"Modo de clipping inválido: {mode}")
