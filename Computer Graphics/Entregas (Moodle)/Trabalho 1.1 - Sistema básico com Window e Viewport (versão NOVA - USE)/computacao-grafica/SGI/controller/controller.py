from model.model import Model
from view.view import View


class Controller:
    """Classe que representa o controller da nossa arquitetura MVC."""

    def __init__(self):
        self.view = View(controller=self)
        self.model = Model(view=self.view)

    def run(self) -> None:
        """Executa a aplicação."""
        self.view.run()

    def handle_point_input(self, points_input: list, name_input: str) -> None:
        """Recebe e lida com a entrada do usuário contendo as coordenadas dos pontos."""
        self.model.add_object(points=points_input, name=name_input)

    def handle_remove_object(self, index: int) -> None:
        """Lida com as requisições de remoção de objeto vindas do View."""
        self.model.remove_object(index=index)

    def handle_zoom(self, factor: float) -> None:
        """Lida com as requisições de zoom vindas do View."""
        self.model.zoom(factor)

    def handle_pan(self, dx: float, dy: float) -> None:
        """Lida com as requisições de pan vindas do View."""
        self.model.pan(dx, dy)
