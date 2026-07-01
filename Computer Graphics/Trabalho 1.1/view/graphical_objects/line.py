from PyQt6 import QtCore, QtGui

from view.graphical_objects.graphical_object import GraphicalObject


class Line(GraphicalObject):
    """Classe que representa o segmento de reta no viewport."""

    def draw(self, painter: QtGui.QPainter) -> None:
        """Desenha o segmento de reta no viewport."""
        point_a, point_b = self.viewport_points
        x1, y1 = point_a
        x2, y2 = point_b
        painter.drawLine(QtCore.QPointF(x1, y1), QtCore.QPointF(x2, y2))
