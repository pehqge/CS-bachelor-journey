import sys

from PyQt6 import QtWidgets, uic

from view.creation_dialogs import LineDialog, ObjectDialog, PointDialog, WireframeDialog
from view.graphical_objects.graphical_object import GraphicalObject
from view.transform_dialogs import TransformationDialog
from view.viewport import Viewport


class View(QtWidgets.QMainWindow):
    """
    Classe responsavel por gerenciar a interface grafica da aplicação.
    Métodos on_* são disparados pelo usuário ao interagir com a interface.
    """

    def __init__(self, controller):
        self.app = QtWidgets.QApplication(sys.argv)  # Necessário estar no começo

        super().__init__()
        uic.loadUi("view/screens/main.ui", self)
        self.controller = controller

        self.define_values()
        self.connect_buttons()
        self.setup_viewport()
        self.show()

    def define_values(self):
        """Define os valores iniciais dos widgets"""
        self.zoom_value = 50
        self.zoomSlider.setMinimum(1)
        self.zoomSlider.setMaximum(300)
        self.zoomSlider.setValue(self.zoom_value)

    def connect_buttons(self) -> None:
        """Conecta os botões da interface com os callbacks correspondentes (on_*)."""

        # Botões de alteração da lista de objetos
        self.createPoint.clicked.connect(lambda: self.on_create_object(PointDialog()))
        self.createLine.clicked.connect(lambda: self.on_create_object(LineDialog()))
        self.createWireframe.clicked.connect(
            lambda: self.on_create_object(WireframeDialog())
        )
        self.removeObject.clicked.connect(self.on_remove_object)
        self.transformObject.clicked.connect(self.on_transform_object)

        # Botões de zoom
        self.zoomInButton.clicked.connect(
            lambda: self.on_zoom(mode="in")
        )  # Quando aperta o botao de zoom in
        self.zoomOutButton.clicked.connect(lambda: self.on_zoom(mode="out"))
        self.zoomSlider.valueChanged.connect(
            lambda: self.on_zoom(mode="slider")
        )  # Quando altera o valor do zoom pela barra

        # Botões de navegação
        self.navUpButton.clicked.connect(lambda: self.on_pan(direction="up"))
        self.navDownButton.clicked.connect(lambda: self.on_pan(direction="down"))
        self.navLeftButton.clicked.connect(lambda: self.on_pan(direction="left"))
        self.navRightButton.clicked.connect(lambda: self.on_pan(direction="right"))

    def setup_viewport(self) -> None:
        """Configura o viewport para exibir os objetos gráficos."""
        self.viewport = Viewport(self.frame)

        # Adiciona o viewport ao layout do frame
        layout = QtWidgets.QVBoxLayout(self.frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.viewport)
        self.frame.setLayout(layout)

    def run(self) -> None:
        """Executa a aplicação PyQt."""
        sys.exit(self.app.exec())

    def update_viewport(self, objects_list: list[GraphicalObject]) -> None:
        """
        Atualiza o viewport com a lista de objetos gráficos. Chamado pelo model quando
        houver necessidade de atualização da interface.
        """
        self.viewport.update_viewport(objects_list)

    def update_object_list(self, object_list: list) -> None:
        """
        Atualiza a lista de objetos (canto superior esquerdo) exibida na interface.
        Chamado pelo model quando a lista de objetos é alterada.
        """

        self.objectsList.clear()
        self.objectsList.addItems(object_list)

    def add_log(self, message) -> None:
        """Adiciona uma mensagem ao log da aplicação"""

        logbox = self.logsBox  # Pega o objeto que contem o log
        logbox.addItem(message)  # Adiciona a mensagem ao log
        logbox.scrollToBottom()  # Faz o log rolar para baixo para mostrar a mensagem mais recente

    def on_create_object(self, dialog: ObjectDialog) -> None:
        """Trata requisições de criação de objetos usando uma caixa de diálogo."""

        points, name, color = dialog.create_object()
        if name is not None:
            self.controller.handle_create_object(points, name, color)
            self.add_log(f"{dialog.type} {name} created: {points}")

    def on_remove_object(self) -> None:
        """Trata requisições de remoção de objetos no mundo."""

        # pega o index do item selecionado
        selected = self.objectsList.currentRow()

        # se nao tiver selecionado nenhum item
        if selected == -1:
            self.add_log("You must select an object to remove")
            return

        text = self.objectsList.currentItem().text()

        self.controller.handle_remove_object(index=selected)
        self.add_log(f"{text} has been removed")

    def on_transform_object(self) -> None:
        """Trata requisições de transformação de objetos no mundo."""

        selected = self.objectsList.currentRow()

        if selected == -1:
            self.add_log("You must select an object to transform")
            return

        transformation_info = TransformationDialog().get_transformation()
        self.controller.handle_transformation(
            index=selected, transformation_info=transformation_info
        )

    def on_zoom(self, mode: str) -> None:
        """
        Trata as requisições de zoom.
        Slide no meio = 50% de zoom
        Slide no máximo = 100% de zoom (dobro do tamanho original)
        Slide no mínimo = 1% de zoom (1/100 do tamanho original)
        """

        value = 10

        if mode == "in":
            value += self.zoomSlider.value()
        elif mode == "out":
            value = self.zoomSlider.value() - value
        else:
            value = self.zoomSlider.value()

        # Evitar recursão infinita
        if self.zoomSlider.value() != value:
            self.zoomSlider.setValue(value)
            return

        old_zoom_value = self.zoom_value
        new_zoom_value = value

        # Aplica zoom apenas se houver mudança significativa
        if abs(new_zoom_value - old_zoom_value) > 0.01:
            relative_change = new_zoom_value / old_zoom_value
            self.controller.handle_zoom(
                1 / relative_change  # Pois o zoom aumenta com a diminuição da Window
            )

            self.zoom_value = new_zoom_value
            self.add_log(f"Zoom updated: {new_zoom_value:.2f}%")

    def on_pan(self, direction: str) -> None:
        """Trata as requisições de pan."""

        movement = 10
        dx, dy = {
            "up": (0, movement),
            "down": (0, -movement),
            "left": (-movement, 0),
            "right": (movement, 0),
        }[direction]

        self.controller.handle_pan(dx, dy)
        self.add_log(f"Went {direction} by {dx}, {dy}")
