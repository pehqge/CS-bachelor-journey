import numpy as np

from model.window import Window
from model.world_object import WorldObject
from view.view import View


class Model:
    """Classe que representa o modelo da nossa arquitetura MVC."""

    def __init__(self, view: View):
        self.view = view
        self.window = Window(viewport_bounds=view.viewport.viewport_bounds)
        self.display_file = []

    @staticmethod
    def update_interface(func: callable) -> callable:
        """
        Decorator que atualiza a interface após a execução de um método.
        """

        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            self = args[0]
            self.view.update_viewport(
                [obj.graphical_representation for obj in self.display_file]
            )
            self.view.update_object_list(self.get_object_list())
            return result

        return wrapper

    def get_object_list(self):
        """Retorna uma representação em string dos objetos do mundo."""
        return [str(obj) for obj in self.display_file]

    @update_interface
    def add_object(self, points: list, name: str, color: tuple[int, int, int]) -> None:
        """Adiciona um objeto gráfico ao display file e atualiza a View."""

        window_bounds = self.window.window_bounds
        viewport_bounds = self.view.viewport.viewport_bounds
        world_object = WorldObject(points, name, color, window_bounds, viewport_bounds)

        self.display_file.append(world_object)

    @update_interface
    def remove_object(self, index: int) -> None:
        """Remove um objeto do display file e atualiza a View."""
        self.display_file.pop(index)

    @update_interface
    def zoom(self, factor: float) -> None:
        """Aplica um zoom na janela de visualização e atualiza a View."""

        self.window.apply_zoom(factor)
        for obj in self.display_file:
            obj.update_representation(
                self.window.window_bounds, self.view.viewport.viewport_bounds
            )

    @update_interface
    def pan(self, dx: float, dy: float) -> None:
        """Aplica um pan na janela de visualização e atualiza a View."""

        self.window.apply_pan(dx, dy)
        for obj in self.display_file:
            obj.update_representation(
                self.window.window_bounds, self.view.viewport.viewport_bounds
            )

    @update_interface
    def translate_object(self, index: int, dx: float, dy: float) -> None:
        """Translada um objeto no display file e atualiza a View."""

        world_object = self.display_file[index]
        translation_matrix = np.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])
        world_object.update_coordinates([translation_matrix])
        world_object.update_representation(
            self.window.window_bounds, self.view.viewport.viewport_bounds
        )

        self.view.add_log(f"{world_object.name} translated by ({dx}, {dy})")

    @update_interface
    def scale_object(self, index: int, x_factor: float, y_factor: float) -> None:
        """Escala um objeto no display file e atualiza a View."""

        world_object = self.display_file[index]
        center_x, center_y = world_object.get_center()

        translation_matrix = np.array([[1, 0, 0], [0, 1, 0], [-center_x, -center_y, 1]])
        scaling_matrix = np.array([[x_factor, 0, 0], [0, y_factor, 0], [0, 0, 1]])
        inverse_translation_matrix = np.array(
            [[1, 0, 0], [0, 1, 0], [center_x, center_y, 1]]
        )

        world_object.update_coordinates(
            [translation_matrix, scaling_matrix, inverse_translation_matrix]
        )
        world_object.update_representation(
            self.window.window_bounds, self.view.viewport.viewport_bounds
        )

        self.view.add_log(f"{world_object.name} scaled by ({x_factor}, {y_factor})")

    @update_interface
    def rotate_object(self, index: int, x: float, y: float, angle: float) -> None:
        """
        Rotaciona um objeto em torno de (x, y) e atualiza a View.
        """

        angle_degrees = angle
        angle_radians = np.radians(angle)

        world_object = self.display_file[index]
        translation_matrix = np.array([[1, 0, 0], [0, 1, 0], [-x, -y, 1]])
        rotation_matrix = np.array(
            [
                [np.cos(angle_radians), np.sin(angle_radians), 0],
                [-np.sin(angle_radians), np.cos(angle_radians), 0],
                [0, 0, 1],
            ]
        )
        inverse_translation_matrix = np.array([[1, 0, 0], [0, 1, 0], [x, y, 1]])

        world_object.update_coordinates(
            [translation_matrix, rotation_matrix, inverse_translation_matrix]
        )
        world_object.update_representation(
            self.window.window_bounds, self.view.viewport.viewport_bounds
        )

        self.view.add_log(f"{world_object.name} rotated about ({x}, {y}) by an angle of {angle_degrees}°")
