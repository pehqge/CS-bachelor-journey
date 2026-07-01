"""
Módulo com as classes relativas às caixas de diálogo para criação de objetos
"""

import re

from PyQt6 import QtWidgets, uic


class ObjectDialog(QtWidgets.QDialog):
    """Classe responsável por gerenciar o popup de criação de objeto"""

    def __init__(self):
        super().__init__()
        uic.loadUi("view/screens/newObject.ui", self)

        self.points: list = []
        self.color: tuple = (0, 0, 0)  # Cor padrão preto
        self.name: str | None = None
        self.fill_state: bool = False  # Estado inicial do preenchimento

        self.newPointButton.clicked.connect(self.add_point)
        self.removeButton.clicked.connect(self.remove_selected_point)
        self.colorButton.clicked.connect(self.choose_color)
        self.bulkPointsButton.clicked.connect(self.handle_add_bulk_points)
        self.fillCheckBox.stateChanged.connect(self._handle_fill_checkbox)

        # Criando o grupo de botões de tipo de objeto
        self.objectType = QtWidgets.QButtonGroup()
        self.objectType.addButton(self.pointRadio)
        self.objectType.addButton(self.lineRadio)
        self.objectType.addButton(self.wireframeRadio)
        self.objectType.addButton(self.curveRadio)
        self.objectType.addButton(self.bSplineRadio)

        self.objectType.buttonClicked.connect(self._update_fill_checkbox_visibility)

    def create_object(self):
        """Cria um objeto"""

        self.show()
        result = self.exec()

        # Se o usuário cancelou, retorna None para todos os valores
        if result == QtWidgets.QDialog.DialogCode.Rejected:
            return None, None, None, None, None

        self.name = self.nameInput.text() if self.nameInput.text().strip() else None

        is_filled = (
            self.fillCheckBox.isChecked() if self.fillCheckBox.isEnabled() else False
        )

        object_type = self.objectType.checkedButton().text()

        return self.points, self.name, self.color, is_filled, object_type

    def add_point(self):
        """Adiciona um novo ponto à lista"""

        x = float(self.xInput.value())
        y = float(self.yInput.value())
        point = (x, y)

        self.points.append(point)
        self.pointsList.addItem(f"Point: {point}")
        self._update_interface()

    def remove_selected_point(self):
        """Remove o ponto selecionado da lista"""

        current_item = self.pointsList.currentItem()
        if current_item:
            index = self.pointsList.row(current_item)
            self.points.pop(index)
            self.pointsList.takeItem(index)
            self._update_interface()
        else:
            self.show_error_message("You must select a point to remove.")

    def handle_add_bulk_points(self):
        """Adiciona um conjunto de pontos à lista por meio de um input de texto"""

        try:
            # tratamento do texto inserido
            text = self.bulkPointsInput.text()
            text = re.sub(r"[^0-9.,() \-]", "", text)
            points = text.replace(",", " ").split()

            new_points = []
            coordinates = []

            for point in points:

                if point[0] == "(":  # começo de uma coordenada
                    coordinates.append(float(point[1:]))
                elif point[-1] == ")":  # fim de uma coordenada
                    coordinates.append(float(point[:-1]))
                    new_points.append(coordinates)
                    coordinates = []
                elif (
                    coordinates
                ):  # adiciona um numero a coordenada apenas se houver uma coordenada iniciada
                    coordinates.append(float(point))

        except ValueError:
            self.show_error_message("Invalid input. Please enter valid coordinates.")
            return

        # Conferindo se há mais de 2 coordenadas
        for point in new_points:
            if len(point) > 2:
                self.show_error_message(
                    "Points with more than 2 coordinates are not supported yet."
                )
                return

        for point in new_points:
            self.points.append(tuple(point))
            self.pointsList.addItem(f"Point: {point}")
            self._update_interface()

    def choose_color(self):
        """Abre o diálogo de escolha de cor"""

        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.color = (color.red(), color.green(), color.blue())
            self.colorPreview.setStyleSheet(
                f"border: 2px solid white; border-radius: 16px; background-color: rgb{self.color};"
            )

        self.raise_()

    def show_error_message(self, message: str):
        """Mostra uma mensagem de erro"""

        error_dialog = QtWidgets.QMessageBox()
        error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("Erro")
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        error_dialog.exec()

    def accept(self):
        """Sobrescreve o método accept para validar o número de pontos"""

        if len(self.points) < 1:
            self.show_error_message(
                "There must be at least 1 point to create an object."
            )
        elif self.curveRadio.isChecked() and (len(self.points) - 1) % 3 != 0:
            self.show_error_message(
                """The number of points must be 4 plus a multiple of 3 for a curve.
                Example: 4, 7, 10, 13, etc.
                """
            )
        else:
            super().accept()

    def _update_fill_checkbox_visibility(self):
        """Atualiza a habilitação do checkbox 'Filled' baseado no número de pontos.
        O filled só é habilitado se o número de pontos for maior ou igual a 3 (Wireframe).
        """

        num_points = len(self.points)
        if num_points >= 3 and self.wireframeRadio.isChecked():
            self.fillCheckBox.setEnabled(True)
            self.fillCheckBox.setChecked(self.fill_state)

        else:
            self.fillCheckBox.setChecked(False)
            self.fillCheckBox.setEnabled(False)

    def _handle_fill_checkbox(self):
        """Gerencia o estado do checkbox 'Filled'"""

        if self.wireframeRadio.isChecked():
            if self.fillCheckBox.isChecked():
                self.fill_state = True
            else:
                self.fill_state = False

    def _update_object_type(self):
        """Atualiza o tipo de objeto baseado no número de pontos"""

        num_points = len(self.points)
        radio_buttons = [
            self.pointRadio,
            self.lineRadio,
            self.wireframeRadio,
            self.curveRadio,
            self.bSplineRadio,
        ]

        if num_points == 0:  # desabilita todos os botões
            for button in radio_buttons:
                button.setChecked(False)
                button.setEnabled(False)

        if num_points == 1:  # habilita apenas ponto
            for button in radio_buttons:
                button.setEnabled(False)

            self.pointRadio.setEnabled(True)
            self.pointRadio.setChecked(True)

        if num_points == 2:  # habilita linha
            for button in radio_buttons:
                button.setEnabled(False)

            self.lineRadio.setEnabled(True)
            self.lineRadio.setChecked(True)

        if num_points == 3:  # habilita wireframe
            for button in radio_buttons:
                button.setEnabled(False)

            self.wireframeRadio.setEnabled(True)
            self.wireframeRadio.setChecked(True)

        if num_points > 3:  # habilita curva e wireframe
            for button in radio_buttons:
                button.setEnabled(False)

            self.curveRadio.setEnabled(True)
            self.bSplineRadio.setEnabled(True)
            self.wireframeRadio.setEnabled(True)

    def _update_points_number(self):
        """Atualiza o número de pontos"""

        num_points = len(self.points)
        self.numPoints.setText(
            f'<html><head/><body><p><span style=" font-weight:700;">Number of points:</span> {num_points}</p></body></html>'
        )

    def _update_interface(self):
        """Atualiza a interface baseado no tipo de objeto selecionado"""

        self._update_object_type()
        self._update_points_number()
        self._update_fill_checkbox_visibility()
