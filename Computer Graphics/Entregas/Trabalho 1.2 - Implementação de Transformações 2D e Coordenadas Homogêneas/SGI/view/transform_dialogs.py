"""
Módulo que contém classes relativas às caixas de diálogo para transformação de objetos
"""

from PyQt6 import QtWidgets, uic


class TransformationDialog(QtWidgets.QDialog):
    """
    Classe que representa uma caixa de diálogo para transformação de objeto. Opções:
    1 - Translação
    2 - Escalonamento em torno do centro do objeto
    3 - Rotação (em torno do centro do mundo, do centro do objeto, ou de um ponto arbitrário)
    """

    def __init__(self):
        super().__init__()
        uic.loadUi("view/screens/transformObject.ui", self)

        self.translationBtn.clicked.connect(
            lambda: self.select_option_dialog(TranslationOptionDialog)
        )
        self.scalingBtn.clicked.connect(
            lambda: self.select_option_dialog(ScalingOptionDialog)
        )
        self.rotationBtn.clicked.connect(
            lambda: self.select_option_dialog(RotationOptionDialog)
        )

        self.option_dialog: QtWidgets.QDialog = None

    def get_transformation(self) -> dict:
        """
        Retorna informações sobre a transformação selecionada pelo usuário em um dicionário

        Exemplo de retorno:
        {
            "option": "translation",  # Opção selecionada
            "x_value": 10.0,  # Valor no eixo x (nesse caso, fator de escala). Interpretação depende de option
            "y_value": 20.0   # Mesma coisa do x_value
        }
        """

        self.show()
        result = self.exec()

        if result == QtWidgets.QDialog.DialogCode.Rejected:
            return None

        return self.option_dialog.get_option_input()

    def select_option_dialog(self, option_dialog: type) -> None:
        """Seta a caixa de diálogo a ser utilizada para a opção selecionada"""
        self.option_dialog = option_dialog()
        self.accept()


class OptionDialog(QtWidgets.QDialog):
    """
    Classe que representa uma caixa de diálogo genérica para seleção de opções.
    Deve ser herdada por classes específicas para cada opção de transformação.
    """

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        uic.loadUi(f"view/screens/{name}Option.ui", self)

    def get_option_input(self) -> dict:
        """Exibe a caixa de diálogo e retorna a entrada inserida pelo usuário"""

        self.show()
        result = self.exec()

        if result == QtWidgets.QDialog.DialogCode.Rejected:
            return None

        transformation_info = {}
        return self.read_input(transformation_info)

    def read_input(self, transformation_info: dict) -> dict:
        """
        Método para leitura da entrada na tela de seleção de opção
        Precisa ser reimplementado nas classes filhas, as quais chamarão super().read_input()
        """
        transformation_info["option"] = self.name


class TranslationOptionDialog(OptionDialog):
    """Classe que representa uma caixa de diálogo para a translação"""

    def __init__(self):
        super().__init__(name="translation")
        self.xInput.setRange(-1000.0, 1000.0)
        self.yInput.setRange(-1000.0, 1000.0)

    def read_input(self, transformation_info: dict) -> dict:
        """Retorna o vetor de translação inserido pelo usuário"""

        super().read_input(transformation_info)
        transformation_info["x_value"] = float(self.xInput.text().replace(",", "."))
        transformation_info["y_value"] = float(self.yInput.text().replace(",", "."))
        return transformation_info


class ScalingOptionDialog(OptionDialog):
    """Classe que representa uma caixa de diálogo para o escalonamento"""

    def __init__(self):
        super().__init__(name="scaling")
        self.xInput.setRange(0.01, 100.0)
        self.xInput.setValue(1.0)
        self.yInput.setRange(0.01, 100.0)
        self.yInput.setValue(1.0)

    def read_input(self, transformation_info: dict) -> dict:
        """Retorna o fator de escala inserido pelo usuário"""
        super().read_input(transformation_info)
        transformation_info["x_value"] = float(self.xInput.text().replace(",", "."))
        transformation_info["y_value"] = float(self.yInput.text().replace(",", "."))
        return transformation_info


class RotationOptionDialog(OptionDialog):
    """Classe que representa uma caixa de diálogo para selecionar a rotação"""

    def __init__(self):
        super().__init__(name="rotation")
        self.originBtn.clicked.connect(
            lambda: self.set_button_handler(self.select_origin)
        )
        self.objCenterBtn.clicked.connect(
            lambda: self.set_button_handler(self.select_obj_center)
        )
        self.arbitraryBtn.clicked.connect(
            lambda: self.set_button_handler(self.select_arbitrary)
        )

        self.xInput.setRange(-1000.0, 1000.0)
        self.yInput.setRange(-1000.0, 1000.0)
        self.angleInput.setRange(-360.0, 360.0)

        self.chosen_point: tuple[float | str, float | str] = None
        self.button_handler: callable = None

    def read_input(self, transformation_info: dict) -> dict:
        """
        Retorna a rotação inserida pelo usuário.
        O diferencial aqui é a inserção de uma nova chave para o ângulo.
        """

        super().read_input(transformation_info)
        x_value, y_value = self.chosen_point
        transformation_info["x_value"] = x_value
        transformation_info["y_value"] = y_value
        transformation_info["angle"] = float(self.angleInput.text().replace(",", "."))

        return transformation_info

    def accept(self) -> None:
        """Só permite aceitar a caixa de diálogo se um ponto de rotação foi escolhido"""
        if self.button_handler is None:
            QtWidgets.QApplication.beep()
        else:
            self.button_handler()  # Armazena o ponto de rotação e o ângulo
            super().accept()

    def set_button_handler(self, button_handler: callable) -> None:
        """Armazena o método correspondente ao botão escolhido pelo usuário"""
        self.button_handler = button_handler

    def select_origin(self):
        """Seleciona a origem como ponto de rotação"""
        self.chosen_point = (0, 0)

    def select_obj_center(self):
        """Seleciona o centro do objeto como ponto de rotação"""
        self.chosen_point = ("obj_center", "obj_center")

    def select_arbitrary(self):
        """Seleciona um ponto arbitrário como ponto de rotação"""
        chosen_x = float(self.xInput.text().replace(",", "."))
        chosen_y = float(self.yInput.text().replace(",", "."))
        self.chosen_point = (chosen_x, chosen_y)
