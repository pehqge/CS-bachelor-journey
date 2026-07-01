import numpy as np

from model.world_objects.sc_world_object import SCWorldObject
from view.graphical_objects.graphical_line import GraphicalLine


class WorldBicubicSurface(SCWorldObject):
    """Classe referente a superfícies bicúbicas B-Spline no mundo."""

    def __init__(
        self,
        points: list[list[list[float]]],  # Matriz NxMx3 de pontos de controle
        name: str,
        color: tuple[int, int, int],
        viewport_bounds,
    ):
        """
        Inicializa uma superfície bicúbica B-Spline.

        @param points: Matriz NxMx3 de pontos de controle 3D [x,y,z].
                       N e M devem ser >= 4.
        @param name: Nome da superfície.
        @param color: Cor da superfície em RGB.
        @param viewport_bounds: Limites da viewport.
        """
        self.control_points_matrix_nxm = np.array(points, dtype=float)

        if (
            self.control_points_matrix_nxm.ndim != 3
            or self.control_points_matrix_nxm.shape[0] < 4
            or self.control_points_matrix_nxm.shape[1] < 4
        ):
            raise ValueError(
                f"A matriz de pontos de controle para '{name}' deve ser pelo menos 4x4x3. Recebido shape: {self.control_points_matrix_nxm.shape}"
            )

        # Converte para lista plana para o construtor da superclasse
        flat_perceived_points = [
            tuple(self.control_points_matrix_nxm[i, j, :])
            for i in range(self.control_points_matrix_nxm.shape[0])
            for j in range(self.control_points_matrix_nxm.shape[1])
        ]

        super().__init__(flat_perceived_points, name, color, viewport_bounds)

        self.obj_type = "bicubic_surface"

        self.num_steps_s = 10
        self.num_steps_t = 10

        self.M_bspline = (1 / 6) * np.array(
            [[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]], dtype=float
        )
        self.M_bspline_T = self.M_bspline.T

        self.Gx = np.zeros((4, 4), dtype=float)
        self.Gy = np.zeros((4, 4), dtype=float)
        self.Gz = np.zeros((4, 4), dtype=float)

        self.normalized_surface_patches_grids: list[
            list[list[tuple[float, float] | None]]
        ] = []
        self.projection_points_matrix: np.ndarray | None = None

    def _populate_patch_geometry_matrices(self, control_patch_4x4: np.ndarray) -> None:
        """
        Preenche as matrizes de geometria Gx, Gy, Gz para um retalho 4x4 específico.

        @param control_patch_4x4: Matriz 4x4x3 de pontos de controle do retalho.
        """
        for i in range(4):
            for j in range(4):
                self.Gx[i, j] = control_patch_4x4[i, j, 0]
                self.Gy[i, j] = control_patch_4x4[i, j, 1]
                self.Gz[i, j] = control_patch_4x4[i, j, 2]

    def _calculate_forward_difference_matrix_E(self, delta: float) -> np.ndarray:
        """
        Cria a matriz de forward differences E(delta).

        @param delta: O passo de discretização.
        @return: A matriz de forward differences E.
        """
        delta_sq = delta * delta
        delta_cb = delta_sq * delta
        return np.array(
            [
                [0, 0, 0, 1],
                [delta_cb, delta_sq, delta, 0],
                [6 * delta_cb, 2 * delta_sq, 0, 0],
                [6 * delta_cb, 0, 0, 0],
            ],
            dtype=float,
        )

    def _calculate_patch_points_3d_fwd_diff(
        self, control_patch_4x4: np.ndarray
    ) -> list[list[tuple[float, float, float]]]:
        """
        Calcula os pontos 3D de um retalho bicúbico B-Spline 4x4 usando Forward Differences.

        @param control_patch_4x4: Matriz 4x4x3 de pontos de controle do retalho.
        @return: Uma grade (lista de listas) de pontos 3D (x,y,z) do retalho.
        """
        self._populate_patch_geometry_matrices(control_patch_4x4)

        Cx = self.M_bspline @ self.Gx @ self.M_bspline_T
        Cy = self.M_bspline @ self.Gy @ self.M_bspline_T
        Cz = self.M_bspline @ self.Gz @ self.M_bspline_T

        delta_s = 1.0 / self.num_steps_s
        delta_t = 1.0 / self.num_steps_t

        E_ds = self._calculate_forward_difference_matrix_E(delta_s)
        E_dt_T = self._calculate_forward_difference_matrix_E(delta_t).T

        DDx = E_ds @ Cx @ E_dt_T
        DDy = E_ds @ Cy @ E_dt_T
        DDz = E_ds @ Cz @ E_dt_T

        patch_grid_3d: list[list[tuple[float, float, float]]] = [
            [(0, 0, 0)] * (self.num_steps_t + 1) for _ in range(self.num_steps_s + 1)
        ]

        current_DDx_s_iter = DDx.copy()
        current_DDy_s_iter = DDy.copy()
        current_DDz_s_iter = DDz.copy()

        for i in range(self.num_steps_s + 1):
            x, dx_t, d2x_t, d3x_t = (
                current_DDx_s_iter[0, 0],
                current_DDx_s_iter[0, 1],
                current_DDx_s_iter[0, 2],
                current_DDx_s_iter[0, 3],
            )
            y, dy_t, d2y_t, d3y_t = (
                current_DDy_s_iter[0, 0],
                current_DDy_s_iter[0, 1],
                current_DDy_s_iter[0, 2],
                current_DDy_s_iter[0, 3],
            )
            z, dz_t, d2z_t, d3z_t = (
                current_DDz_s_iter[0, 0],
                current_DDz_s_iter[0, 1],
                current_DDz_s_iter[0, 2],
                current_DDz_s_iter[0, 3],
            )

            for j in range(self.num_steps_t + 1):
                patch_grid_3d[i][j] = (x, y, z)
                x += dx_t
                dx_t += d2x_t
                d2x_t += d3x_t
                y += dy_t
                dy_t += d2y_t
                d2y_t += d3y_t
                z += dz_t
                dz_t += d2z_t
                d2z_t += d3z_t

            if i < self.num_steps_s:
                current_DDx_s_iter[0, :] += current_DDx_s_iter[1, :]
                current_DDx_s_iter[1, :] += current_DDx_s_iter[2, :]
                current_DDx_s_iter[2, :] += current_DDx_s_iter[3, :]

                current_DDy_s_iter[0, :] += current_DDy_s_iter[1, :]
                current_DDy_s_iter[1, :] += current_DDy_s_iter[2, :]
                current_DDy_s_iter[2, :] += current_DDy_s_iter[3, :]

                current_DDz_s_iter[0, :] += current_DDz_s_iter[1, :]
                current_DDz_s_iter[1, :] += current_DDz_s_iter[2, :]
                current_DDz_s_iter[2, :] += current_DDz_s_iter[3, :]

        return patch_grid_3d

    def _generate_project_and_transform_grid(self) -> None:
        """
        Gera a grade de pontos 3D da superfície completa (todos os retalhos),
        projeta-os para coordenadas normalizadas (NDC) e armazena os resultados
        em self.normalized_surface_patches_grids.
        """
        if self.projection_points_matrix is None:
            self.normalized_surface_patches_grids = []
            return

        self.normalized_surface_patches_grids = []
        num_patches_s = self.control_points_matrix_nxm.shape[0] - 3
        num_patches_t = self.control_points_matrix_nxm.shape[1] - 3

        if num_patches_s < 1 or num_patches_t < 1:
            return

        for patch_i in range(num_patches_s):
            for patch_j in range(num_patches_t):
                world_control_points_4x4_patch = np.zeros((4, 4, 3))
                for r_idx in range(4):
                    for c_idx in range(4):
                        flat_idx = (
                            patch_i + r_idx
                        ) * self.control_points_matrix_nxm.shape[1] + (patch_j + c_idx)
                        if flat_idx >= len(self.world_points):
                            return
                        world_control_points_4x4_patch[r_idx, c_idx, :] = (
                            self.world_points[flat_idx][:3]
                        )

                patch_world_grid = self._calculate_patch_points_3d_fwd_diff(
                    world_control_points_4x4_patch
                )

                normalized_patch_grid: list[list[tuple[float, float] | None]] = []
                for s_row in patch_world_grid:
                    normalized_s_row: list[tuple[float, float] | None] = []
                    for xw, yw, zw in s_row:
                        point_wc_h = np.array([xw, yw, zw, 1.0])
                        projected_h = point_wc_h @ self.projection_points_matrix

                        w_clip = projected_h[3]
                        if abs(w_clip) < 1e-9:
                            normalized_s_row.append(None)
                            continue

                        xn = projected_h[0] / w_clip
                        yn = projected_h[1] / w_clip

                        is_perspective = self.projection_points_matrix[3, 2] != 0
                        if is_perspective and w_clip < 0:
                            normalized_s_row.append(None)
                        else:
                            normalized_s_row.append((xn, yn))
                    normalized_patch_grid.append(normalized_s_row)
                self.normalized_surface_patches_grids.append(normalized_patch_grid)

    def update_projection_points(self, projection_matrix: np.ndarray) -> None:
        """
        Atualiza a matriz de projeção utilizada para transformar os pontos da superfície
        para coordenadas normalizadas (NDC) e marca o objeto como 'sujo' (dirty),
        indicando que sua representação precisa ser recalculada.

        @param projection_matrix: A nova matriz de projeção.
        """
        self.projection_points_matrix = projection_matrix
        self.dirty = True

    def get_clipped_representation(self) -> list[GraphicalLine]:
        """
        Gera a representação gráfica da superfície bicúbica após aplicar a projeção,
        o recorte (clipping) e a transformação para coordenadas de viewport.

        @return: Uma lista de objetos GraphicalLine representando os segmentos
                 visíveis da superfície na viewport. Retorna uma lista vazia se
                 não houver grades de patches normalizados ou se nenhum segmento
                 for visível após o recorte.
        """
        self._generate_project_and_transform_grid()

        clipped_graphical_lines: list[GraphicalLine] = []

        if not self.normalized_surface_patches_grids:
            return []

        for normalized_patch_grid in self.normalized_surface_patches_grids:
            num_rows_in_patch = len(normalized_patch_grid)
            num_cols_in_patch = (
                len(normalized_patch_grid[0]) if num_rows_in_patch > 0 else 0
            )

            for t_idx in range(num_cols_in_patch):
                for s_idx in range(num_rows_in_patch - 1):
                    p1_ndc = normalized_patch_grid[s_idx][t_idx]
                    p2_ndc = normalized_patch_grid[s_idx + 1][t_idx]

                    if p1_ndc and p2_ndc:
                        clipped_segment = self.clipping_mode(p1_ndc, p2_ndc)
                        if clipped_segment:
                            vp_points = self.transform_projection_points_to_viewport(
                                clipped_segment
                            )
                            clipped_graphical_lines.append(
                                GraphicalLine(vp_points, self.color)
                            )

            for s_idx in range(num_rows_in_patch):
                for t_idx in range(num_cols_in_patch - 1):
                    p1_ndc = normalized_patch_grid[s_idx][t_idx]
                    p2_ndc = normalized_patch_grid[s_idx][t_idx + 1]

                    if p1_ndc and p2_ndc:
                        clipped_segment = self.clipping_mode(p1_ndc, p2_ndc)
                        if clipped_segment:
                            vp_points = self.transform_projection_points_to_viewport(
                                clipped_segment
                            )
                            clipped_graphical_lines.append(
                                GraphicalLine(vp_points, self.color)
                            )

        return clipped_graphical_lines

    def get_center(self) -> tuple[float, float, float]:
        """
        Calcula o centro geométrico da superfície bicúbica com base em seus pontos de controle.

        O centro é determinado pela média das coordenadas x, y e z de todos os
        pontos de controle percebidos (perceived_points) da superfície.

        @return: Uma tupla (x, y, z) representando as coordenadas do centro.
                 Retorna (0.0, 0.0, 0.0) se não houver pontos de controle.
        """
        if not self.perceived_points:
            return 0.0, 0.0, 0.0

        all_x = [p[0] for p in self.perceived_points]
        all_y = [p[1] for p in self.perceived_points]
        all_z = [p[2] for p in self.perceived_points]

        center_x = np.mean(all_x) if all_x else 0.0
        center_y = np.mean(all_y) if all_y else 0.0
        center_z = np.mean(all_z) if all_z else 0.0
        return center_x, center_y, center_z

    def get_obj_description(self, last_index: int) -> tuple[str, int]:
        """
        Gera uma descrição da superfície bicúbica no formato Wavefront OBJ.

        A descrição inclui os vértices (pontos de controle) da superfície e uma
        linha especificando o tipo de objeto ('bicubic_surface'), suas dimensões N e M,
        e os índices dos seus pontos de controle.

        @param last_index: O último índice de vértice utilizado no arquivo OBJ,
                           para garantir que os novos índices sejam únicos.
        @return: Uma tupla contendo:
                 - A string da descrição do objeto no formato OBJ.
                 - O novo último índice de vértice após adicionar os pontos desta superfície.
        """
        obj_description = f"o {self.name}\n"

        num_total_control_points = len(self.perceived_points)

        for point_h in self.perceived_points:
            obj_description += f"v {point_h[0]:.4f} {point_h[1]:.4f} {point_h[2]:.4f}\n"

        N = self.control_points_matrix_nxm.shape[0]
        M = self.control_points_matrix_nxm.shape[1]

        obj_points_indices = " ".join(
            str(i) for i in range(last_index, last_index + num_total_control_points)
        )
        obj_description += f"{self.obj_type} {N} {M} {obj_points_indices}\n\n"

        return obj_description, last_index + num_total_control_points
