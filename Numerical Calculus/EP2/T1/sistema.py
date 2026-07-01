from abc import ABC, abstractmethod
import numpy as np


class SistemaLinear(ABC):
    def __init__(self, solutions):
        self.solutions = solutions

    @abstractmethod
    def f1(self, x, y):
        pass

    @abstractmethod
    def f2(self, x, y):
        pass

    @abstractmethod
    def jacobian(self, x, y):
        pass


class Sistema1(SistemaLinear):
    def f1(self, x, y):
        """Função f1(x, y) = x^2 - y^2 - 1."""
        return x**2 - y**2 - 1

    def f2(self, x, y):
        """Função f2(x, y) = 2xy."""
        return 2 * x * y

    def jacobian(self, x, y):
        """Matriz jacobiana."""
        return np.array([[2 * x, -2 * y], [2 * y, 2 * x]])


class Sistema2(SistemaLinear):
    def f1(self, x, y):
        """Função f1(x, y) = x^3 - 3xy^2 - 1."""
        return x**3 - 3 * x * (y**2) - 1

    def f2(self, x, y):
        """Função f2(x, y) = 3x^2y - y^3."""
        return 3 * (x**2) * y - y**3

    def jacobian(self, x, y):
        """Matriz jacobiana."""
        return np.array(
            [[3 * (x**2) - y**2, -6 * x * y], [6 * x * y, 3 * (x**2) - 3 * (y**2)]]
        )
