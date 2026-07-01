import numpy as np


class TransformationGenerator:
    """
    Classe responsável por gerar matrizes de transformação.
    """

    @staticmethod
    def get_composite_transformation_matrix(
        transformations_list: list[dict], obj_center: tuple[float, float, float]
    ) -> np.ndarray | None:
        """
        Método para obtenção de uma matriz de transformação composta.
        @param transformations_list: Lista de dicionários, cada um representando uma transformação.
        @param obj_center: Centro do objeto a ser transformado. Usado no escalonamento e na rotação.
        @return: Matriz que produzirá uma transformação equivalente a todas as transformações individuais.
        None se a lista estiver vazia.
        """

        if not transformations_list:
            return None

        # Inicializa a matriz composta como a matriz identidade
        composite_matrix = np.identity(4)

        for transformation in transformations_list:
            transformation_type = transformation["type"]
            matrix = np.identity(4)

            if transformation_type == "translation":
                dx = transformation["dx"]
                dy = transformation["dy"]
                dz = transformation["dz"]
                matrix = TransformationGenerator.get_translation_matrix(dx, dy, dz)

            elif transformation_type == "scaling":
                sx = transformation["sx"]
                sy = transformation["sy"]
                sz = transformation["sz"]

                center_x, center_y, center_z = obj_center
                center_transformed = (
                    np.array([center_x, center_y, center_z, 1]) @ composite_matrix
                )
                cx_current, cy_current, cz_current = (
                    center_transformed[0],
                    center_transformed[1],
                    center_transformed[2],
                )

                matrix = TransformationGenerator.get_scaling_matrix(
                    cx_current, cy_current, cz_current, sx, sy, sz
                )

            elif transformation_type == "rotation":
                angle = transformation["angle"]
                x1 = transformation["x1"]
                y1 = transformation["y1"]
                z1 = transformation["z1"]
                x2 = transformation["x2"]
                y2 = transformation["y2"]
                z2 = transformation["z2"]
                axis = transformation["axis"]

                if axis == "X":
                    matrix = TransformationGenerator.get_x_axis_rotation_matrix(angle)
                elif axis == "Y":
                    matrix = TransformationGenerator.get_y_axis_rotation_matrix(angle)
                elif axis == "Z":
                    matrix = TransformationGenerator.get_z_axis_rotation_matrix(angle)
                elif axis == "arbitrary":
                    matrix = TransformationGenerator.get_arbitrary_rotation_matrix(
                        angle, (x1, y1, z1), (x2, y2, z2)
                    )
                else:
                    raise ValueError(f"Eixo de rotação inválido: {axis}")

            composite_matrix = composite_matrix @ matrix

        return composite_matrix

    @staticmethod
    def get_x_axis_rotation_matrix(angle_degrees: float) -> np.ndarray:
        """
        Obtém a matriz de rotação em torno do eixo x.
        @return: Matriz de rotação em torno do eixo x.
        """

        angle_radians = np.radians(angle_degrees)
        cos_r = np.cos(angle_radians)
        sin_r = np.sin(angle_radians)

        return np.array(
            [
                [1, 0, 0, 0],
                [0, cos_r, sin_r, 0],
                [0, -sin_r, cos_r, 0],
                [0, 0, 0, 1],
            ]
        )

    @staticmethod
    def get_y_axis_rotation_matrix(angle_degrees: float) -> np.ndarray:
        """
        Obtém a matriz de rotação em torno do eixo y.
        @param angle_degrees: Ângulo de rotação em graus.
        @return: Matriz de rotação em torno do eixo y.
        """
        angle_radians = np.radians(angle_degrees)
        cos_r = np.cos(angle_radians)
        sin_r = np.sin(angle_radians)
        return np.array(
            [
                [cos_r, 0, -sin_r, 0],
                [0, 1, 0, 0],
                [sin_r, 0, cos_r, 0],
                [0, 0, 0, 1],
            ]
        )

    @staticmethod
    def get_z_axis_rotation_matrix(angle_degrees: float) -> np.ndarray:
        """
        Obtém a matriz de rotação em torno do eixo z.
        @param angle_degrees: Ângulo de rotação em graus.
        @return: Matriz de rotação em torno do eixo z.
        """
        angle_radians = np.radians(angle_degrees)
        cos_r = np.cos(angle_radians)
        sin_r = np.sin(angle_radians)
        return np.array(
            [
                [cos_r, sin_r, 0, 0],
                [-sin_r, cos_r, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )

    @staticmethod
    def get_arbitrary_rotation_matrix(
        angle_degrees: float,
        p1: tuple[float, float, float],
        p2: tuple[float, float, float],
    ) -> np.ndarray:
        """
        Obtém a matriz de rotação em torno de um eixo arbitrário que passa pela origem e pelo ponto (x, y, z).
        @param angle_degrees: Ângulo de rotação em graus.
        @param p1: Ponto 1 (x, y, z) que define o eixo de rotação.
        @param p2: Ponto 2 (x, y, z) que define o eixo de rotação. Forma uma reta com p1.
        @return: Matriz de rotação em torno do eixo arbitrário.
        """

        x1 = p1[0]
        y1 = p1[1]
        z1 = p1[2]

        x2 = p2[0]
        y2 = p2[1]
        z2 = p2[2]

        # Passo 1. Translação do sistema objeto/eixo de forma que um ponto do eixo fique sobre a origem
        translate_to_origin = TransformationGenerator.get_translation_matrix(
            dx=-x1, dy=-y1, dz=-z1
        )

        # Passo 2. Rotação Rx em torno do eixo x por θx de forma a trazer o eixo sobre o plano xy
        # Calcula o ângulo entre o eixo arbitrário projetado no plano xz e o plano xy
        theta_x = np.arctan2(z2 - z1, y2 - y1)

        rotate_x = TransformationGenerator.get_x_axis_rotation_matrix(
            -np.degrees(theta_x)
        )

        # Passo 3. Rotação Rz em torno do eixo z por θz de forma a alinhar o eixo com o eixo y
        # Calcula o ângulo entre a projeção do eixo no plano xy e o eixo y
        axis_vector = np.array([x2 - x1, y2 - y1, z2 - z1, 0])
        axis_after_rx = axis_vector @ rotate_x
        theta_z = np.arctan2(axis_after_rx[0], axis_after_rx[1])
        rotate_z = TransformationGenerator.get_z_axis_rotation_matrix(
            np.degrees(theta_z)
        )

        # Passo 4. Rotação Ry em torno do eixo y pelo ângulo dado pelo usuário
        rotate_y = TransformationGenerator.get_y_axis_rotation_matrix(angle_degrees)

        # Passo 5. Desfaz a rotação do passo 3
        revert_z_rotation = TransformationGenerator.get_z_axis_rotation_matrix(
            -np.degrees(theta_z)
        )

        # Passo 6. Desfaz a rotação do passo 2
        revert_x_rotation = TransformationGenerator.get_x_axis_rotation_matrix(
            np.degrees(theta_x)
        )

        # Passo 7. Translação de volta para a posição original
        translate_back = TransformationGenerator.get_translation_matrix(
            dx=x1, dy=y1, dz=z1
        )

        # Composição das transformações
        transformation = (
            translate_to_origin
            @ rotate_x
            @ rotate_z
            @ rotate_y
            @ revert_z_rotation
            @ revert_x_rotation
            @ translate_back
        )

        return transformation

    @staticmethod
    def get_pan_matrix(
        d_vertical: float,
        d_horizontal: float,
        d_depth: float,
        window_vup: np.ndarray,
        window_vright: np.ndarray,
        view_plane_normal: np.ndarray,
    ) -> np.ndarray:
        """
        Obtém a matriz de pan.
        @param d_vertical: Deslocamento vertical.
        @param d_horizontal: Deslocamento horizontal.
        @param d_depth: Deslocamento em profundidade.
        @param window_vup: Vetor Vup da janela (indicando a direção "para cima").
        @param window_vright: Vetor Vright da janela (indicando a direção "para a direita").
        @param view_plane_normal: Vetor normal ao plano de visão.
        @return: Matriz de pan.
        """

        window_vup_x, window_vup_y, window_vup_z, _ = window_vup
        window_vright_x, window_vright_y, window_vright_z, _ = window_vright
        view_plane_normal_x, view_plane_normal_y, view_plane_normal_z, _ = (
            view_plane_normal
        )

        # Para mover numa dada direção, multiplicamos o vetor unitário da janela pelo deslocamento.
        # Isto produz um vetor de deslocamento na direção desejada e com o comprimento desejado.
        translation_x = (
            d_horizontal * window_vright_x
            + d_vertical * window_vup_x
            + d_depth * view_plane_normal_x
        )
        translation_y = (
            d_horizontal * window_vright_y
            + d_vertical * window_vup_y
            + d_depth * view_plane_normal_y
        )
        translation_z = (
            d_horizontal * window_vright_z
            + d_vertical * window_vup_z
            + d_depth * view_plane_normal_z
        )

        pan_matrix = np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [translation_x, translation_y, translation_z, 1],
            ]
        )

        return pan_matrix

    @staticmethod
    def get_translation_matrix(dx: float, dy: float, dz: float) -> np.ndarray:
        """
        Obtém a matriz de translação.
        @param dx: Deslocamento em x.
        @param dy: Deslocamento em y.
        @param dz: Deslocamento em z.
        @return: Matriz de translação.
        """

        return np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [dx, dy, dz, 1],
            ]
        )

    @staticmethod
    def get_scaling_matrix(
        cx: float, cy: float, cz: float, scale_x: float, scale_y: float, scale_z: float
    ) -> np.ndarray:
        """
        Obtém a matriz de escalonamento natural, isto é, em torno do centro do objeto.
        @param cx: Coordenada x do centro do objeto a ser escalonado.
        @param cy: Coordenada y do centro do objeto a ser escalonado.
        @param cz: Coordenada z do centro do objeto a ser escalonado.
        @param scale_x: Fator de escalonamento em x.
        @param scale_y: Fator de escalonamento em y.
        @param scale_z: Fator de escalonamento em z.
        @return: Matriz de escalonamento.
        """

        # Passo 1: Translação do centro do objeto para a origem
        translate_to_origin = TransformationGenerator.get_translation_matrix(
            dx=-cx, dy=-cy, dz=-cz
        )

        # Passo 2: Escalonamento
        scale_mtx = np.array(
            [
                [scale_x, 0, 0, 0],
                [0, scale_y, 0, 0],
                [0, 0, scale_z, 0],
                [0, 0, 0, 1],
            ]
        )

        # Passo 3: Translação de volta para a posição original
        translate_back = TransformationGenerator.get_translation_matrix(
            dx=cx, dy=cy, dz=cz
        )

        return translate_to_origin @ scale_mtx @ translate_back

    @staticmethod
    def get_ncs_matrix(
        window_width: float,
        window_height: float,
    ) -> np.ndarray:
        """
        Obtém a matriz de transformação para o sistema de coordenadas normalizadas (NCS).
        @param window_width: Largura da janela de visualização.
        @param window_height: Altura da janela de visualização.
        @return: Matriz de transformação para o sistema de coordenadas normalizadas.
        """

        scale_x = -2.0 / window_width  # Negativo pois o positivo fica à esquerda
        scale_y = 2.0 / window_height
        scale_to_ncs = TransformationGenerator.get_scaling_matrix(
            cx=0, cy=0, cz=0, scale_x=scale_x, scale_y=scale_y, scale_z=1
        )

        return scale_to_ncs

    @staticmethod
    def get_parallel_projection_points(
        window_width: float,
        window_height: float,
        **kwargs,
    ):
        """
        Método para obter a matriz de projeção paralela.
        @param window_width: Largura da janela de visualização.
        @param window_height: Altura da janela de visualização.
        @return: Matriz de projeção paralela.
        """

        # Passo 1: Ignorar z
        ignore_z = np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 1],
            ]
        )

        # Passo 2: Escalonar para o sistema de coordenadas normalizadas
        scale_to_ncs = TransformationGenerator.get_ncs_matrix(
            window_width=window_width,
            window_height=window_height,
        )

        return ignore_z @ scale_to_ncs

    @staticmethod
    def get_perspective_projection_points(
        window_width: float,
        window_height: float,
        **kwargs,
    ):
        """
        Método para obter a matriz de projeção perspectiva.
        @param center_of_projection: Centro de projeção (COP).
        @param window_width: Largura da janela de visualização.
        @param window_height: Altura da janela de visualização.
        @return: Matriz de projeção perspectiva.
        """

        center_of_projection = kwargs["center_of_projection"]

        # Passo 1: Translação do centro de projeção (COP) para a origem
        translate_cop_to_origin = TransformationGenerator.get_translation_matrix(
            dx=-center_of_projection[0],
            dy=-center_of_projection[1],
            dz=-center_of_projection[2],
        )

        # Passo 2: Cálculo da distância do COP ao plano de visualização e geração da matriz
        # que obtém o fator z/d
        distance_to_view_plane = np.linalg.norm(
            center_of_projection[:3] - np.array([0, 0, 0])
        )

        perspective_matrix = np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 1 / distance_to_view_plane],
                [0, 0, 0, 0],
            ]
        )

        # Passo 3: Escalonamento para o sistema de coordenadas normalizadas
        scale_to_ncs = TransformationGenerator.get_ncs_matrix(
            window_width=window_width,
            window_height=window_height,
        )

        return translate_cop_to_origin @ perspective_matrix @ scale_to_ncs
