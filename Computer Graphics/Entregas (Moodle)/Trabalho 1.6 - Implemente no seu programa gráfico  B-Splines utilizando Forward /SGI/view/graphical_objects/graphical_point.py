from PyQt6 import QtCore, QtGui
from view.graphical_objects.graphical_object import GraphicalObject


class GraphicalPoint(GraphicalObject):
    """Classe que representa um ponto no viewport."""

    def draw(self, painter: QtGui.QPainter) -> None:
        """Desenha o ponto no viewport."""
        x, y = self.viewport_points[0]
        painter.setPen(self.get_pen())
        painter.drawPoint(QtCore.QPointF(x, y))
