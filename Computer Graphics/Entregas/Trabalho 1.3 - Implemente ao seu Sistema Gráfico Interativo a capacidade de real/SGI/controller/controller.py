import numpy as np

from model.model import Model
from view.view import View

class Controller:
    """
    Classe que representa o controller da nossa arquitetura MVC.
    Métodos handle_* são chamados pela View para processar entradas do usuário.
    """

    def __init__(self):
        self.view = View(controller=self)
        self.model = Model(view=self.view)

    def run(self) -> None:
        """Executa a aplicação."""

        self.view.run()

    def handle_create_object(
        self, points_input: list, name_input: str, color_input: tuple
    ) -> None:
        """
        Constrói um novo objeto no mundo.
        @param points_input: Lista de pontos que compõem o objeto.
        @param name_input: Nome do objeto
        """

        self.model.add_object(points=points_input, name=name_input, color=color_input)

    def handle_remove_object(self, index: int) -> None:
        """
        Remove um objeto do mundo.
        @param index: Índice do objeto a ser removido.
        """

        self.model.remove_object(index=index)

    def handle_zoom(self, factor: float) -> None:
        """
        Processa um zoom out/in da janela de visualização.
        @param factor: Fator de zoom.
        """

        self.model.zoom(factor)

    def handle_pan(self, dx: float, dy: float) -> None:
        """
        Processa um deslocamento na janela de visualização.
        @param dx: Deslocamento em x.
        @param dy: Deslocamento em y.
        """

        self.model.pan(dx, dy)

    def handle_transformations(self, index: int, transformations_list: list[dict]) -> None:
        """
        Processa uma lista de transformações aplicadas a um objeto.
        @param index: Índice do objeto a ser transformado.
        @param transformations_list: Lista de transformações a serem aplicadas.
        """

        self.model.handle_transformations(index, transformations_list)

    def handle_window_rotation(self, angle: float) -> None:
        """
        Processa uma rotação da janela de visualização.
        @param angle: Ângulo de rotação.
        """

        self.model.rotate_window(angle)

    def handle_import_obj_file(self, filepath: str) -> None:
        """
        Importa um arquivo .obj.
        @param filepath: Caminho do arquivo .obj.
        """

        self.model.import_obj_file(filepath)

    def handle_export_obj_file(self, filepath: str, name: str) -> None:
        """
        Exporta um arquivo .obj.
        @param filepath: Caminho do arquivo .obj.
        """

        self.model.export_obj_file(filepath, name)
        
    def get_display_file(self) -> list:
        """
        Retorna a lista de objetos do mundo.
        """

        return self.model.display_file
