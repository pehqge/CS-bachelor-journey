import sys

from PyQt6 import QtCore, QtWidgets, uic

from view.creation_dialogs import ObjectDialog
from view.graphical_objects.graphical_object import GraphicalObject
from view.transform_dialogs import TransformationDialog
from view.viewport.viewport import Viewport


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

        self.connect_buttons()
        self.setup_rotation_timers()
        self.setup_viewport()
        self.show()

    def connect_buttons(self) -> None:
        """Conecta os botões da interface com os callbacks correspondentes (on_*)."""

        # Botões de alteração da lista de objetos
        self.createObject.clicked.connect(lambda: self.on_create_object(ObjectDialog()))
        self.removeObject.clicked.connect(self.on_remove_object)
        self.transformObject.clicked.connect(self.on_transform_object)

        # Botões de zoom
        max_zoom = 300
        self.zoomSlider.setMaximum(max_zoom)
        self.zoomInButton.clicked.connect(
            lambda: self.on_zoom(mode="in")
        )  # Quando aperta o botao de zoom in
        self.zoomOutButton.clicked.connect(lambda: self.on_zoom(mode="out"))
        self.zoomSlider.valueChanged.connect(
            lambda: self.on_zoom(mode="slider")
        )  # Quando altera o valor do zoom pela barra

        # Botão de rotação da janela
        self.spinRotationSlider.valueChanged.connect(lambda: self.on_window_rotation())
        # Sticky slider para rotação da janela
        self.spinRotationSlider.sliderPressed.connect(self.start_window_rotation)
        self.spinRotationSlider.sliderReleased.connect(self.stop_window_rotation)

        # Botões de navegação
        self.navUpButton.clicked.connect(lambda: self.on_pan(direction="up"))
        self.navDownButton.clicked.connect(lambda: self.on_pan(direction="down"))
        self.navLeftButton.clicked.connect(lambda: self.on_pan(direction="left"))
        self.navRightButton.clicked.connect(lambda: self.on_pan(direction="right"))
        self.forwardButton.clicked.connect(lambda: self.on_pan(direction="forward"))
        self.backwardButton.clicked.connect(lambda: self.on_pan(direction="backward"))

        # Botões de rotação
        self.verticalRotationSlider.valueChanged.connect(
            lambda: self.on_vertical_rotation()
        )
        self.horizontalRotationSlider.valueChanged.connect(
            lambda: self.on_horizontal_rotation()
        )
        # Sticky sliders para rotação vertical e horizontal
        self.verticalRotationSlider.sliderPressed.connect(self.start_vertical_rotation)
        self.verticalRotationSlider.sliderReleased.connect(self.stop_vertical_rotation)
        self.horizontalRotationSlider.sliderPressed.connect(
            self.start_horizontal_rotation
        )
        self.horizontalRotationSlider.sliderReleased.connect(
            self.stop_horizontal_rotation
        )

        # Botões de importação e exportação de arquivos
        self.importButton.clicked.connect(self.import_obj_file)
        self.exportButton.clicked.connect(self.export_obj_file)

        # Botoes de clipping
        self.cohenSutherlandRadioButton.clicked.connect(
            lambda: self.on_clipping(mode="cohen_sutherland")
        )
        self.liangBarskyRadioButton.clicked.connect(
            lambda: self.on_clipping(mode="liang_barsky")
        )

        # Botões de teste
        self.addTestButton.clicked.connect(self.add_test_objects)
        self.removeTestButton.clicked.connect(self.remove_test_objects)

    def setup_viewport(self) -> None:
        """Configura o viewport para exibir os objetos gráficos."""

        self.viewport = Viewport(self.frame)
        self.viewport.setup_viewport()

    def run(self) -> None:
        """Executa a aplicação PyQt."""

        sys.exit(self.app.exec())

    def update_view_objects(
        self, graphical_objs: list[GraphicalObject], obj_list: list[str]
    ) -> None:
        """
        Atualiza a view com a lista de objetos gráficos.
        @param graphical_objs: Lista de objetos gráficos a serem exibidos após o clipping.
        @param obj_list: Lista de objetos a serem exibidos na lista de objetos lateral.
        """

        self.viewport.update_viewport(graphical_objs)
        self.objectsList.clear()
        self.objectsList.addItems([str(obj) for obj in obj_list])

    def add_log(self, message) -> None:
        """Adiciona uma mensagem ao log da aplicação"""

        logbox = self.logsBox
        logbox.addItem(message)
        logbox.scrollToBottom()  # Faz o log rolar para baixo para mostrar a mensagem mais recente

    def on_create_object(self, dialog: ObjectDialog) -> None:
        """Trata requisições de criação de objetos usando uma caixa de diálogo."""

        points, name, color, is_filled, object_type, edges = dialog.create_object()
        if points is not None:
            self.controller.handle_create_object(
                points, name, color, is_filled, object_type, edges
            )

    def on_remove_object(self) -> None:
        """Trata requisições de remoção de objetos no mundo."""

        selected = [item.row() for item in self.objectsList.selectedIndexes()]
        selected.sort()

        if selected == []:
            self.add_log("You must select an object to remove")
            return

        count = 0
        for index in selected:
            index -= count
            text = self.objectsList.item(index).text()
            self.controller.handle_remove_object(index=index)
            self.add_log(f"{text} has been removed")
            count += 1

    def on_transform_object(self) -> None:
        """Trata requisições de transformação de objetos no mundo."""

        selected = self.objectsList.currentRow()

        if selected == -1:
            self.add_log("You must select an object to transform")
            return

        dialog = TransformationDialog()
        transformations_list = dialog.get_transformations()

        if transformations_list:
            self.controller.handle_transformations(
                index=selected, transformations_list=transformations_list
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

        # Verificar se o atributo zoom_value existe antes de usar
        if not hasattr(self, "zoom_value"):
            self.zoom_value = 50.0  # Valor inicial padrão

        old_zoom_value = self.zoom_value
        new_zoom_value = value

        # Aplica zoom apenas se houver mudança significativa
        if abs(new_zoom_value - old_zoom_value) > 0.01:
            self.controller.handle_zoom(new_zoom_value)

            self.zoomLabel.setText(f"{new_zoom_value}%")
            self.zoom_value = new_zoom_value

    def on_pan(self, direction: str) -> None:
        """Trata as requisições de pan."""

        movement = 100 / self.zoomSlider.value()
        d_horizontal, d_vertical, d_depth = {
            "up": (0, movement, 0),
            "down": (0, -movement, 0),
            "left": (-movement, 0, 0),
            "right": (movement, 0, 0),
            "forward": (0, 0, movement),
            "backward": (0, 0, -movement),
        }[direction]

        self.controller.handle_pan(d_horizontal, d_vertical, d_depth)

    def on_vertical_rotation(self) -> None:
        """Trata as requisições de rotação vertical, chamadas pelo timer."""
        angle_delta = self.verticalRotationSlider.value()
        if angle_delta != 0:  # Só rotaciona se o slider não estiver no centro (0)
            self.controller.handle_window_rotation("vertical", angle_delta)
            # O print foi removido pois seria muito verboso com o timer

    def on_horizontal_rotation(self) -> None:
        """Trata as requisições de rotação horizontal, chamadas pelo timer."""
        angle_delta = self.horizontalRotationSlider.value()
        if angle_delta != 0:
            self.controller.handle_window_rotation("horizontal", angle_delta)

    def import_obj_file(self) -> None:
        """Importa um arquivo .obj."""

        filepath = self.open_import_file_dialog()
        if filepath:
            self.controller.handle_import_obj_file(filepath)

    def export_obj_file(self) -> None:
        """Exporta um arquivo .obj."""

        filepath = self.open_export_file_dialog()
        if filepath:
            self.controller.handle_export_obj_file(filepath)

    def open_import_file_dialog(self) -> str:
        """Abre um diálogo para selecionar um arquivo."""

        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("*.obj")

        if file_dialog.exec():
            return file_dialog.selectedFiles()[0]
        return None

    def open_export_file_dialog(self) -> tuple[str, str]:
        """Abre um diálogo para selecionar uma pasta."""

        if self.objectsList.count() == 0:
            self.add_log("You must create an object to export")
            return None, None

        filepath, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Export Object as OBJ",
            "export.obj",  # Sugere 'export.obj' no diretório que o diálogo abrir
            "OBJ Files (*.obj);;All Files (*)",  # Filtros de arquivo
        )

        if not filepath:
            return None

        if not filepath.lower().endswith(".obj"):
            filepath += ".obj"

        return filepath

    def on_clipping(self, mode: str) -> None:
        """Muda o modo de clipping."""

        self.controller.handle_clipping_change(mode)

    def add_test_objects(self) -> None:
        """Adiciona objetos de teste ao mundo."""

        self.controller.handle_add_test_objects()

    def remove_test_objects(self) -> None:
        """Remove objetos de teste do mundo."""

        self.controller.handle_remove_test_objects()

    def keyPressEvent(self, event) -> None:
        """Trata os eventos de pressionamento de tecla."""

        key = event.key()

        # Movimentação da janela
        if key == QtCore.Qt.Key.Key_Up:
            self.on_pan(direction="up")
        elif key == QtCore.Qt.Key.Key_Down:
            self.on_pan(direction="down")
        elif key == QtCore.Qt.Key.Key_Left:
            self.on_pan(direction="left")
        elif key == QtCore.Qt.Key.Key_Right:
            self.on_pan(direction="right")

        # Zoom (command+ ou command-) ou (ctrl+ ou ctrl-)
        elif key == QtCore.Qt.Key.Key_Equal or key == QtCore.Qt.Key.Key_Plus:
            self.on_zoom(mode="in")
        elif key == QtCore.Qt.Key.Key_Minus:
            self.on_zoom(mode="out")

        # Rotação da janela ([ ou ])
        elif key == QtCore.Qt.Key.Key_BracketLeft:
            self.on_window_rotation(mode="left")
        elif key == QtCore.Qt.Key.Key_BracketRight:
            self.on_window_rotation(mode="right")
        else:
            super().keyPressEvent(event)

    def setup_rotation_timers(self) -> None:
        """Configura timers para rotação contínua enquanto o slider está pressionado."""
        self.rotation_timer_interval = 50  # ms

        # Cria timer para rotação vertical
        self._vertical_timer = QtCore.QTimer(self)
        self._vertical_timer.setInterval(self.rotation_timer_interval)
        self._vertical_timer.timeout.connect(self.on_vertical_rotation)

        # Cria timer para rotação horizontal
        self._horizontal_timer = QtCore.QTimer(self)
        self._horizontal_timer.setInterval(self.rotation_timer_interval)
        self._horizontal_timer.timeout.connect(self.on_horizontal_rotation)

        # Cria timer para rotação da janela (spin)
        self._window_timer = QtCore.QTimer(self)
        self._window_timer.setInterval(self.rotation_timer_interval)
        self._window_timer.timeout.connect(self.on_window_rotation)

    def start_vertical_rotation(self) -> None:
        """Inicia a rotação vertical contínua."""
        self._vertical_timer.start()

    def stop_vertical_rotation(self) -> None:
        """Para a rotação vertical e reseta o slider."""
        self._vertical_timer.stop()
        self.verticalRotationSlider.setValue(0)

    def start_horizontal_rotation(self) -> None:
        """Inicia a rotação horizontal contínua."""
        self._horizontal_timer.start()

    def stop_horizontal_rotation(self) -> None:
        """Para a rotação horizontal e reseta o slider."""
        self._horizontal_timer.stop()
        self.horizontalRotationSlider.setValue(0)

    def start_window_rotation(self) -> None:
        """Inicia a rotação de spin contínua."""
        self._window_timer.start()

    def stop_window_rotation(self) -> None:
        """Para a rotação de spin e reseta o slider."""
        self._window_timer.stop()
        # Chama uma última vez com o valor atual antes de resetar, caso tenha movido rápido
        self.on_window_rotation()
        self.spinRotationSlider.setValue(0)

    def on_window_rotation(self) -> None:
        """Trata as requisições de rotação da janela (spin), chamadas pelo timer."""
        angle_delta = self.spinRotationSlider.value()
        if angle_delta != 0:
            self.controller.handle_window_rotation("spin", angle_delta)

        # Remove a atualização do label, pois o slider volta a 0
        # self.windowRotationLabel.setText(f"{angle_delta}º")
