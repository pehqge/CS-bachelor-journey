"""
Módulo com as classes relativas às caixas de diálogo para criação de objetos
"""

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

    def create_object(self):
        """Cria um objeto"""

        self.show()
        result = self.exec()

        # Se o usuário cancelou, retorna None para todos os valores
        if result == QtWidgets.QDialog.DialogCode.Rejected:
            return None, None, None, None

        self.name = self.nameInput.text() if self.nameInput.text().strip() else None
        is_filled = (
            self.fillCheckBox.isChecked() if self.fillCheckBox.isEnabled() else False
        )

        return self.points, self.name, self.color, is_filled

    def add_point(self):
        """Adiciona um novo ponto à lista"""

        x = float(self.xInput.value())
        y = float(self.yInput.value())
        point = (x, y)

        self.points.append(point)
        self.pointsList.addItem(f"Point: {point}")
        self._update_fill_checkbox_visibility()

    def remove_selected_point(self):
        """Remove o ponto selecionado da lista"""

        current_item = self.pointsList.currentItem()
        if current_item:
            index = self.pointsList.row(current_item)
            self.points.pop(index)
            self.pointsList.takeItem(index)
            self._update_fill_checkbox_visibility()
        else:
            self.show_error_message("You must select a point to remove.")

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
                "É necessário ter pelo menos 1 ponto para criar um objeto."
            )
        else:
            super().accept()

    def _update_fill_checkbox_visibility(self):
        """Atualiza a habilitação do checkbox 'Filled' baseado no número de pontos.
        O filled só é habilitado se o número de pontos for maior ou igual a 3 (Wireframe).
        """

        num_points = len(self.points)
        if num_points >= 3:
            self.fillCheckBox.setEnabled(True)
            self.fillCheckBox.setChecked(self.fill_state)  # Restaura o estado salvo

        else:
            self.fill_state = self.fillCheckBox.isChecked()  # Salva o estado atual
            self.fillCheckBox.setChecked(False)
            self.fillCheckBox.setEnabled(False)
