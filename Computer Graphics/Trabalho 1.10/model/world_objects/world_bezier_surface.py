import numpy as np

from model.world_objects.sc_world_object import SCWorldObject
from view.graphical_objects.graphical_line import GraphicalLine


class WorldBezierSurface(SCWorldObject):
    """Classe pertinente a superfícies de Bézier cúbicas no mundo."""

    def __init__(
        self,
        points: list[list[list[float]]],
        name: str,
        color: tuple[int, int, int],
        viewport_bounds,
    ):
        """
        @param points_matrix_4x4x3: Matriz 4x4 de pontos de controle 3D [x,y,z].
                                     Formato: [[[x,y,z], [x,y,z], ...], ...]
        """

        self.control_points_3d_matrix = np.array(
            points, dtype=float
        )  # matriz 4x4x3 de pontos de controle 3D [x,y,z]
        matrix_converted_to_flat = [
            self.control_points_3d_matrix[i, j, :].tolist()
            for i in range(4)
            for j in range(4)
        ]  # lista de pontos para WorldObject

        super().__init__(matrix_converted_to_flat, name, color, viewport_bounds)

        self.obj_type = "bezier_surface"

        # definição da superfície de Bézier
        self.num_steps_s = 20
        self.num_steps_t = 20

        # Matriz de base de Bézier
        self.MB = np.array(
            [[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]], dtype=float
        )

        self.MBT = self.MB.T  # Transposta da matriz de base

        # Matrizes de geometria para cada coordenada (X, Y, Z)
        self.Gx = np.zeros((4, 4), dtype=float)
        self.Gy = np.zeros((4, 4), dtype=float)
        self.Gz = np.zeros((4, 4), dtype=float)
        self._populate_geometry_matrices()  # Preenche Gx, Gy, Gz com os pontos de controle iniciais

        # grade de pontos 3D da superfície
        self.world_surface_grid: list[list[tuple[float, float, float]]] = []
        self.normalized_surface_grid: list[list[tuple[float, float] | None]] = []
        self.projection_points: np.ndarray | None = None

    def _populate_geometry_matrices(self) -> None:
        """Preenche as matrizes Gx, Gy, Gz a partir dos pontos de controle 3D (self.control_points_3d_matrix)."""

        for i in range(4):
            for j in range(4):
                self.Gx[i, j] = self.control_points_3d_matrix[i, j, 0]
                self.Gy[i, j] = self.control_points_3d_matrix[i, j, 1]
                self.Gz[i, j] = self.control_points_3d_matrix[i, j, 2]

    def update_coordinates(self, composite_matrix: np.ndarray) -> None:
        """
        Sobrescreve o método update_coordinates da classe base WorldObject. Para tratar transformações.
        @param composite_matrix: Matriz de transformação composta.
        ***
        Método inteiramente gerado por IA
        - Modelo utilizado: gemini-2.5-pro-exp-05-06
        - URL da implementação do modelo: https://aistudio.google.com/
        - Finalidade: Implementar a lógica de atualização das coordenadas dos pontos de controle da superfície de Bézier.
        - Prompt empregado: crie um método que atualize as coordenadas dos pontos de controle da superfície de Bézier aplicando uma matriz de transformação composta.
        ***
        """

        new_control_points_3d_matrix = np.zeros_like(self.control_points_3d_matrix)
        for i in range(4):
            for j in range(4):
                point_3d = self.control_points_3d_matrix[i, j, :]
                point_4d_homogeneous = np.array(
                    [point_3d[0], point_3d[1], point_3d[2], 1.0]
                )
                transformed_point_4d = point_4d_homogeneous @ composite_matrix

                w = transformed_point_4d[3]
                if abs(w) < 1e-9:
                    new_control_points_3d_matrix[i, j, :] = transformed_point_4d[:3]
                elif w != 1.0:
                    new_control_points_3d_matrix[i, j, :] = transformed_point_4d[:3] / w
                else:
                    new_control_points_3d_matrix[i, j, :] = transformed_point_4d[:3]

        self.control_points_3d_matrix = new_control_points_3d_matrix
        self._populate_geometry_matrices()

        updated_flat_points_homogeneous = []
        for r in range(4):
            for c in range(4):
                pt = self.control_points_3d_matrix[r, c, :]
                updated_flat_points_homogeneous.append(
                    np.array([pt[0], pt[1], pt[2], 1.0])
                )
        self.world_points = updated_flat_points_homogeneous

    def _calculate_surface_point_3d(
        self, s: float, t: float
    ) -> tuple[float, float, float]:
        """Calcula um ponto 3D (X, Y, Z) na superfície para dados s e t usando as matrizes de geometria atuais.
        Utilizando a fórmula de Bézier para superfícies paramétricas.

        @param s: Parâmetro s da superfície de Bézier.
        @param t: Parâmetro t da superfície de Bézier.
        @return: Ponto 3D (X, Y, Z) na superfície.
        """

        S_vec = np.array([s**3, s**2, s, 1])  # vetor s
        T_vec_col = np.array([[t**3], [t**2], [t], [1]])  # vetor coluna

        # Q(s,t) = S * MB * G * MB_T * T_col
        x_coord = S_vec @ self.MB @ self.Gx @ self.MBT @ T_vec_col
        y_coord = S_vec @ self.MB @ self.Gy @ self.MBT @ T_vec_col
        z_coord = S_vec @ self.MB @ self.Gz @ self.MBT @ T_vec_col

        return float(x_coord), float(y_coord), float(z_coord)

    def _generate_project_and_transform_grid(self) -> None:
        """
        Gera a grade de pontos 3D da superfície no espaço do mundo,
        projeta-os para coordenadas normalizadas (NDC) e armazena-os.
        A transformação para viewport será feita após o clipping dos segmentos em NDC.
        """

        # se a matriz de projeção não está definida, não gera a grade
        if self.projection_points is None:
            self.world_surface_grid = []
            self.normalized_surface_grid = []
            return

        self.world_surface_grid = []
        self.normalized_surface_grid = []

        # vai iterando sobre o parametro s
        for i in range(self.num_steps_s + 1):
            s = i / self.num_steps_s
            world_row: list[tuple[float, float, float]] = []
            normalized_row: list[tuple[float, float] | None] = []

            # vai iterando sobre o parametro t
            for j in range(self.num_steps_t + 1):
                t = j / self.num_steps_t

                # pega o valor do ponto e adiciona na lista
                xw, yw, zw = self._calculate_surface_point_3d(s, t)
                world_row.append((xw, yw, zw))

                # ponto homogêneo no mundo
                point_wc_h = np.array([xw, yw, zw, 1.0])
                projected_h = point_wc_h @ self.projection_points

                # pega o valor de w do ponto projetado
                w_clip = projected_h[3]
                if w_clip <= 1e-6:  # caso for muito pequeno ou negativo, nao desenha
                    normalized_row.append(None)
                    continue

                # normalização para projeção
                xn = projected_h[0] / w_clip
                yn = projected_h[1] / w_clip

                normalized_row.append((xn, yn))

            self.world_surface_grid.append(world_row)
            self.normalized_surface_grid.append(normalized_row)

    def get_clipped_representation(self) -> list[GraphicalLine]:
        """
        Gera, projeta e transforma os pontos da superfície para o viewport.
        Retorna a representação gráfica para desenho.
        O clipping 2D da malha (se necessário) seria idealmente feito aqui antes de criar o GraphicalObject.
        Por simplicidade, esta versão passa a grade completa para GraphicalBezierSurface.
        ***
        Método parcialmente gerado por IA
        - Modelo utilizado: gemini-2.5-pro-exp-05-06
        - URL da implementação do modelo: https://aistudio.google.com/
        - Finalidade: Implementar a lógica de geração e clipping da grade de pontos da superfície de Bézier.
        - Prompt empregado: Implemente o método get_clipped_representation para a classe WorldBezierSurface.
        ***
        """

        self._generate_project_and_transform_grid()

        clipped_graphical_lines: list[GraphicalLine] = []

        # 1. desenha as linhas na direção S
        for t_idx in range(len(self.normalized_surface_grid[0])):
            for s_idx in range(len(self.normalized_surface_grid) - 1):
                p1_ndc = self.normalized_surface_grid[s_idx][t_idx]
                p2_ndc = self.normalized_surface_grid[s_idx + 1][t_idx]

                if p1_ndc is not None and p2_ndc is not None:
                    clipped_ndc_segment = self.clipping_mode(p1_ndc, p2_ndc)

                    if clipped_ndc_segment is not None:
                        viewport_points = self.transform_projection_points_to_viewport(
                            clipped_ndc_segment
                        )
                        graphical_line = GraphicalLine(viewport_points, self.color)
                        clipped_graphical_lines.append(graphical_line)

        # 2. desenha as linhas na direção T
        for s_idx in range(len(self.normalized_surface_grid)):
            for t_idx in range(len(self.normalized_surface_grid[0]) - 1):
                p1_ndc = self.normalized_surface_grid[s_idx][t_idx]
                p2_ndc = self.normalized_surface_grid[s_idx][t_idx + 1]

                if p1_ndc is not None and p2_ndc is not None:
                    clipped_ndc_segment = self.clipping_mode(p1_ndc, p2_ndc)

                    if clipped_ndc_segment is not None:
                        viewport_points = self.transform_projection_points_to_viewport(
                            clipped_ndc_segment
                        )
                        graphical_line = GraphicalLine(viewport_points, self.color)
                        clipped_graphical_lines.append(graphical_line)

        return clipped_graphical_lines

    def get_center(self) -> tuple[float, float, float]:
        """
        Retorna o centro geométrico dos 16 pontos de controle da superfície.
        """

        if self.control_points_3d_matrix.size == 0:
            return 0.0, 0.0, 0.0

        center_x = np.mean(self.control_points_3d_matrix[:, :, 0])
        center_y = np.mean(self.control_points_3d_matrix[:, :, 1])
        center_z = np.mean(self.control_points_3d_matrix[:, :, 2])
        return center_x, center_y, center_z

    def get_obj_description(self, last_index: int) -> tuple[str, int]:
        """
        Sobrescreve o método get_obj_description da classe base WorldObject para conseguir trabalhar com matrizes 4x4x3
        """
        obj_description = f"o {self.name}\n"

        # Escreve os 16 pontos de controle 3D
        for i in range(4):
            for j in range(4):
                pt = self.control_points_3d_matrix[i, j, :]
                obj_description += f"v {pt[0]:.4f} {pt[1]:.4f} {pt[2]:.4f}\n"

        obj_points = " ".join(str(i) for i in range(last_index, last_index + 16))
        obj_description += f"{self.obj_type} {obj_points}\n\n"

        return obj_description, last_index + 16

    def update_world_coordinates(self, conversion_mtx):
        """
        Atualiza as coordenadas do mundo da superfície de Bézier.
        @param conversion_mtx: Matriz de conversão.
        """

        self.world_points = []

        # Convertemos cada ponto de controle para as coordenadas do mundo
        for perceived_point in self.perceived_points:
            homogeneous_point = perceived_point
            world_point = homogeneous_point @ conversion_mtx
            self.world_points.append(world_point)

        # Atualizamos também a matriz de pontos de controle 3D
        for i in range(4):
            for j in range(4):
                idx = i * 4 + j
                self.control_points_3d_matrix[i, j, :] = self.world_points[idx][:3]

        # Recalculamos as matrizes de geometria
        self._populate_geometry_matrices()
