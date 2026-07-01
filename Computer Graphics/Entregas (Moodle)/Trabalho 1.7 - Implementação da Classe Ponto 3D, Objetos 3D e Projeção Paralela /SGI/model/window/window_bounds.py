from dataclasses import dataclass

import numpy as np


@dataclass
class WindowBounds:
    """
    Classe para armazenar os limites da Window: canto inferior esquerdo e canto superior direito.
    """

    x_lower_left: float
    y_lower_left: float
    z_lower_left: float
    x_upper_right: float
    y_upper_right: float
    z_upper_right: float

    @property
    def lower_left_point(self) -> np.ndarray:
        """
        Retorna o ponto inferior esquerdo da janela como um vetor numpy em coordenadas homogêneas.
        """
        return np.array(
            [
                self.x_lower_left,
                self.y_lower_left,
                self.z_lower_left,
                1.0,
            ]
        )

    @lower_left_point.setter
    def lower_left_point(self, value: np.ndarray) -> None:
        self.x_lower_left = value[0]
        self.y_lower_left = value[1]
        self.z_lower_left = value[2]

    @property
    def upper_right_point(self) -> np.ndarray:
        """
        Retorna o ponto superior direito da janela como um vetor numpy em coordenadas homogêneas.
        """
        return np.array(
            [
                self.x_upper_right,
                self.y_upper_right,
                self.z_upper_right,
                1.0,
            ]
        )

    @upper_right_point.setter
    def upper_right_point(self, value: np.ndarray) -> None:
        self.x_upper_right = value[0]
        self.y_upper_right = value[1]
        self.z_upper_right = value[2]
