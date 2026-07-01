import os

import numpy as np

from model.window import Window
from model.world_object import WorldObject
from utils.obj_handler import ObjHandler
from view.view import View
from view.graphical_objects.point import Point
from view.graphical_objects.line import Line
from view.graphical_objects.wireframe import Wireframe

class Model:
    """Classe que representa o modelo da nossa arquitetura MVC."""

    def __init__(self, view: View):
        self.view = view
        self.window = Window(viewport_bounds=view.viewport.viewport_bounds)
        self.display_file = []

    @staticmethod
    def update_interface(func: callable) -> callable:
        """Decorator para atualizar a interface quando uma função é chamada."""

        def wrapper(*args, **kwargs):
            self = args[0]
            result = func(*args, **kwargs)

            # Recalcula as coordenadas normalizadas para todos os objetos
            self._calculate_and_update_scn()

            # Atualiza a View
            self.view.update_view_objects(self.display_file)

            return result

        return wrapper

    @update_interface
    def add_object(self, points: list, name: str, color: tuple) -> None:
        """Adiciona um objeto gráfico ao display file e atualiza a View."""
        
        # Confere se ja nao existe um objeto com os mesmos pontos
        if any(points == [(x, y) for x, y, *_ in objs.world_points] for objs in self.display_file):
            self.view.add_log(f"Object {name} already exists, skipping...")
            return
        
        if len(points) == 1:
            graphical_representation = Point(color)
        elif len(points) == 2:
            graphical_representation = Line(color)
        else:
            graphical_representation = Wireframe(color)
            
        tipo = graphical_representation.__class__.__name__
        
        if not name:
            name = f"{tipo} {len([obj for obj in self.display_file if obj.graphical_representation.__class__.__name__ == tipo]) + 1}"

        viewport_bounds = self.view.viewport.viewport_bounds
        world_object = WorldObject(points, name, viewport_bounds, graphical_representation)

        self.display_file.append(world_object)
        self.view.add_log(f"{tipo} {name} created: {points}")

    @update_interface
    def remove_object(self, index: int) -> None:
        """Remove um objeto do display file e atualiza a View."""

        self.display_file.pop(index)

    @update_interface
    def zoom(self, factor: float) -> None:
        """Aplica um zoom na janela de visualização e atualiza a View."""

        self.window.apply_zoom(factor)

    @update_interface
    def pan(self, dx: float, dy: float) -> None:
        """Aplica um pan na janela de visualização e atualiza a View."""

        # Rotaciona dx e dy pelo ângulo atual da window
        dx_world = dx * np.cos(self.window.angle) - dy * np.sin(self.window.angle)
        dy_world = dx * np.sin(self.window.angle) + dy * np.cos(self.window.angle)

        self.window.apply_pan(dx_world, dy_world)

    @update_interface
    def handle_transformations(self, index: int, transformations_list: list[dict]) -> None:
        """
        Processa uma lista de transformações em um objeto sequencialmente,
        compondo uma matriz única e aplicando-a ao final.
        @param index: Índice do objeto a ser transformado.
        @param transformations_list: Lista de dicionários, cada um representando uma transformação.
        """

        if not transformations_list:
            return

        # Inicializa a matriz composta como a matriz identidade
        composite_matrix = np.identity(3)

        obj = self.display_file[index]

        for transformation in transformations_list:
            transformation_type = transformation["type"]
            matrix = np.identity(3)

            if transformation_type == "translation":
                dx = transformation["dx"]
                dy = transformation["dy"]
                matrix = self.get_translation_matrix(dx, dy)
                self.view.add_log(f"{obj.name}: Translation ({dx}, {dy})")
            
            elif transformation_type == "scaling":
                sx = transformation["sx"]
                sy = transformation["sy"]
                center_x, center_y = obj.get_center()
                center_transformed = np.array([center_x, center_y, 1]) @ composite_matrix
                cx_current, cy_current = center_transformed[0], center_transformed[1]
                matrix = self.get_scaling_matrix(sx, sy, cx_current, cy_current)
                self.view.add_log(f"{obj.name}: Scaling ({sx*100:.1f}%, {sy*100:.1f}%)")
                
            elif transformation_type == "rotation":
                angle = transformation["angle"]
                cx = transformation["cx"]
                cy = transformation["cy"]
                
                if cx == "obj_center":
                    center_x, center_y = obj.get_center()
                    center_transformed = np.array([center_x, center_y, 1]) @ composite_matrix
                    cx_current, cy_current = center_transformed[0], center_transformed[1]
                    matrix = self.get_rotation_matrix(angle, cx_current, cy_current)
                else: # origem ou ponto arbitrario
                    matrix = self.get_rotation_matrix(angle, float(cx), float(cy))
                    
                self.view.add_log(f"{obj.name}: Rotation ({angle}°) around ({cx}, {cy})")

            composite_matrix = composite_matrix @ matrix 

        obj.update_coordinates(composite_matrix)

        self.view.add_log(f"{obj.name}: Transformations applied.")

    def _calculate_and_update_scn(self):
        """Calcula as coordenadas normalizadas para todos os objetos e atualiza a View."""

        # 0. Obtem os parametros da window
        wcx, wcy = self.window.get_center()  # centro da window
        win_width, win_height = (
            self.window.get_width_height()
        )  # largura e altura da window

        # 1. Translada Wc para origem
        translate_to_origin = np.array([[1, 0, 0], [0, 1, 0], [-wcx, -wcy, 1]])
        transformations = translate_to_origin

        # 2. Determina vup e o angulo entre ele e o eixo y
        vup = self.window.vup
        angle_vup_y = np.arctan2(vup[1], vup[0]) - np.pi / 2
        rotation_angle_rad = -angle_vup_y

        # 3. Rotaciona o mundo para alinhar vup com o eixo y
        cos_r = np.cos(rotation_angle_rad)
        sin_r = np.sin(rotation_angle_rad)
        rotate_align_y = np.array([[cos_r, sin_r, 0], [-sin_r, cos_r, 0], [0, 0, 1]])
        transformations = transformations @ rotate_align_y

        # 4. Normaliza as coordenadas, realizando um escalonamento
        scale_x = 2.0 / win_width if win_width != 0 else 1.0
        scale_y = 2.0 / win_height if win_height != 0 else 1.0
        scale_to_scn = np.array([[scale_x, 0, 0], [0, scale_y, 0], [0, 0, 1]])
        transformations = transformations @ scale_to_scn

        # 5. Calcula a SCN e armazena no display file de cada objeto
        for obj in self.display_file:
            normalized_coords = []

            for point_wc in obj.world_points:
                point_scn = point_wc @ transformations  # Transforma o ponto WC para SCN

                nx = point_scn[0]
                ny = point_scn[1]

                normalized_coords.append((nx, ny))

            obj.update_normalized_points(normalized_coords)

    def import_obj_file(self, filepath: str) -> None:
        """Importa um arquivo .obj e adiciona os objetos ao display file."""

        obj_handler = ObjHandler()
        objects_list = obj_handler.read_obj_file(filepath)

        for obj in objects_list:

            if obj[1] in [
                [(x, y) for x, y, *_ in objs.world_points] for objs in self.display_file
            ]:
                self.view.add_log(f"Object {obj[0]} already exists, skipping...")
                continue

            self.add_object(points=obj[1], name=obj[0], color=(0, 0, 0))

        self.view.add_log(f"Objects successfully imported from {filepath}")

    def export_obj_file(self, filepath: str, name: str) -> None:
        """Exporta os objetos do display file para um arquivo .obj."""

        if not name:
            name = "output"

        filepath = os.path.join(filepath, f"{name}.obj")

        obj_handler = ObjHandler()
        obj_str = obj_handler.generate_obj_str(self.display_file)

        with open(filepath, "w") as f:
            f.write(obj_str)

        self.view.add_log(f"Objects successfully exported to {filepath}")

    def get_translation_matrix(self, dx: float, dy: float) -> np.ndarray:
        """Retorna a matriz de translação."""
        
        return np.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])

    def get_scaling_matrix(self, sx: float, sy: float, cx: float, cy: float) -> np.ndarray:
        """Retorna a matriz de escalonamento em torno de (cx, cy)."""
        
        translate_to_origin = self.get_translation_matrix(-cx, -cy)
        scale = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
        translate_back = self.get_translation_matrix(cx, cy)
        return translate_to_origin @ scale @ translate_back

    def get_rotation_matrix(self, angle_degrees: float, cx: float, cy: float) -> np.ndarray:
        """Retorna a matriz de rotação em torno de (cx, cy)."""
        
        angle_radians = np.radians(angle_degrees)
        cos_r = np.cos(angle_radians)
        sin_r = np.sin(angle_radians)
        
        translate_to_origin = self.get_translation_matrix(-cx, -cy)
        rotate = np.array([[cos_r, sin_r, 0], [-sin_r, cos_r, 0], [0, 0, 1]])
        translate_back = self.get_translation_matrix(cx, cy)
        return translate_to_origin @ rotate @ translate_back

    @update_interface
    def rotate_window(self, angle: float) -> None:
        """Rotaciona a janela de visualização para o ângulo especificado em graus."""

        angle_radians = np.radians(angle)

        self.window.apply_rotation(angle_radians)