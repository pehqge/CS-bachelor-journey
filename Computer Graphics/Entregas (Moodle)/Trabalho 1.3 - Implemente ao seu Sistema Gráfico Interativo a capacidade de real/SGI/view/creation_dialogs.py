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

        self.newPointButton.clicked.connect(self.add_point)
        self.removeButton.clicked.connect(self.remove_selected_point)
        self.colorButton.clicked.connect(self.choose_color)

    def create_object(self):
        """Cria um objeto"""

        self.show()
        result = self.exec()

        # Se o usuário cancelou, retorna None
        if result == QtWidgets.QDialog.DialogCode.Rejected:
            return None, None, None

        self.name = self.nameInput.text() if self.nameInput.text().strip() else None

        return self.points, self.name, self.color

    def add_point(self):
        """Adiciona um novo ponto à lista"""
        
        x = float(self.xInput.value())
        y = float(self.yInput.value())
        point = (x, y)

        # Verifica se o ponto já existe
        if point in self.points:
            self.show_error_message("This point already exists.")
            return

        self.points.append(point)
        self.pointsList.addItem(f"Point: {point}")

    def remove_selected_point(self):
        """Remove o ponto selecionado da lista"""
        
        current_item = self.pointsList.currentItem()
        if current_item:
            index = self.pointsList.row(current_item)
            self.points.pop(index)
            self.pointsList.takeItem(index)
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
            self.show_error_message("É necessário ter pelo menos 1 ponto para criar um objeto.")
        else:
            super().accept()


class NameDialog(QtWidgets.QDialog):
    """Classe responsável por gerenciar o popup de inserção de nome"""

    def __init__(self, text: str = None):
        super().__init__()
        uic.loadUi("view/screens/name.ui", self)

        # conectando para ver se o usuario apertou enter
        self.nameInput.textChanged.connect(self._handle_text_changed)

        if text:
            self.title.setText(text)

        self.show()
        self.exec()

    def _handle_text_changed(self):
        """Verifica se o usuário clicou em enter"""
        if "\n" in self.nameInput.toPlainText():
            # remove o enter
            text = self.nameInput.toPlainText().replace("\n", "")
            self.nameInput.setPlainText(text)
            self.accept()

    def accept(self):
        """Retorna o nome inserido pelo usuário"""
        self.name = self.nameInput.toPlainText()
        super().accept()

    def reject(self):
        """Se cancela a inserção do nome, retorna None (não cria o objeto)"""
        self.name = None
        super().reject()
