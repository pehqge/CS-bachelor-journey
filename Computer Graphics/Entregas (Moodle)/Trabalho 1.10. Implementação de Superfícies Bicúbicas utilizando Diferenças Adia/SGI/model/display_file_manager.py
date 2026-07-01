import numpy as np

from model.transformation_generator import TransformationGenerator
from model.world_objects.sc_world_object import SCWorldObject
from model.world_objects.world_bezier_curve import WorldBezierCurve
from model.world_objects.world_bezier_surface import WorldBezierSurface
from model.world_objects.world_bicubic_surface import WorldBicubicSurface
from model.world_objects.world_bspline_curve import WorldBSplineCurve
from model.world_objects.world_line import WorldLine
from model.world_objects.world_object import WorldObject
from model.world_objects.world_object_factory import WorldObjectFactory
from model.world_objects.world_point import WorldPoint
from model.world_objects.world_polygon import WorldPolygon
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

        self.projection_algorithms = {
            "parallel": TransformationGenerator.get_parallel_projection_points,
            "perspective": TransformationGenerator.get_perspective_projection_points,
        }

        self.projection_mode = "perspective"

    def get_clipped_representations(self) -> list[GraphicalObject]:
        """
        Retorna as representações gráficas a serem enviadas para o Viewport desenhar.
        @return: Lista de representações gráficas após o clipping.
        """

        representations = []
        for obj in self.display_file:

            if (
                not isinstance(obj, WorldBezierSurface)
                and not isinstance(obj, WorldBicubicSurface)
                and not obj.projection_points
            ):
                continue

            clipped_repr_list = obj.get_clipped_representation()
            if (
                clipped_repr_list
            ):  # Garante que a lista não seja None ou vazia antes de adicionar
                representations.extend(clipped_repr_list)

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
        edges: list = None,
    ) -> WorldObject | None:
        """
        Adiciona um objeto gráfico ao display file.

        @param points: Lista de pontos que representam o objeto.
        @param name: Nome do objeto.
        @param color: Cor do objeto.
        @param is_filled: Se o objeto é preenchido ou não.
        @param object_type: Tipo de objeto.
        @param edges: Lista de arestas que compõem o objeto.
        @return: Retorna o objeto adicionado ou None se o objeto já existir.
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
        return world_object

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
        self,
        index: int,
        transformations_list: list[dict],
        conversion_mtx: np.ndarray,
    ) -> None:
        """
        Aplica uma transformação matricial a um objeto do display file.
        @param index: Índice do objeto a ser transformado.
        @param transformations_list: Lista de dicionários, cada um representando uma transformação.
        @param conversion_mtx: Matriz de conversão para coordenadas reais.
        """

        obj = self.display_file[index]
        obj_center = obj.get_center()

        transformation_mtx = (
            TransformationGenerator.get_composite_transformation_matrix(
                transformations_list=transformations_list,
                obj_center=obj_center,
            )
        )

        if transformation_mtx is None:
            return

        obj.update_perceived_coordinates(transformation_mtx)
        obj.update_world_coordinates(conversion_mtx)
        obj.dirty = True

    def set_all_objects_as_dirty(self) -> None:
        """
        Marca todos os objetos no display file como sujos, indicando que precisam ser atualizados.
        """
        for obj in self.display_file:
            obj.dirty = True

    def update_projections(
        self,
        center_of_projection: np.ndarray,
        window_width: float,
        window_height: float,
    ) -> None:
        """
        Atualiza as projeções dos objetos no display file.
        @param view_plane_normal: Vetor normal ao plano de visualização.
        @param window_vup: Vetor de orientação para cima da janela de visualização.
        @param window_width: Largura da janela de visualização.
        @param window_height: Altura da janela de visualização.
        """

        projection_mtx = self.projection_algorithms[self.projection_mode](
            center_of_projection=center_of_projection,
            window_width=window_width,
            window_height=window_height,
        )

        for obj in self.display_file:
            if not obj.dirty and np.array_equal(obj.projection_points, projection_mtx):
                continue

            obj.dirty = False

            projection_points = []
            obj_out_of_view = False

            if isinstance(obj, WorldBezierSurface) or isinstance(
                obj, WorldBicubicSurface
            ):  # se for uma superficie de Bezier, nao precisa calcular a grade
                obj.update_projection_points(projection_mtx)
                continue

            for point_wc in obj.world_points:
                projected_point = point_wc @ projection_mtx
                normalized_x, normalized_y, _, distance_factor = projected_point

                if distance_factor <= 0:
                    # Se o objeto estiver atrás ou no mesmo plano que o COP, não projete-o
                    obj_out_of_view = True
                    break

                normalized_x /= distance_factor
                normalized_y /= distance_factor

                projection_points.append(
                    (normalized_x, normalized_y)
                )  # Descarta z e w e converte em lista de tuplas

            if obj_out_of_view:
                obj.update_projection_points([])
                continue
            obj.update_projection_points(projection_points)

    def import_file_to_display_file(
        self, filepath: str
    ) -> tuple[list[WorldObject], list[str]]:
        """
        Importa um arquivo .obj e adiciona os objetos ao display file.
        @param filepath: Caminho do arquivo .obj a ser importado.
        @return: Tupla contendo os objetos importados e os nomes dos objetos que foram pulados.
        """

        added_objects, skipped_objects_names = WorldObjectFactory.new_objects_from_file(
            filepath=filepath, display_file=self.display_file
        )

        for world_object in added_objects:
            self.display_file.append(world_object)
            world_object.dirty = True

        return added_objects, skipped_objects_names

    def change_clipping_mode(self, mode: str) -> None:
        """
        Muda o modo de clipping das linhas.
        @param mode: Modo de clipping.
        """
        for obj in self.display_file:
            if isinstance(obj, SCWorldObject):
                obj.change_clipping_mode(mode)

    def add_test_objects(self) -> list[WorldObject]:
        """Adiciona objetos para testarmos o sistema gráfico."""

        test_objects = []

        # Ponto 3D
        test_objects.append(
            self.add_object(
                points=[(0, 0, 10)],
                name="Test Point",
                color=(0, 0, 0),  # black
                is_filled=True,
                object_type=WorldPoint,
            )
        )

        # Curva artística 1 - Bézier (13 pontos para 3n+1)
        curve1 = [
            (-18, -10, 0),
            (-14, -4, 0),
            (-10, 2, 0),
            (-6, 8, 0),
            (-2, 12, 0),
            (4, 16, 0),
            (10, 12, 0),
            (14, 6, 0),
            (18, 2, 0),
            (14, -4, 0),
            (10, -8, -0),
            (4, -12, 0),
            (20, -16, 0),
        ]

        test_objects.append(
            self.add_object(
                points=curve1,
                name="Test Curve I",
                color=(255, 20, 147),  # deep pink
                is_filled=False,
                object_type=WorldBezierCurve,
            )
        )

        # Curva artística 2 - B-Spline
        curve2 = [
            (-15, 20, 0),
            (-20, 15, 0),
            (-15, 45, 0),
            (-5, 0, 0),
            (10, 30, 0),
            (14, -5, 0),
            (0, -8, 0),
            (5, -9, 0),
            (0, -10, 0),
            (5, 20, 0),
        ]

        test_objects.append(
            self.add_object(
                points=curve2,
                name="Test Curve II",
                color=(0, 206, 209),  # dark turquoise
                is_filled=False,
                object_type=WorldBSplineCurve,
            )
        )

        # Cubo de lado 20, atravessado pelo eixo Z e centralizado no plano XY
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

        test_objects.append(
            self.add_object(
                points=cube_points,
                name="Test Cube",
                color=(255, 0, 0),
                is_filled=False,
                object_type=WorldWireframe,
                edges=cube_edges,
            )
        )

        # Adiciona eixo X (vermelho) de tamanho 5
        test_objects.append(
            self.add_object(
                points=[(0, 0, 0), (5, 0, 0)],
                name="Test Axis X",
                color=(255, 0, 0),
                is_filled=False,
                object_type=WorldLine,
            )
        )

        # Adiciona eixo Y (verde) de tamanho 5
        test_objects.append(
            self.add_object(
                points=[(0, 0, 0), (0, 5, 0)],
                name="Test Axis Y",
                color=(0, 255, 0),
                is_filled=False,
                object_type=WorldLine,
            )
        )

        # Adiciona eixo Z (azul) de tamanho 5
        test_objects.append(
            self.add_object(
                points=[(0, 0, 0), (0, 0, 5)],
                name="Test Axis Z",
                color=(0, 0, 255),
                is_filled=False,
                object_type=WorldLine,
            )
        )

        # Triângulo
        triangle_points = [
            (-5, 0, 0),
            (-6, 7, 8),
            (-6.5, 0, 9),
        ]

        test_objects.append(
            self.add_object(
                points=triangle_points,
                name="Test Triangle",
                color=(255, 165, 0),  # orange
                is_filled=True,
                object_type=WorldPolygon,
            )
        )

        # Adiciona uma superfície de Bézier
        bezier_surface_points = [
            [[0.0, 0.0, 0.0], [30.0, 0.0, 50.0], [60.0, 0.0, 50.0], [90.0, 0.0, 0.0]],
            [
                [0.0, 30.0, 40.0],
                [30.0, 30.0, 80.0],
                [60.0, 30.0, 80.0],
                [90.0, 30.0, 40.0],
            ],
            [
                [0.0, 60.0, 40.0],
                [30.0, 60.0, 80.0],
                [60.0, 60.0, 80.0],
                [90.0, 60.0, 40.0],
            ],
            [
                [0.0, 90.0, 0.0],
                [30.0, 90.0, 50.0],
                [60.0, 90.0, 50.0],
                [90.0, 90.0, 0.0],
            ],
        ]

        test_objects.append(
            self.add_object(
                points=bezier_surface_points,
                name="Test Bezier Surface",
                color=(75, 75, 70),
                is_filled=False,
                object_type=WorldBezierSurface,
            )
        )

        # Adiciona uma superfície bicúbica
        bspline_surface_points_4x4 = [
            [[-10, -10, 10], [0, -10, 15], [0, -10, 15], [10, -10, 10]],
            [[-10, 0, 15], [0, 0, 20], [0, 0, 20], [10, 0, 15]],
            [[-10, 0, 15], [0, 0, 20], [0, 0, 20], [10, 0, 15]],
            [[-10, 10, 10], [0, 10, 15], [0, 10, 15], [10, 10, 10]],
        ]
        test_objects.append(
            self.add_object(
                points=bspline_surface_points_4x4,
                name="Test Bicubic B-Spline Surface",
                color=(100, 100, 255),
                is_filled=False,
                object_type=WorldBicubicSurface,
            )
        )

        return test_objects

    def remove_test_objects(self) -> None:
        """Remove objetos de teste do display file."""

        display_file_copy = self.display_file.copy()

        for obj in display_file_copy:
            if obj.name.startswith("Test"):
                self.remove_object(self.display_file.index(obj))

    def change_projection_mode(self, mode: str) -> None:
        """
        Muda o modo de projeção.
        @param mode: Modo de projeção ('parallel' ou 'perspective').
        @raises ValueError: Se o modo de projeção for inválido.
        """

        if mode not in self.projection_algorithms:
            raise ValueError(
                f"Modo de projeção inválido: {mode}. Válidos: {list(self.projection_algorithms.keys())}"
            )

        if self.projection_mode != mode:
            self.projection_mode = mode
            self.set_all_objects_as_dirty()
