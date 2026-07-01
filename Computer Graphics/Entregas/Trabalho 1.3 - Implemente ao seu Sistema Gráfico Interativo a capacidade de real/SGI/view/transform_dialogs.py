"""
Módulo que contém classes relativas às caixas de diálogo para transformação de objetos
"""
from PyQt6 import QtWidgets, uic


class TransformationDialog(QtWidgets.QDialog):
    """
    Classe que representa uma caixa de diálogo para adicionar múltiplas transformações a um objeto.
    Permite adicionar translações, escalonamentos e rotações a uma lista.
    Ao confirmar, retorna a lista de transformações a serem aplicadas sequencialmente.
    """

    def __init__(self):
        super().__init__()
        uic.loadUi("view/screens/transformations.ui", self)

        self.transformations = []  # Lista para armazenar os dicionários de transformação
        
        self.addTranslationButton.clicked.connect(self.add_translation)
        self.addScalingButton.clicked.connect(self.add_scaling)
        self.addRotationBtn.clicked.connect(self.add_rotation)
        
        self.removeTransformationBtn.clicked.connect(self.remove_transformation)
        
        self.arbitraryBtn.toggled.connect(self.toggle_arbitrary_point_input)

    def toggle_arbitrary_point_input(self, checked):
        """Habilita/desabilita os inputs de ponto arbitrário para rotação."""
        
        self.rotationXInput.setEnabled(checked)
        self.rotationYInput.setEnabled(checked)

    def get_transformations(self) -> list[dict] | None:
        """Exibe o diálogo e retorna a lista de transformações ou None se cancelado."""
        
        self.show()
        result = self.exec()

        if result == QtWidgets.QDialog.DialogCode.Rejected:
            return None

        return self.transformations

    def add_translation(self):
        """Adiciona uma transformação de translação à lista."""
        
        dx = self.translationXInput.value()
        dy = self.translationYInput.value()
        
        if dx == 0 and dy == 0:
            return
            
        transformation = {"type": "translation", "dx": dx, "dy": dy}
        self.transformations.append(transformation)
        self.transformationsList.addItem(f"Translate: ({dx:.2f}, {dy:.2f})")

    def add_scaling(self):
        """Adiciona uma transformação de escalonamento à lista."""
        
        if self.scalingTab.currentIndex() == 0: # Tab "Coordinates"
            sx = self.scalingXInput.value() / 100.0
            sy = self.scalingYInput.value() / 100.0
            
            if sx == 1 and sy == 1:
                return
            
            label = f"Scale: (x: {sx*100:.1f}%, y: {sy*100:.1f}%)"
            
        else: # Tab "Proportion"
            proportion = self.scalingProportionInput.value() / 100.0
            sx = proportion
            sy = proportion
            
            if sx == 1:
                return
            
            label = f"Scale: ({proportion*100:.1f}%)"
            
        transformation = {"type": "scaling", "sx": sx, "sy": sy}
        self.transformations.append(transformation)
        self.transformationsList.addItem(label)
        
        # reseta os inputs (evita adicionar a mesma transformação de novo)
        self.scalingXInput.setValue(100.0)
        self.scalingYInput.setValue(100.0)
        self.scalingProportionInput.setValue(100.0)

    def add_rotation(self):
        """Adiciona uma transformação de rotação à lista."""
        
        angle = self.angleInput.value()
        
        if angle == 0:
            return

        # origem
        cx, cy = 0, 0 
        point_label = "origin"

        if self.objCenterBtn.isChecked(): # centro do objeto
            cx, cy = "obj_center", "obj_center"
            point_label = "object center"
            
        elif self.arbitraryBtn.isChecked(): # ponto arbitrario
            cx = self.rotationXInput.value()
            cy = self.rotationYInput.value()
            point_label = f"({cx:.2f}, {cy:.2f})"

        transformation = {"type": "rotation", "angle": angle, "cx": cx, "cy": cy}
        self.transformations.append(transformation)
        self.transformationsList.addItem(f"Rotate: {angle:.2f}° about {point_label}")
        
        # reseta o angulo
        self.angleInput.setValue(0.0)

    def remove_transformation(self):
        """Remove a transformação selecionada da lista."""
        
        selected_row = self.transformationsList.currentRow()
        
        if selected_row >= 0:
            self.transformationsList.takeItem(selected_row)
            self.transformations.pop(selected_row)
