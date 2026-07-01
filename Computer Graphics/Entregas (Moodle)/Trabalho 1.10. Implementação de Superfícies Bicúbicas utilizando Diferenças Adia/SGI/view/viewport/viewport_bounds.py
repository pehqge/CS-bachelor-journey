from dataclasses import dataclass


@dataclass
class ViewportBounds:
    """
    Classe para armazenar os limites do viewport
    """

    x_upper_left: float
    y_upper_left: float
    x_lower_right: float
    y_lower_right: float
