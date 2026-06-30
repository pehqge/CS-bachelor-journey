from animal import Animal
from abc import ABC, abstractmethod


class Ave(Animal, ABC):
    def __init__(self, tamanhoPasso: int, alturaVoo: int):
        super().__init__(tamanhoPasso)
        if isinstance(alturaVoo, int):
            self.__alturaVoo = alturaVoo

    @property
    def alturaVoo(self):
        return self.__alturaVoo

    @alturaVoo.setter
    def alturaVoo(self, alturaVoo):
        self.__alturaVoo = alturaVoo

    @abstractmethod
    def mover(self):
        pass

    @abstractmethod
    def produzirSom(self):
        pass
