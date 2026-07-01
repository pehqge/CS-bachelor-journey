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
        self, points_input: list, name_input: str, color_input: tuple[int, int, int]
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

    def handle_transformation(self, index: int, transformation_info: dict) -> None:
        """
        Processa alguma transformação em um objeto (translação, escalonamento ou rotação).
        @param index: Índice do objeto a ser transformado.
        @param transformation_info: Informações da transformação a ser aplicada.
        """

        if transformation_info is None:
            return

        transformation_option = transformation_info["option"]
        x_value = transformation_info["x_value"]
        y_value = transformation_info["y_value"]
        angle = transformation_info.get("angle", None)

        if transformation_option == "translation":
            self.model.translate_object(index, x_value, y_value)
        elif transformation_option == "scaling":
            self.model.scale_object(index, x_value, y_value)

        elif transformation_option == "rotation":
            if x_value == y_value == "obj_center":
                x_value, y_value = self.model.display_file[index].get_center()
            self.model.rotate_object(index, x_value, y_value, angle)
