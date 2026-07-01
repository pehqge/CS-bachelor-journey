from PyQt6.QtWidgets import QDialog, QVBoxLayout
from .utils.zoomable_graphics_view import ZoomableGraphicsView

class AutomataImageDialog(QDialog):
    """Dialog para imagem do autômato."""
    def __init__(self, img_data: bytes, name: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Máquina de Estados - {name}")
        self.resize(self.screen().availableGeometry().size() * 0.8)
        self.move(self.screen().availableGeometry().center() - self.rect().center())
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.view = ZoomableGraphicsView(self)
        self.view.set_image(img_data)
        layout.addWidget(self.view)
        self.view.fit_view()
