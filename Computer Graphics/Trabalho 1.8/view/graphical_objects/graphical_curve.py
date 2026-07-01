from PyQt6 import QtCore, QtGui

from view.graphical_objects.graphical_object import GraphicalObject


class GraphicalCurve(GraphicalObject):
    """Classe que representa uma curva no viewport."""

    def draw(self, painter: QtGui.QPainter) -> None:
        """
        Desenha a curva como uma sequência de linhas conectando os pontos calculados.
        """

        path = QtGui.QPainterPath()

        path.moveTo(
            QtCore.QPointF(self.viewport_points[0][0], self.viewport_points[0][1])
        )

        for point in self.viewport_points[1:]:
            path.lineTo(QtCore.QPointF(point[0], point[1]))

        painter.setPen(self.get_pen())
        painter.drawPath(path)
