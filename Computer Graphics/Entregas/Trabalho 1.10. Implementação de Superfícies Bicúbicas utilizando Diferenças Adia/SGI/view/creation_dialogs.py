"""
Módulo com as classes relativas às caixas de diálogo para criação de objetos
"""

import re

from PyQt6 import QtWidgets, uic


class GenericDialog(QtWidgets.QDialog):
    """Classe genérica para diálogos"""

    def __init__(self, file_path: str):
        super().__init__()
        uic.loadUi(file_path, self)

    def show_error_message(self, message: str):
        """Mostra uma mensagem de erro"""

        error_dialog = QtWidgets.QMessageBox()
        error_dialog.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        error_dialog.exec()

    def choose_color(self):
        """Abre o diálogo de escolha de cor"""

        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.color = (color.red(), color.green(), color.blue())
            self.colorPreview.setStyleSheet(
                f"border: 2px solid white; border-radius: 16px; background-color: rgb{self.color};"
            )

        self.raise_()


class ObjectDialog(GenericDialog):
    """Classe responsável por gerenciar o popup de criação de objeto"""

    def __init__(self):
        super().__init__("view/screens/newObject.ui")

        self.points: list = []
        self.color: tuple = (0, 0, 0)  # Cor padrão preto
        self.name: str | None = None
        self.fill_state: bool = False  # Estado inicial do preenchimento
        self.is_surface: bool = False
        self.surface_type: str | None = None

        self.newPointButton.clicked.connect(self.add_point)
        self.removeButton.clicked.connect(self.remove_selected_point)
        self.colorButton.clicked.connect(self.choose_color)
        self.batchPointsButton.clicked.connect(self.handle_add_points_in_batch)
        self.fillCheckBox.stateChanged.connect(self._handle_fill_checkbox)

        # Criando o grupo de botões de tipo de objeto
        self.objectType = QtWidgets.QButtonGroup()
        self.objectType.addButton(self.pointRadio)
        self.objectType.addButton(self.lineRadio)
        self.objectType.addButton(self.wireframeRadio)
        self.objectType.addButton(self.curveRadio)
        self.objectType.addButton(self.bSplineRadio)
        self.objectType.addButton(self.polygonRadio)

        self.createBezierSurfaceButton.clicked.connect(self.open_bezier_surface_dialog)
        self.createBicubicSurfaceButton.clicked.connect(
            self.open_bicubic_surface_dialog
        )

        self.objectType.buttonClicked.connect(self._update_fill_checkbox_visibility)

    def open_bezier_surface_dialog(self):
        """Abre o diálogo de criação de superfície de Bézier."""

        bezier_surface_dialog = BezierSurfaceDialog()
        dialog_result = bezier_surface_dialog.exec()
        if dialog_result == QtWidgets.QDialog.DialogCode.Accepted:
            self.points = bezier_surface_dialog.surface_points
            self.name = bezier_surface_dialog.name
            self.color = bezier_surface_dialog.color
            self.is_surface = True
            self.surface_type = "Bezier Surface"

            self.result = QtWidgets.QDialog.DialogCode.Accepted
            self.accept()

    def open_bicubic_surface_dialog(self):
        """Abre o diálogo de criação de superfície bicúbica."""

        bicubic_surface_dialog = BicubicSurfaceDialog()
        dialog_result = bicubic_surface_dialog.exec()
        if dialog_result == QtWidgets.QDialog.DialogCode.Accepted:
            self.points = bicubic_surface_dialog.surface_points
            self.name = bicubic_surface_dialog.name
            self.color = bicubic_surface_dialog.color
            self.is_surface = True
            self.surface_type = "Bicubic Surface"

            self.result = QtWidgets.QDialog.DialogCode.Accepted
            self.accept()

    def create_object(self):
        """Cria um objeto, solicitando arestas se for um Wireframe."""
        self.show()
        self.result = self.exec()

        # Se o diálogo principal foi rejeitado
        if self.result == QtWidgets.QDialog.DialogCode.Rejected:
            return None, None, None, None, None, None  # Adiciona None para edges

        if self.is_surface:
            return self.points, self.name, self.color, None, self.surface_type, None

        # Obter dados básicos independentemente do tipo
        self.name = self.nameInput.text() if self.nameInput.text().strip() else None
        is_filled = (
            self.fillCheckBox.isChecked() if self.fillCheckBox.isEnabled() else False
        )
        object_type = self.objectType.checkedButton().text()
        edges = None  # Inicializa edges

        # Se for Wireframe, solicitar arestas
        if object_type == "Wireframe":
            # Validação de pontos mínimos para wireframe já deve ter ocorrido no accept
            edge_dialog = EdgeDialog(self.points)
            edge_result = edge_dialog.exec()

            # Se o diálogo de arestas foi confirmado
            if edge_result == QtWidgets.QDialog.DialogCode.Accepted:
                edges = edge_dialog.edges
            else:  # Se o diálogo de arestas foi cancelado, anula toda a criação
                return None, None, None, None, None, None

        # Ignora o eixo z para curvas, deixando-o como 0
        elif object_type == "B-Spline" or object_type == "Bézier":
            for i, point in enumerate(self.points):
                self.points[i] = (point[0], point[1], 0)

            self.show_error_message(
                "Because you selected a Curve, the points will have Z = 0."
            )

        # Retorna os dados (edges será None se não for Wireframe ou se cancelado)
        return self.points, self.name, self.color, is_filled, object_type, edges

    def add_point(self):
        """Adiciona um novo ponto à lista"""

        x = float(self.xInput.value())
        y = float(self.yInput.value())
        z = float(self.zInput.value())
        point = (x, y, z)

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

    def handle_add_points_in_batch(self):
        """Adiciona um conjunto de pontos à lista por meio de um input de texto"""

        try:
            # tratamento do texto inserido
            text = self.batchPointsInput.text()
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

        # Conferindo se o número de coordenadas difere de 3
        for point in new_points:
            if len(point) != 3:
                self.show_error_message("Points must have 3 coordinates (x, y, z).")
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
        O filled só é habilitado se Polygon estiver selecionado e houver pelo menos 3 pontos.
        """

        num_points = len(self.points)
        if num_points >= 3 and self.polygonRadio.isChecked():
            self.fillCheckBox.setEnabled(True)
            self.fillCheckBox.setChecked(self.fill_state)

        else:
            self.fillCheckBox.setChecked(False)
            self.fillCheckBox.setEnabled(False)

    def _handle_fill_checkbox(self):
        """Gerencia o estado do checkbox 'Filled'"""

        if self.polygonRadio.isChecked():
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
            self.polygonRadio,
        ]

        for button in radio_buttons:
            button.setEnabled(False)
            button.setChecked(False)

        if num_points == 1:
            self.pointRadio.setEnabled(True)
            self.pointRadio.setChecked(True)

        if num_points == 2:
            self.lineRadio.setEnabled(True)
            self.lineRadio.setChecked(True)

        if num_points == 3:
            self.wireframeRadio.setEnabled(True)
            self.polygonRadio.setEnabled(True)
            self.wireframeRadio.setChecked(True)

        if num_points > 3:
            self.curveRadio.setEnabled(True)
            self.bSplineRadio.setEnabled(True)
            self.wireframeRadio.setEnabled(True)
            self.polygonRadio.setEnabled(True)
            self.wireframeRadio.setChecked(True)

    def _update_points_number(self):
        """Atualiza o número de pontos"""

        num_points = len(self.points)
        self.numPoints.setText(
            f'<html><head/><body><p><span style=" font-weight:700;">Number of points:</span> {num_points}</p></body></html>'
        )

    def _update_interface(self):
        """Atualiza a interface baseado no tipo de objeto selecionado"""

        self._update_points_number()
        self._update_object_type()
        self._update_fill_checkbox_visibility()


class EdgeDialog(GenericDialog):
    """Classe responsável por gerenciar o popup de criação de arestas para Wireframes."""

    def __init__(self, points: list[tuple[float, float, float]]):
        super().__init__("view/screens/addEdges.ui")

        self.points = points
        self.edges = (
            []
        )  # Lista para armazenar as arestas como tuplas de índices (idx1, idx2)

        self._fill_select_boxes()
        self._update_select_boxes()
        self._update_points_without_edges_list()  # Atualiza a lista inicialmente

        # Conecta botoes
        self.addEdgeButton.clicked.connect(
            lambda: self.add_edge(
                self.selectPoint1.currentIndex(), self.selectPoint2.currentIndex()
            )
        )
        self.removeButton.clicked.connect(self.remove_selected_edge)
        self.selectPoint1.currentIndexChanged.connect(self._update_select_boxes)
        self.selectPoint2.currentIndexChanged.connect(self._update_select_boxes)
        self.addOrderedEdgesButton.clicked.connect(self.add_ordered_edges)

    def _fill_select_boxes(self):
        """Preenche as caixas de seleção com os pontos disponíveis."""

        self.selectPoint1.clear()
        self.selectPoint2.clear()

        for i, point in enumerate(self.points):
            point_str = f"Point {i} ({point[0]:.1f}, {point[1]:.1f}, {point[2]:.1f})"
            self.selectPoint1.addItem(point_str, i)
            self.selectPoint2.addItem(point_str, i)

    def _update_select_boxes(self):
        """Garante que o mesmo ponto não possa ser selecionado em ambas as caixas de seleção e que não seja possível adicionar arestas já existentes."""

        idx1 = self.selectPoint1.currentIndex()
        idx2 = self.selectPoint2.currentIndex()

        self.addEdgeButton.setEnabled(
            idx1 != idx2 and tuple(sorted((idx1, idx2))) not in self.edges
        )

    def add_edge(self, idx1: int, idx2: int):
        """Adiciona uma nova aresta com base nos pontos selecionados."""

        if idx1 == -1 or idx2 == -1:
            self.show_error_message("Please select two points.")
            return

        if idx1 == idx2:
            self.show_error_message(
                "The initial and final points of the edge cannot be the same."
            )
            return

        # Normaliza a aresta para ter sempre o menor índice primeiro
        edge = tuple(sorted((idx1, idx2)))

        if edge in self.edges:
            self.show_error_message(
                f"Edge between Point {edge[0]} and Point {edge[1]} already exists."
            )
            return

        self.edges.append(edge)
        self._update_edges_list()
        self._update_select_boxes()
        self._update_points_without_edges_list()

    def remove_selected_edge(self):
        """Remove a aresta selecionada da lista."""

        current_item = self.pointsList.currentItem()

        if current_item:
            index = self.pointsList.row(current_item)

            if 0 <= index < len(self.edges):
                self.edges.pop(index)
                self._update_edges_list()
                self._update_points_without_edges_list()
                self._update_select_boxes()
            else:
                self.show_error_message("Invalid edge index.")

        else:
            self.show_error_message("Please select an edge to remove.")

    def add_ordered_edges(self):
        """Adiciona arestas ordenadas de acordo com a lista de pontos."""

        for i in range(len(self.points) - 1):
            if tuple(sorted((i, i + 1))) not in self.edges:
                self.add_edge(i, i + 1)

        if tuple(sorted((len(self.points) - 1, 0))) not in self.edges:
            self.add_edge(len(self.points) - 1, 0)

        self._update_edges_list()
        self._update_select_boxes()
        self._update_points_without_edges_list()

    def _update_edges_list(self):
        """Atualiza a QListWidget que mostra as arestas."""

        self.pointsList.clear()
        for edge in self.edges:
            item_text = f"Edge: Point {edge[0]} ({self.points[edge[0]][0]:.1f}, {self.points[edge[0]][1]:.1f}, {self.points[edge[0]][2]:.1f}) <-> Point {edge[1]} ({self.points[edge[1]][0]:.1f}, {self.points[edge[1]][1]:.1f}, {self.points[edge[1]][2]:.1f})"
            self.pointsList.addItem(item_text)

    def _update_points_without_edges_list(self):
        """Atualiza a lista de pontos que não pertencem a nenhuma aresta."""

        all_point_indices = set(range(len(self.points)))
        used_point_indices = set()

        for edge in self.edges:
            used_point_indices.add(edge[0])
            used_point_indices.add(edge[1])

        points_without_edges_indices = all_point_indices - used_point_indices

        self.pointsWithoutEdgesList.clear()
        for idx in sorted(list(points_without_edges_indices)):
            point = self.points[idx]
            point_str = f"Point {idx} ({point[0]:.1f}, {point[1]:.1f}, {point[2]:.1f})"
            self.pointsWithoutEdgesList.addItem(point_str)

    def accept(self):
        """Sobrescreve o método accept para validar o número de arestas"""

        if self.pointsWithoutEdgesList.count() > 0:
            self.show_error_message("There are points without edges.")
            return

        super().accept()


class SurfaceDialog(GenericDialog):
    def __init__(self, ui_path: str):
        super().__init__(ui_path)

        self.color: tuple = (0, 0, 0)
        self.colorButton.clicked.connect(self.choose_color)

    def convert_string_to_matrix(self, string: str) -> list[list[list[float]]]:
        """
        ***
        Método inteiramente gerado por IA
        - Modelo utilizado: gemini-2.5-pro-exp-05-06
        - URL da implementação do modelo: https://aistudio.google.com/
        - Finalidade: Implementar a lógica de conversão de uma string formatada de pontos de controle (e.g., "(x1,y1,z1),(x2,y2,z2);(x3,y3,z3),...") em uma matriz 3D de pontos (lista de listas de pontos [x,y,z]).
        - Prompt empregado: crie uma função capaz de converter uma string como (x11,y11,z11),(x12,y12,z12),(x13,y13,z13),(x14,y14,z14); (x21,y21,z21),(x22,y22,z22),(x23,y23,z23),(x24,y24,z24); (x31,y31,z31),(x32,y32,z32),(x33,y33,z33),(x34,y34,z34); (x41,y41,z41),(x42,y42,z42),(x43,y43,z43),(x44,y44,z44)   em uma matriz
        ***
        Converte uma string de pontos de controle em uma matriz de pontos.

        A string deve seguir o formato:
        "(x11,y11,z11),(x12,y12,z12),...; (x21,y21,z21),(x22,y22,z22),...; ..."
        - Cada ponto é uma tupla de 3 coordenadas (x, y, z).
        - Pontos dentro de uma mesma linha da matriz são separados por vírgulas.
        - Linhas da matriz são separadas por ponto e vírgula.
        - Espaços em branco e quebras de linha são ignorados.

        @param string: A string contendo os pontos de controle.
        @return: Uma lista de listas de pontos (list[list[list[float]]]), onde cada ponto é [x, y, z].
                 Retorna uma lista vazia se a string de entrada for vazia ou contiver apenas espaços.
        @raise ValueError: Se um ponto estiver malformado, não puder ser convertido para float,
                         ou se uma linha não contiver pontos no formato esperado.
        """
        if not string.strip():
            return []

        matrix_of_points: list[list[list[float]]] = []
        # Remove todos os espaços em branco e quebras de linha para simplificar o parsing
        processed_string = string.replace(" ", "").replace("\n", "")

        # Divide a string em representações de linha (separadas por ';')
        row_strings = processed_string.split(";")

        for row_str in row_strings:
            # Ignora linhas que ficaram vazias após o split
            if not row_str.strip():
                continue

            points_in_current_row: list[list[float]] = []
            # Regex corrigida para encontrar pontos no formato (num,num,num)
            point_matches = re.findall(r"\(([^,]+),([^,]+),([^)]+)\)", row_str)

            # Se a string da linha não é vazia mas não encontrou nenhum ponto, é um erro de formato
            if not point_matches and row_str.strip():
                raise ValueError(
                    f"Linha não contém pontos válidos no formato (x,y,z): '{row_str}'"
                )

            for match in point_matches:
                # match é uma tupla de strings, ex: ('1.0', '-2.5', '3')
                try:
                    x = float(match[0])
                    y = float(match[1])
                    z = float(match[2])
                    points_in_current_row.append([x, y, z])
                except ValueError as e:
                    # Levanta um erro mais informativo
                    raise ValueError(
                        f"Coordenada inválida no ponto '({match[0]},{match[1]},{match[2]})' na linha '{row_str}'. Erro original: {e}"
                    ) from e

            if points_in_current_row:
                matrix_of_points.append(points_in_current_row)

        return matrix_of_points

    def verify_size(self, size: int | None = None):
        """Verifica se o número de pontos é válido para a superfície."""

        try:
            matrix = self.convert_string_to_matrix(self.surfaceInput.toPlainText())

            if size is None:
                size = len(matrix)

            if (
                (not all(len(row) == size for row in matrix) or len(matrix) != size)
                and size >= 4
                and size <= 20
            ):
                self.show_error_message(f"The number of points must be {size}x{size}.")
                return

            self.name = self.nameInput.text()
            self.surface_points = matrix

        except ValueError as e:
            self.show_error_message(str(e))
            return

        super().accept()


class BezierSurfaceDialog(SurfaceDialog):
    """Classe responsável por gerenciar o popup de criação de superfície de Bézier."""

    def __init__(self):
        super().__init__("view/screens/bezierSurface.ui")

    def accept(self):
        """Sobrescreve o método accept para validar o número de pontos"""

        self.verify_size(4)


class BicubicSurfaceDialog(SurfaceDialog):
    """Classe responsável por gerenciar o popup de criação de superfície bicúbica."""

    def __init__(self):
        super().__init__("view/screens/bicubicSurface.ui")

    def accept(self):
        """Sobrescreve o método accept para validar o número de pontos"""

        self.verify_size()
