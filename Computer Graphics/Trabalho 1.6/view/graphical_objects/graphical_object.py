from abc import ABC, abstractmethod

from PyQt6 import QtGui


class GraphicalObject(ABC):
    """
    Classe abstrata que representa um objeto gráfico. Cada instância está associada a um
    WorldObject. Mediante qualquer modificação/adição de objetos, o Model passa as representações
    gráficas para a View, que, por sua vez, desenha os objetos na tela (invocando o método
    draw() de cada objeto gráfico).
    """

    def __init__(
        self,
        viewport_points: list[tuple[float, float, float]],
        color: tuple[int, int, int],
    ):
        """
        @param viewport_points: Lista de pontos do objeto NO VIEWPORT (e não no mundo). Pode
        ser uma lista simples, não havendo necessidade de usarmos np.array. Isso porque
        não faremos cálculos com esses pontos, já que isso é responsabilidade do Model.
        @param color: Cor do objeto gráfico. Deve ser uma tupla com três valores inteiros: (R, G, B)
        """

        self.viewport_points = viewport_points
        self.color = color

    @abstractmethod
    def draw(self, painter: QtGui.QPainter) -> None:
        """
        Desenha o objeto gráfico na tela.
        @param painter: O pintor que desenhará o objeto gráfico.
        """

    def get_pen(self) -> QtGui.QPen:
        """
        Retorna a caneta a ser utilizada para desenhar o objeto.
        @return: Caneta com a cor do objeto.
        """

        pen = QtGui.QPen(QtGui.QColor(*self.color))
        pen.setWidth(3)
        return pen

    def update_points(self, points: list[tuple[float, float]]) -> None:
        """Atualiza os pontos do objeto gráfico."""

        self.viewport_points = points
