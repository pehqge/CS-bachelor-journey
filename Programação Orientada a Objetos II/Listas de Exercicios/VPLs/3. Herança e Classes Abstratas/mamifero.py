from animal import Animal
from abc import ABC, abstractmethod


class Mamifero(Animal, ABC):
    def __init__(self, volumeSom: int, tamanhoPasso: int):
        super().__init__(tamanhoPasso)
        if isinstance(volumeSom, int):
            self.__volumeSom = volumeSom

    @property
    def volumeSom(self):
        return self.__volumeSom

    @volumeSom.setter
    def volumeSom(self, volumeSom):
        self.__volumeSom = volumeSom

    @abstractmethod
    def produzirSom(self):
        pass
