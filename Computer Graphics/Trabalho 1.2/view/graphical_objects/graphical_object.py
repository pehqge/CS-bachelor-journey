from abc import ABC, abstractmethod

from PyQt6 import QtGui


class GraphicalObject(ABC):
    """
    Classe abstrata que representa um objeto gráfico. Cada instância está associada a um
    WorldObject. Mediante qualquer modificação/adição de objetos, o Model passa as representações
    gráficas para a View, que, por sua vez, desenha os objetos na tela (invocando o método
    draw() de cada objeto gráfico).
    """

    def __init__(self, viewport_points: list, color: tuple[int, int, int]):
        """
        @param viewport_points: Lista de pontos do objeto NO VIEWPORT (e não no mundo). Pode
        ser uma lista simples, não havendo necessidade de usarmos np.array. Isso porque
        não faremos cálculos com esses pontos, já que isso é responsabilidade do Model.
        """
        self.viewport_points = viewport_points
        self.color = color

    @abstractmethod
    def draw(self, painter: QtGui.QPainter) -> None:
        """Desenha o objeto gráfico na tela."""

    def get_pen(self) -> QtGui.QPen:
        """Retorna a caneta a ser utilizada para desenhar o objeto."""
        pen = QtGui.QPen(QtGui.QColor(*self.color))
        pen.setWidth(3)
        return pen
