from model.display_file_manager import DisplayFileManager
from model.window import Window
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

            # Recalcula as coordenadas normalizadas para todos os objetos
            self._calculate_and_update_ncs()

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
        self, points: list, name: str, color: tuple, is_filled: bool
    ) -> None:
        """
        Adiciona um objeto gráfico ao mundo.
        @param points: Lista de pontos que representam o objeto.
        @param name: Nome do objeto.
        @param color: Cor do objeto.
        @param is_filled: Se o objeto é preenchido ou não.
        """

        obj_name = self.display_file_manager.add_object(
            points=points, name=name, color=color, is_filled=is_filled
        )
        if obj_name is None:
            self.view.add_log("Object already exists, skipping...")
            return

        self.view.add_log(f"Object {obj_name} added: {points}")

    @update_interface
    def remove_object(self, index: int) -> None:
        """
        Remove um objeto do display file e atualiza a View.
        @param index: Índice do objeto a ser removido. Coincide com o índice na lista de objetos da interface.
        """

        self.display_file_manager.remove_object(index)

    @update_interface
    def zoom(self, factor: float) -> None:
        """
        Aplica um zoom na janela de visualização e atualiza a View.
        @factor: Fator de zoom. Valores maiores que 1 aumentam o zoom, valores menores que 1 diminuem.
        """
        self.window.apply_zoom(factor)

    @update_interface
    def pan(self, dx: float, dy: float) -> None:
        """
        Aplica um pan na janela de visualização.
        @param dx: Deslocamento em x.
        @param dy: Deslocamento em y.
        """
        self.window.apply_pan(dx, dy)

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
                    f"Scaling object by factors {transformation['sx']}, {transformation['sy']}"
                )
            elif transformation["type"] == "translation":
                self.view.add_log(
                    f"Translating object by ({transformation['dx']}, {transformation['dy']})"
                )
            elif transformation["type"] == "rotation":
                self.view.add_log(
                    f"Rotating object by {transformation['angle']} degrees"
                )

        obj_name = self.display_file_manager.get_obj_name(index)
        self.view.add_log(f"{obj_name}: Transformations applied.")

    def _calculate_and_update_ncs(self) -> None:
        """Calcula as coordenadas normalizadas para todos os objetos."""

        window_cx, window_cy = self.window.get_center()
        window_width, window_height = self.window.get_width_height()
        window_vup = self.window.vup

        self.display_file_manager.update_ncs_coordinates(
            window_cx=window_cx,
            window_cy=window_cy,
            window_width=window_width,
            window_height=window_height,
            window_vup=window_vup,
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

        with open(filepath, "w") as f:
            f.write(obj_str)

        self.view.add_log(f"Objects successfully exported to {filepath}")

    @update_interface
    def rotate_window(self, angle: float) -> None:
        """
        Rotaciona a janela de visualização para o ângulo especificado em graus.
        @param angle: Ângulo de rotação em graus.
        """

        self.window.apply_rotation(angle)

    @update_interface
    def change_clipping_mode(self, mode: str) -> None:
        """
        Muda o modo de clipping.
        @param mode: Modo de clipping.
        """

        self.display_file_manager.change_clipping_mode(mode)
