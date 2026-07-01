from model.display_file_manager import DisplayFileManager
from model.window.window import Window
from model.world_objects.world_bezier_curve import WorldBezierCurve
from model.world_objects.world_bspline_curve import WorldBSplineCurve
from model.world_objects.world_line import WorldLine
from model.world_objects.world_point import WorldPoint
from model.world_objects.world_wireframe import WorldWireframe
from view.view import View


class Model:
    """Classe que representa o modelo da nossa arquitetura MVC."""

    def __init__(self, view: View):
        self.view = view
        self.window = Window(viewport_bounds=view.viewport.viewport_bounds)
        self.display_file_manager = DisplayFileManager(
            self.view.viewport.viewport_bounds
        )

    @staticmethod
    def update_interface(func: callable) -> callable:
        """Decorator para atualizar a interface quando uma função é chamada."""

        def wrapper(*args, **kwargs):
            self = args[0]
            result = func(*args, **kwargs)

            # Atualiza as projeções
            self.update_projections()

            # Atualiza a View
            graphical_representations = (
                self.display_file_manager.get_clipped_representations()
            )
            obj_list = self.display_file_manager.get_objs_as_strings()
            self.view.update_view_objects(graphical_representations, obj_list)

            return result

        return wrapper

    @update_interface
    def add_object(
        self,
        points: list,
        name: str,
        color: tuple,
        is_filled: bool,
        object_type: str,
        edges: list,
    ) -> None:
        """
        Adiciona um objeto gráfico ao mundo.
        @param points: Lista de pontos que representam o objeto.
        @param name: Nome do objeto.
        @param color: Cor do objeto.
        @param is_filled: Se o objeto é preenchido ou não.
        @param object_type: Tipo de objeto.
        @param edges: Lista de arestas que compõem o objeto.
        """

        obj_types = {
            "Wireframe": WorldWireframe,
            "Point": WorldPoint,
            "Line": WorldLine,
            "Bézier": WorldBezierCurve,
            "B-Spline": WorldBSplineCurve,
        }

        object_type_cls = obj_types[object_type]

        obj_name = self.display_file_manager.add_object(
            points=points,
            name=name,
            color=color,
            is_filled=is_filled,
            object_type=object_type_cls,
            edges=edges,
        )
        if obj_name is None:
            self.view.add_log("Object already exists, skipping...")
            return

        self.view.add_log(f"{object_type} {obj_name} added: {points}")

    @update_interface
    def remove_object(self, index: int) -> None:
        """
        Remove um objeto do display file e atualiza a View.
        @param index: Índice do objeto a ser removido. Coincide com o índice na lista de objetos da interface.
        """
        self.display_file_manager.remove_object(index)

    @update_interface
    def zoom(self, new_zoom_value: float) -> None:
        """
        Aplica um zoom na janela de visualização e atualiza a View.
        @new_zoom_value: Novo valor de zoom. Valores maiores que 1 aumentam o zoom, valores menores que 1 diminuem.
        """
        self.window.apply_zoom(new_zoom_value)
        self.display_file_manager.set_all_objects_as_dirty()

    @update_interface
    def pan(self, d_horizontal: float, d_vertical: float, d_depth: float) -> None:
        """
        Aplica um pan na janela de visualização.
        @param d_horizontal: Deslocamento horizontal.
        @param d_vertical: Deslocamento vertical.
        @param d_depth: Deslocamento em profundidade ("para fora" ou "para trás").
        """
        self.window.apply_pan(
            d_horizontal=d_horizontal,
            d_vertical=d_vertical,
            d_depth=d_depth,
        )
        self.display_file_manager.set_all_objects_as_dirty()

    @update_interface
    def rotate_window(self, rotation_mode: str, angle: float) -> None:
        """
        Rotaciona a janela de visualização para o ângulo especificado em graus.
        @param rotation_mode: Tipo de rotação (horizontal, vertical ou em torno de si mesma)
        @param angle: Ângulo de rotação em graus.
        """

        self.window.apply_rotation(angle, rotation_mode)
        self.display_file_manager.set_all_objects_as_dirty()

    @update_interface
    def handle_transformations(
        self,
        index: int,
        transformations_list: list[dict],
    ) -> None:
        """
        Aplica uma lista de transformações a um determinado objeto gráfico.
        @param index: Índice do objeto a ser transformado.
        @param transformations_list: Lista de dicionários, cada um representando uma transformação.
        """

        self.display_file_manager.apply_transformation(
            index=index,
            transformations_list=transformations_list,
        )

        for transformation in transformations_list:
            if transformation["type"] == "scaling":
                self.view.add_log(
                    f"Scaling object by factors {transformation['sx']}, {transformation['sy']}, {transformation['sz']}"
                )
            elif transformation["type"] == "translation":
                self.view.add_log(
                    f"Translating object by ({transformation['dx']}, {transformation['dy']}, {transformation['dz']})"
                )
            elif transformation["type"] == "rotation":
                self.view.add_log(
                    f"Rotating object by {transformation['angle']} degrees"
                )

        obj_name = self.display_file_manager.get_obj_name(index)
        self.view.add_log(f"{obj_name}: transformations applied.")

    def update_projections(self) -> None:
        """Método para recalcular as projeções de todos os objetos no display file."""

        self.display_file_manager.update_projections(
            window_center=self.window.window_center,
            view_plane_normal=self.window.view_plane_normal,
            window_vup=self.window.vup,
            window_width=self.window.get_width(),
            window_height=self.window.get_height(),
        )

    @update_interface
    def import_obj_file(self, filepath: str) -> None:
        """
        Importa um arquivo .obj para o display file.
        @param filepath: Caminho do arquivo .obj a ser importado.
        """

        try:
            skipped_objects = self.display_file_manager.import_file_to_display_file(
                filepath=filepath
            )

            self.view.add_log(f"Objects successfully imported from {filepath}")
            if skipped_objects:
                self.view.add_log(f"Skipped objects: {", ".join(skipped_objects)}")

        except FileNotFoundError:
            self.view.add_log(f"File not found: {filepath}")
            return
        except Exception as e:
            self.view.add_log(f"Error importing file: {e}")
            return

    def export_obj_file(self, filepath: str) -> None:
        """
        Exporta os objetos do display file para um arquivo .obj.
        @param filepath: Caminho do diretório onde o arquivo .obj será salvo.
        @param name: Nome do arquivo .obj a ser salvo.
        """

        obj_str = self.display_file_manager.convert_display_file_to_obj()
        if obj_str == "":
            self.view.add_log("No objects to export")
            return

        with open(filepath, "w") as f:
            f.write(obj_str)

        self.view.add_log(f"Objects successfully exported to {filepath}")

    @update_interface
    def change_clipping_mode(self, mode: str) -> None:
        """
        Muda o modo de clipping.
        @param mode: Modo de clipping.
        """
        self.display_file_manager.change_clipping_mode(mode)

    @update_interface
    def add_test_objects(self) -> None:
        """Adiciona objetos de teste ao mundo."""

        self.display_file_manager.add_test_objects()

        # Aplica uma rotação no primeiro objeto
        # self.handle_transformations(0, [{"type": "rotation", "angle": 180, "x1": 10, "y1": -10, "z1": 40, "x2": -10, "y2": 10, "z2": 60, "axis": "arbitrary"}])

    @update_interface
    def remove_test_objects(self) -> None:
        """Remove objetos de teste do mundo."""
        self.display_file_manager.remove_test_objects()
