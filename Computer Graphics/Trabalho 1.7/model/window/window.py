import numpy as np

from model.transformation_generator import TransformationGenerator
from model.window.window_bounds import WindowBounds
from view.viewport.viewport_bounds import ViewportBounds


class Window:
    """Classe que representa a janela de visualização."""

    def __init__(self, viewport_bounds: ViewportBounds):
        """
        Como o tamanho do viewport é determinado em tempo de execução,
        adequamos o tamanho da janela de visualização para manter a proporção. De
        outra forma, a imagem seria distorcida.
        """

        viewport_width = viewport_bounds.x_lower_right - viewport_bounds.x_upper_left
        viewport_height = viewport_bounds.y_lower_right - viewport_bounds.y_upper_left
        aspect_ratio = viewport_width / viewport_height

        # Foco (pivot) em (0,0,0) e câmera inicial em (0,0,-40)
        self.focus = np.array([0.0, 0.0, 0.0, 1.0])
        self.yaw = 0.0  # rotação horizontal (graus)
        self.pitch = 0.0  # rotação vertical (graus)
        self.roll = 0.0  # spin da câmera

        # Janela ortográfica (magnitudes locais)
        height = 20.0
        width = height * aspect_ratio
        self.initial_height = height
        self.initial_width = width
        self.zoom_level = 1.0
        self.width = width
        self.height = height

        # Bounds locais, apenas para referência (não gira)
        self.window_bounds = WindowBounds(
            x_lower_left=-self.width,
            x_upper_right=self.width,
            y_lower_left=-self.height,
            y_upper_right=self.height,
            z_lower_left=0.0,
            z_upper_right=0.0,
        )
        # Inicializa posição da câmera usando pivot (focus) e raio
        # Posição inicial atrás do foco no eixo Z
        self.window_center = np.array([0.0, 0.0, 0.01, 1.0])
        # Inicializa vetores da câmera (VPN, VUP, VRIGHT)
        self._update_camera_vectors()

    def _update_camera_vectors(self) -> None:
        """
        Atualiza apenas os vetores da câmera sem modificar sua posição.

        Calcula:
        - view_plane_normal (VPN): vetor normal ao plano de visualização
        - vup: vetor de orientação "para cima"
        - vright: vetor de orientação "para a direita"
        """
        # Cálculo do VPN (view_plane_normal)
        vpn = self.focus[:3] - self.window_center[:3]
        vpn /= np.linalg.norm(vpn)

        # Cálculo dos eixos UVN do sistema de coordenadas da câmera
        world_up = np.array([0.0, 1.0, 0.0])
        vright = np.cross(vpn, world_up)
        if np.linalg.norm(vright) < 1e-6:
            vright = np.cross(vpn, np.array([0.0, 0.0, 1.0]))
        vright /= np.linalg.norm(vright)
        vup = np.cross(vright, vpn)
        vup /= np.linalg.norm(vup)

        # Aplica roll (rotação em torno do eixo VPN)
        if abs(self.roll) > 1e-3:
            Rr = TransformationGenerator.get_rotation_around_axis_through_origin(
                vpn, self.roll
            )
            vup4 = np.array([*vup, 0.0])
            vup = (vup4 @ Rr)[:3]
            vup /= np.linalg.norm(vup)
            vright = np.cross(vpn, vup)
            vright /= np.linalg.norm(vright)

        # Armazena vetores homogêneos para uso na projeção
        self.vup = np.array([vup[0], vup[1], vup[2], 1.0])
        self.vright = np.array([vright[0], vright[1], vright[2], 1.0])
        self.view_plane_normal = np.array([vpn[0], vpn[1], vpn[2], 1.0])

    def apply_zoom(self, zoom_percent: float) -> None:
        """
        Aplica zoom ortográfico ajustando largura e altura da janela.

        No algoritmo de projeção paralela, o zoom afeta o tamanho da janela
        usado na normalização (Passo 5).

        @param zoom_percent: Percentual de zoom (100% = tamanho original)
        """
        self.zoom_level = 1 / (zoom_percent / 100.0)
        self.width = self.initial_width * self.zoom_level
        self.height = self.initial_height * self.zoom_level

    def apply_pan(self, d_horizontal: float, d_vertical: float, d_depth: float) -> None:
        """
        Move a câmera na direção especificada.

        No algoritmo de projeção paralela, isso afeta o VRP (window_center)
        usado no Passo 1 (translação para origem).

        @param d_horizontal: Deslocamento horizontal
        @param d_vertical: Deslocamento vertical
        @param d_depth: Deslocamento em profundidade
        """
        # Calcula o vetor de deslocamento nas direções da câmera
        offset = (
            d_horizontal * self.vright[:3]
            + d_vertical * -self.vup[:3]
            + d_depth * self.view_plane_normal[:3]
        )

        # Move a câmera (window_center) diretamente
        self.window_center[:3] -= offset

        # Move o foco para manter a mesma direção de visão
        self.focus[:3] -= offset

        # A orientação (VPN, VUP, VRIGHT) não muda durante o pan.
        # Portanto, não chamamos _update_camera_vectors() aqui.

    def apply_rotation(self, angle_delta: float, axis: str) -> None:
        """
        Rotaciona a câmera no sistema local UVN.
        - horizontal: rota em torno do eixo VUP (gira view para esquerda/direita)
        - vertical: rota em torno do eixo VRIGHT (gira view para cima/baixo)
        - spin: rota em torno do eixo VPN (spin da câmera)

        @param angle_delta: Variação do ângulo em graus
        @param axis: Tipo de rotação ('horizontal', 'vertical', 'spin')
        """
        # Vetor direção da câmera (de focus para camera)
        dir_vec = self.window_center[:3] - self.focus[:3]
        # Seleciona eixo de rotação LOCAL (UVN)
        if axis == "horizontal":  # Rotação em torno do VUP local
            axis_vec = self.vup[:3]
        elif axis == "vertical":  # Rotação em torno do VRIGHT local
            axis_vec = self.vright[:3]
        elif axis == "spin":  # Rotação em torno do VPN local
            axis_vec = self.view_plane_normal[:3]
        else:
            return
        # Normaliza o eixo para segurança
        axis_vec_norm = np.linalg.norm(axis_vec)
        if axis_vec_norm < 1e-9:
            return  # Evita divisão por zero se o vetor for nulo
        axis_vec /= axis_vec_norm

        # Calcula matriz de rotação em torno do eixo local
        R = TransformationGenerator.get_rotation_around_axis_through_origin(
            axis_vec, angle_delta
        )

        # Spin: rotaciona vetores VUP e VRIGHT
        if axis == "spin":
            vup4 = np.array([*self.vup[:3], 0.0])
            vright4 = np.array([*self.vright[:3], 0.0])
            new_vup = (vup4 @ R)[:3]
            if np.linalg.norm(new_vup) > 1e-9:
                new_vup /= np.linalg.norm(new_vup)
            new_vright = (vright4 @ R)[:3]
            if np.linalg.norm(new_vright) > 1e-9:
                new_vright /= np.linalg.norm(new_vright)
            self.vup = np.array([*new_vup, 1.0])
            self.vright = np.array([*new_vright, 1.0])
            return  # VPN não muda no spin

        # Rotação Vertical (em torno de VRIGHT): Rotaciona VUP, VPN e Posição
        if axis == "vertical":
            vpn4 = np.array([*self.view_plane_normal[:3], 0.0])
            vup4 = np.array([*self.vup[:3], 0.0])
            dir4 = np.array([*dir_vec, 0.0])

            new_vpn = (vpn4 @ R)[:3]
            new_vup = (vup4 @ R)[:3]
            rotated_dir = (dir4 @ R)[:3]

            if np.linalg.norm(new_vpn) > 1e-9:
                new_vpn /= np.linalg.norm(new_vpn)
            if np.linalg.norm(new_vup) > 1e-9:
                new_vup /= np.linalg.norm(new_vup)

            self.view_plane_normal = np.array([*new_vpn, 1.0])
            self.vup = np.array([*new_vup, 1.0])
            # VRIGHT (eixo de rotação) não muda
            self.window_center[:3] = self.focus[:3] + rotated_dir
            return

        # Rotação Horizontal (em torno de VUP): Rotaciona VRIGHT, VPN e Posição
        if axis == "horizontal":
            vpn4 = np.array([*self.view_plane_normal[:3], 0.0])
            vright4 = np.array([*self.vright[:3], 0.0])
            dir4 = np.array([*dir_vec, 0.0])

            new_vpn = (vpn4 @ R)[:3]
            new_vright = (vright4 @ R)[:3]
            rotated_dir = (dir4 @ R)[:3]

            if np.linalg.norm(new_vpn) > 1e-9:
                new_vpn /= np.linalg.norm(new_vpn)
            if np.linalg.norm(new_vright) > 1e-9:
                new_vright /= np.linalg.norm(new_vright)

            self.view_plane_normal = np.array([*new_vpn, 1.0])
            self.vright = np.array([*new_vright, 1.0])
            # VUP (eixo de rotação) não muda
            self.window_center[:3] = self.focus[:3] + rotated_dir
            return

    def get_width(self) -> float:
        """
        Retorna a largura da janela.

        Usado no Passo 5 do algoritmo de projeção paralela (normalização).
        """
        return self.width

    def get_height(self) -> float:
        """
        Retorna a altura da janela.

        Usado no Passo 5 do algoritmo de projeção paralela (normalização).
        """
        return self.height
