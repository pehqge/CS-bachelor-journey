import numpy as np


class ClippingAlgorithms:
    """Classe utilitária para algoritmos de recorte."""

    INSIDE = 0b0000
    LEFT = 0b0001
    RIGHT = 0b0010
    BOTTOM = 0b0100
    TOP = 0b1000

    @classmethod
    def _get_region_code(
        cls, x: float, y: float, x_min: float, y_min: float, x_max: float, y_max: float
    ) -> int:
        """
        Retorna o código da região para o ponto (x, y).
        @param x: Coordenada x do ponto.
        @param y: Coordenada y do ponto.
        @return: Código da região.
        """

        code = cls.INSIDE

        if x < x_min:
            code |= cls.LEFT
        elif x > x_max:
            code |= cls.RIGHT
        if y < y_min:
            code |= cls.BOTTOM
        elif y > y_max:
            code |= cls.TOP

        return code

    @classmethod
    def cohen_sutherland_clipping(
        cls,
        p1: tuple[float, float],
        p2: tuple[float, float],
    ) -> tuple[tuple[float, float], tuple[float, float]] | None:
        """
        Algoritmo de Cohen-Sutherland para recorte de linhas.
        @param p1: Primeiro ponto da linha.
        @param p2: Segundo ponto da linha.
        @return: Tupla com os pontos recortados da linha ou None se a linha estiver fora do viewport.
        """

        y_min, y_max = -1, 1
        x_min, x_max = -1, 1
        x1, y1 = p1
        x2, y2 = p2

        code1 = cls._get_region_code(x1, y1, x_min, y_min, x_max, y_max)
        code2 = cls._get_region_code(x2, y2, x_min, y_min, x_max, y_max)

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

            if code_outside & cls.TOP:
                intersection_x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                intersection_y = y_max

            elif code_outside & cls.BOTTOM:
                intersection_x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                intersection_y = y_min

            elif code_outside & cls.RIGHT:
                intersection_y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                intersection_x = x_max

            elif code_outside & cls.LEFT:
                intersection_y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                intersection_x = x_min

            if code_outside == code1:
                x1, y1 = intersection_x, intersection_y
                code1 = cls._get_region_code(x1, y1, x_min, y_min, x_max, y_max)
            else:
                x2, y2 = intersection_x, intersection_y
                code2 = cls._get_region_code(x2, y2, x_min, y_min, x_max, y_max)

        if accepted:
            return [(x1, y1), (x2, y2)]
        return None

    @classmethod
    def liang_barsky_clipping(
        cls, p1: tuple[float, float], p2: tuple[float, float]
    ) -> tuple | None:
        """
        Algoritmo de Liang-Barsky para recorte de linhas.
        @param p1: Primeiro ponto da linha.
        @param p2: Segundo ponto da linha.
        @return: Tupla com os pontos recortados da linha em coordenadas normalizadas ou None se a linha
        estiver fora do Viewport.
        """

        x_min, x_max = -1, 1
        y_min, y_max = -1, 1

        start_x, start_y = p1
        end_x, end_y = p2

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

    @classmethod
    def sutherland_hodgman_clipping(cls, points: list) -> list | None:
        """
        Algoritmo de Sutherland-Hodgman para recorte de polígonos.
        @param points: Lista de pontos do polígono.
        @return: Lista com os pontos recortados ou None se o polígono estiver fora do Viewport.
        """

        all_inside = True
        for point in points:
            x, y = point
            if not (-1 <= x <= 1 and -1 <= y <= 1):
                all_inside = False
                break

        # Polígono totalmente dentro, dispensa o recorte
        if all_inside:
            return points

        # Define o polígono de recorte (borda do viewport em coordenadas normalizadas)
        clip_window = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        clip_edges = list(zip(clip_window, clip_window[1:] + [clip_window[0]]))

        clipped_polygon = points[:]

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

    @classmethod
    def curve_clipping(cls, points: list, line_clipper: callable) -> list | None:
        """
        Algoritmo de recorte de curvas.
        @param points: Lista de pontos da curva (representação discretizada).
        @return: Lista de listas com os pontos recortados ou None se a curva estiver fora do Viewport.
        """

        clipped_parts = []  # Cada pedaço recortado da curva
        current_part = []  # Pedaço atual

        for i in range(len(points) - 1):
            # Converte para tupla para evitar problemas de comparação com numpy
            current_point = tuple(points[i])
            next_point = tuple(points[i + 1])

            clipped_segment = line_clipper(current_point, next_point)

            if clipped_segment is not None:
                clip_start, clip_end = clipped_segment

                if (
                    np.isclose(current_point[0], clip_start[0])
                    and np.isclose(current_point[1], clip_start[1])
                    and np.isclose(next_point[0], clip_end[0])
                    and np.isclose(next_point[1], clip_end[1])
                ):
                    # Segmento completamente dentro do viewport, continua current_part

                    # Apenda apenas o ponto atual para evitar duplicação quando o
                    # current_point se tornar next_point
                    current_part.append(current_point)

                    if i == len(points) - 2:
                        # Último segmento, adiciona o próximo ponto (caso contrário, ele não seria incluído)
                        current_part.append(next_point)

                else:
                    if np.isclose(current_point[0], clip_start[0]) and np.isclose(
                        current_point[1], clip_start[1]
                    ):
                        # Segmento começa dentro e termina fora
                        # current_point...ponto de interseção...next_point (fora)
                        current_part.append(current_point)
                        current_part.append(clip_end)
                        clipped_parts.append(current_part)
                        current_part = []

                    elif np.isclose(next_point[0], clip_end[0]) and np.isclose(
                        next_point[1], clip_end[1]
                    ):
                        # Segmento começa fora e termina dentro
                        # (fora)...ponto de interseção...next_point
                        current_part = [clip_start, next_point]
                    else:
                        # Segmento começa fora e termina fora
                        clipped_parts.append([clip_start, clip_end])
            else:
                if current_part:
                    clipped_parts.append(current_part)
                    current_part = []

        # Adiciona o último pedaço se houver
        if current_part and len(current_part) >= 2:
            clipped_parts.append(current_part)

        if clipped_parts:
            return clipped_parts

        return None
