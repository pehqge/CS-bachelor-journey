from PyQt6 import QtGui, QtWidgets
from utils.bounds import Bounds
from view.graphical_objects.graphical_object import GraphicalObject


class Viewport(QtWidgets.QWidget):
    """Classe responsável por gerenciar o viewport."""

    def __init__(self, parent):
        super().__init__(parent)

        # Define a cor de fundo do viewport
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(230, 230, 230))
        self.setPalette(palette)

        self.viewport_offset = 10
        self.viewport_bounds: Bounds = (
            None  # Será definido automaticamente no evento resizeEvent
        )
        self.graphical_objects = []

    def setup_viewport(self):
        """Configura o viewport."""

        layout = QtWidgets.QVBoxLayout(self.parent())
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self)
        self.parent().setLayout(layout)

    def resizeEvent(self, event) -> None:
        """
        Sobrescreve o método resizeEvent para atualizar os limites do viewport.
        Deixamos uma margem para visualizar o clipping acontecendo.
        """

        super().resizeEvent(event)

        self.viewport_bounds = Bounds(
            x_min=self.viewport_offset,
            x_max=self.width() - self.viewport_offset,
            y_min=self.viewport_offset,
            y_max=self.height() - self.viewport_offset,
        )

    def paintEvent(self, event) -> None:
        """Sobrescreve o método paintEvent para desenhar os objetos no viewport."""

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        # Desenha cada objeto
        for obj in self.graphical_objects:
            obj.draw(painter)

        def _draw_viewport_frame(
            painter: QtGui.QPainter, color: QtGui.QColor, width: int, offset: int
        ) -> None:
            """Desenha a borda do viewport com as configurações especificadas."""
            frame_pen = QtGui.QPen(color)
            frame_pen.setWidth(width)
            painter.setPen(frame_pen)

            painter.drawRect(
                self.viewport_bounds.x_min - offset,
                self.viewport_bounds.y_min - offset,
                self.viewport_bounds.x_max - self.viewport_bounds.x_min + 2 * offset,
                self.viewport_bounds.y_max - self.viewport_bounds.y_min + 2 * offset,
            )

        # Desenha a borda externa (branca)
        _draw_viewport_frame(
            painter=painter, color=QtGui.QColor(230, 230, 230), width=3, offset=1
        )

        # Desenha a borda interna (preta)
        _draw_viewport_frame(
            painter=painter, color=QtGui.QColor(0, 0, 0), width=1, offset=-1
        )

    def update_viewport(self, objects: list[GraphicalObject]) -> None:
        """Atualiza o viewport."""
        self.graphical_objects = objects
        self.update()  # Redesenha o viewport
