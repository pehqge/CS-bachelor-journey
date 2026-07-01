from dataclasses import dataclass


@dataclass
class Bounds:
    """Classe para armaezar os limites de uma área."""

    x_min: float
    x_max: float
    y_min: float
    y_max: float
