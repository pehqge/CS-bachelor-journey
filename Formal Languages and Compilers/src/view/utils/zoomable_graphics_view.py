from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt, QTimer

class ZoomableGraphicsView(QGraphicsView):
    """Widget com zoom/pan otimizado."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        self.setBackgroundBrush(Qt.GlobalColor.white)
        self._zoom = 1.0

    def set_image(self, data: bytes):
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        if not pixmap.isNull():
            self.setScene(QGraphicsScene())
            self.scene().addItem(QGraphicsPixmapItem(pixmap))
            QTimer.singleShot(0, self.fit_view)

    def fit_view(self):
        if self.scene():
            self.fitInView(self.scene().itemsBoundingRect(), Qt.AspectRatioMode.KeepAspectRatio)
            self._zoom = self.transform().m11()

    def wheelEvent(self, event):
        """Zoom com mouse ou trackpad."""
        if event.angleDelta().y() == 0: return
        factor = 1.0 + (event.pixelDelta().y() * 0.01 if not event.pixelDelta().isNull() else (0.15 if event.angleDelta().y() > 0 else -0.15))
        
        new_zoom = max(0.1, min(self._zoom * factor, 10.0))
        self.scale(new_zoom / self._zoom, new_zoom / self._zoom)
        self._zoom = new_zoom
