from PyQt6 import QtCore, QtGui

from view.graphical_objects.graphical_object import GraphicalObject


class GraphicalPolygon(GraphicalObject):
    """Classe que representa um wireframe no viewport."""

    def __init__(
        self,
        viewport_points: list[tuple[float, float, float]],
        color: tuple[int, int, int],
        is_filled: bool,
    ):
        super().__init__(viewport_points, color)
        self.is_filled = is_filled

    def draw(self, painter: QtGui.QPainter) -> None:
        """
        Primeiro usa o QPainterPath para traçar um caminho que conecta todos os
        pontos do polígono, e então desenha o wireframe no viewport.
        """

        path = QtGui.QPainterPath()

        # Move para o primeiro ponto
        path.moveTo(
            QtCore.QPointF(self.viewport_points[0][0], self.viewport_points[0][1])
        )

        # Adiciona linhas para os pontos restantes
        for point in self.viewport_points[1:]:
            path.lineTo(QtCore.QPointF(point[0], point[1]))

        # Retorna ao primeiro ponto para fechar o polígono
        path.lineTo(
            QtCore.QPointF(self.viewport_points[0][0], self.viewport_points[0][1])
        )

        painter.setPen(self.get_pen())

        if self.is_filled:
            color = QtGui.QColor(*self.color)
            color.setAlpha(100)
            painter.setBrush(QtGui.QBrush(color))

        painter.drawPath(path)

        # reseta o brush
        painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 0)))
