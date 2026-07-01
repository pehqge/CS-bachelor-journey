import numpy as np

from model.transformation_generator import TransformationGenerator
from model.world_objects.sc_world_object import SCWorldObject
from model.world_objects.world_bezier_curve import WorldBezierCurve
from model.world_objects.world_bspline_curve import WorldBSplineCurve
from model.world_objects.world_line import WorldLine
from model.world_objects.world_object import WorldObject
from model.world_objects.world_object_factory import WorldObjectFactory
from model.world_objects.world_point import WorldPoint
from model.world_objects.world_wireframe import WorldWireframe
from view.graphical_objects.graphical_object import GraphicalObject
from view.viewport.viewport_bounds import ViewportBounds


class DisplayFileManager:
    """
    Classe responsável por gerenciar o display file
    """

    def __init__(self, viewport_bounds: ViewportBounds):
        self.display_file: list[WorldObject] = []
        WorldObjectFactory.viewport_bounds = viewport_bounds

    def get_clipped_representations(self) -> list[GraphicalObject]:
        """
        Retorna as representações gráficas a serem enviadas para o Viewport desenhar.
        @return: Lista de representações gráficas após o clipping.
        """

        representations = []
        for obj in self.display_file:
            representations += obj.get_clipped_representation()
        return representations

    def get_obj_name(self, index: int) -> str:
        """
        Retorna o nome do objeto gráfico no índice especificado.
        @param index: Índice do objeto no display file.
        @return: Nome do objeto gráfico.
        """
        return self.display_file[index].name

    def add_object(
        self,
        points: list,
        name: str,
        color: tuple,
        is_filled: bool,
        object_type: type,
        edges: list = [],
    ) -> str | None:
        """
        Adiciona um objeto gráfico ao display file.

        @param points: Lista de pontos que representam o objeto.
        @param name: Nome do objeto.
        @param color: Cor do objeto.
        @param is_filled: Se o objeto é preenchido ou não.
        @param object_type: Tipo de objeto.
        @param edges: Lista de arestas que compõem o objeto.
        @return: Retorna uma string com o nome do objeto adicionado ou None se o objeto já existir.
        Por 'já existir' entende-se que já existe um objeto com as mesmas coordenadas.
        """

        world_object = WorldObjectFactory.new_world_object(
            points=points,
            name=name,
            color=color,
            display_file=self.display_file,
            is_filled=is_filled,
            object_type=object_type,
            edges=edges,
        )

        if world_object is None:
            return None

        self.display_file.append(world_object)
        return world_object.name

    def remove_object(self, index: int) -> None:
        """
        Remove um objeto gráfico do display file.
        @param index: Índice do objeto a ser removido.
        """
        self.display_file.pop(index)

    def convert_display_file_to_obj(self) -> str:
        """
        Converte o conteúdo do display file para o formato OBJ.
        @return: String com os objetos do display file no formato OBJ.
        """

        obj_str = ""
        last_index = 1

        for obj in self.display_file:
            new_obj_str, last_index = obj.get_obj_description(last_index)
            obj_str += new_obj_str

        return obj_str

    def get_objs_as_strings(self) -> list[str]:
        """
        Retorna a representação em string dos objetos no display file.
        @return: Lista de strings representando os objetos no display file.
        """
        return [str(obj) for obj in self.display_file]

    def apply_transformation(
        self, index: int, transformations_list: list[dict]
    ) -> None:
        """
        Aplica uma transformação matricial a um objeto do display file.
        @param index: Índice do objeto a ser transformado.
        @param transformations_list: Lista de dicionários, cada um representando uma transformação.
        """

        obj = self.display_file[index]
        obj_center = obj.get_center()
        transformation_mtx = (
            TransformationGenerator.get_composite_transformation_matrix(
                transformations_list=transformations_list, obj_center=obj_center
            )
        )

        if transformation_mtx is None:
            return
        obj.update_coordinates(transformation_mtx)
        obj.dirty = True

    def set_all_objects_as_dirty(self) -> None:
        """
        Marca todos os objetos no display file como sujos, indicando que precisam ser atualizados.
        """
        for obj in self.display_file:
            obj.dirty = True

    def update_projections(
        self,
        window_center: np.ndarray,
        view_plane_normal: np.ndarray,
        window_vup: np.ndarray,
        window_width: float,
        window_height: float,
    ) -> None:
        """
        Atualiza as projeções dos objetos no display file.
        @param window_center: Centro da janela de visualização.
        @param view_plane_normal: Vetor normal ao plano de visualização.
        @param window_vup: Vetor de orientação para cima da janela de visualização.
        @param window_width: Largura da janela de visualização.
        @param window_height: Altura da janela de visualização.
        """

        projection_mtx = TransformationGenerator.get_parallel_projection_matrix(
            window_center=window_center,
            view_plane_normal=view_plane_normal,
            window_vup=window_vup,
            window_width=window_width,
            window_height=window_height,
        )

        for obj in self.display_file:
            if not obj.dirty:  # Evita atualizações desnecessárias
                continue
            obj.dirty = False

            projection_points = []

            for point_wc in obj.world_points:
                projected_point = point_wc @ projection_mtx
                normalized_x, normalized_y, _, _ = projected_point
                projection_points.append(
                    (normalized_x, normalized_y)
                )  # Descarta z e w e converte em lista de tuplas
            obj.update_projection_points(projection_points)

    def import_file_to_display_file(self, filepath: str) -> None:
        """
        Importa um arquivo .obj e adiciona os objetos ao display file.
        @param filepath: Caminho do arquivo .obj a ser importado.
        """

        world_objects, skipped_objects = WorldObjectFactory.new_objects_from_file(
            filepath=filepath, display_file=self.display_file
        )

        for world_object in world_objects:
            self.display_file.append(world_object)
            world_object.dirty = True

        return skipped_objects

    def change_clipping_mode(self, mode: str) -> None:
        """
        Muda o modo de clipping das linhas.
        @param mode: Modo de clipping.
        """

        for obj in self.display_file:
            if isinstance(obj, SCWorldObject):
                obj.change_clipping_mode(mode)

    def add_test_objects(self) -> None:
        """Adiciona objetos de teste ao display file com arte tangram e curvas artísticas."""

        # Linha diagonal decorativa
        self.add_object(
            points=[(-8, 17, -15), (12, 17, 15)],
            name="Test Line",
            color=(70, 100, 255),
            is_filled=False,
            object_type=WorldLine,
        )

        # Curva artística 1 - Bézier (13 pontos para 3n+1)
        curve1 = [
            (-18, -10, 4),
            (-14, -4, -10),
            (-10, 2, 50),
            (-6, 8, 1),
            (-2, 12, 10),
            (4, 16, 30),
            (10, 12, 40),
            (14, 6, 20),
            (18, 2, 10),
            (14, -4, 2),
            (10, -8, -20),
            (4, -12, 3),
            (20, -16, 0),
        ]
        self.add_object(
            points=curve1,
            name="Test Curve I",
            color=(255, 20, 147),  # deep pink
            is_filled=False,
            object_type=WorldBezierCurve,
        )

        # Curva artística 2 - B-Spline
        curve2 = [
            (-15, 20, 10),
            (-20, 15, 1),
            (-15, 45, 4),
            (-5, 0, 20),
            (10, 30, 10),
            (14, -5, 7),
            (0, -8, 5),
            (5, -9, 3),
            (0, -10, 1),
            (5, 20, 0),
        ]

        self.add_object(
            points=curve2,
            name="Test Curve II",
            color=(0, 206, 209),  # dark turquoise
            is_filled=False,
            object_type=WorldBSplineCurve,
        )

        # Pontos decorativos centrais
        decorative_points = [
            ((0, 0, 4), (255, 255, 255)),
            ((10, 10, 10), (128, 0, 128)),
            ((-10, -10, -20), (0, 128, 128)),
        ]
        for coord, col in decorative_points:
            self.add_object(
                points=[coord],
                name=f"Test Point {coord}",
                color=col,
                is_filled=False,
                object_type=WorldPoint,
            )

        # Cubo
        cube_points = [
            (-10, 10, 40),
            (10, 10, 40),
            (10, -10, 40),
            (-10, -10, 40),
            (-10, 10, 60),
            (10, 10, 60),
            (10, -10, 60),
            (-10, -10, 60),
        ]

        cube_edges = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),
        ]
        self.add_object(
            points=cube_points,
            name="Test Cube",
            color=(255, 0, 0),
            is_filled=True,
            object_type=WorldWireframe,
            edges=cube_edges,
        )

        # Adiciona eixo X (vermelho) de tamanho 5
        self.add_object(
            points=[(0, 0, 0), (5, 0, 0)],
            name="Test Axis X",
            color=(255, 0, 0),
            is_filled=False,
            object_type=WorldLine,
        )

        # Adiciona eixo Y (verde) de tamanho 5
        self.add_object(
            points=[(0, 0, 0), (0, 5, 0)],
            name="Test Axis Y",
            color=(0, 255, 0),
            is_filled=False,
            object_type=WorldLine,
        )

        # Adiciona eixo Z (azul) de tamanho 5
        self.add_object(
            points=[(0, 0, 0), (0, 0, 5)],
            name="Test Axis Z",
            color=(0, 0, 255),
            is_filled=False,
            object_type=WorldLine,
        )

    def remove_test_objects(self) -> None:
        """Remove objetos de teste do display file."""

        display_file_copy = self.display_file.copy()

        for obj in display_file_copy:
            if obj.name.startswith("Test"):
                self.remove_object(self.display_file.index(obj))
