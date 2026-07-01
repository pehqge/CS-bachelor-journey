from abc import abstractmethod

from PyQt6 import QtWidgets, uic


class ObjectDialog(QtWidgets.QDialog):
    """Classe responsável por gerenciar um popup genérico"""

    def __init__(self, name: str):
        super().__init__()
        uic.loadUi(f"view/screens/{name}.ui", self)

    def create_object(self, ask_for_name: bool = True):
        """Cria um objeto"""

        self.show()
        result = self.exec()

        # Se o usuário cancelou, retorna None
        if result == QtWidgets.QDialog.DialogCode.Rejected:
            return None, None

        self.points = self.get_points()

        if ask_for_name:
            self.name = NameDialog().name
        else:
            self.name = None

        return self.points, self.name

    def set_field_ranges(self, fields: list):
        """Define o intervalo dos campos de entrada"""

        for field in fields:
            field.setRange(-1000.0, 1000.0)

    @abstractmethod
    def get_points(self):
        """
        Método abstrato para obtermos a lista de pontos do objeto
        É abstrato pois cada objeto requer uma quantidade diferente de pontos
        """


class PointDialog(ObjectDialog):
    """Classe responsavel por gerenciar o popup de criacao de um ponto"""

    def __init__(self):
        super().__init__("newPoint")
        self.type = "Point"
        self.set_field_ranges([self.xInput, self.yInput])

    def get_points(self):
        """Retorna as coordenadas do ponto inseridas pelo usuario"""

        x = float(self.xInput.text().replace(",", "."))
        y = float(self.yInput.text().replace(",", "."))
        return [(x, y)]


class LineDialog(ObjectDialog):
    """Classe responsavel por gerenciar o popup de criacao de uma linha"""

    def __init__(self):
        super(LineDialog, self).__init__("newLine")
        self.type = "Line"
        self.set_field_ranges([self.x1Input, self.y1Input, self.x2Input, self.y2Input])

    def get_points(self):
        """Retorna as coordenadas da linha inseridas pelo usuario"""

        x1 = float(self.x1Input.text().replace(",", "."))
        y1 = float(self.y1Input.text().replace(",", "."))
        x2 = float(self.x2Input.text().replace(",", "."))
        y2 = float(self.y2Input.text().replace(",", "."))
        return [(x1, y1), (x2, y2)]


class WireframeDialog(ObjectDialog):
    """Classe responsável por gerenciar o popup de criação de um poligono"""

    def __init__(self):
        super().__init__("newWireframe")

        self.type = "Wireframe"
        self.points = []
        self.newPointButton.clicked.connect(
            self.add_point
        )  # Conecta o botao de adicionar um ponto

    def add_point(self):
        point, _ = PointDialog().create_object(
            ask_for_name=False
        )  # Abre um popup para inserir as coordenadas do ponto
        
        # Verifica se o ponto já não existe
        if point[0] in self.points:
            self.show_error_message("This point already exists.")
            return
        
        self.points.append(point[0])
        self.pointsList.addItem(
            f"Point: {point[0]}"
        )  # Adiciona o ponto a lista de pontos

    def get_points(self):
        """Retorna a lista de pontos que formam o polígono"""
        return self.points

    def accept(self):
        """Sobrescreve o método accept para validar o número de pontos"""
        if len(self.points) < 3:
            self.show_error_message(
                "It's necessary to have at least 3 points to create a wireframe."
            )
        else:
            super().accept()

    def show_error_message(self, message: str = None):
        """Mostra uma mensagem de erro sobre o número mínimo de pontos"""
        error_dialog = QtWidgets.QMessageBox()
        error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        error_dialog.exec()


class NameDialog(QtWidgets.QDialog):
    """Classe responsável por gerenciar o popup de inserção de nome"""

    def __init__(self):
        super(NameDialog, self).__init__()
        uic.loadUi("view/screens/name.ui", self)
        
        # conectando para ver se o usuario apertou enter
        self.nameInput.textChanged.connect(self._handle_text_changed)
        
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
