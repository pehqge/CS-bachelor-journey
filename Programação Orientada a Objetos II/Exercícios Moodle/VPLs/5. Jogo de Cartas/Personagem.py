from AbstractPersonagem import *


class Personagem(AbstractPersonagem):
    def __init__(self, energia: int, habilidade: int,
                 velocidade: int, resistencia: int, tipo: Tipo):
        if isinstance(energia, int):
            self.__energia = energia
        if isinstance(habilidade, int):
            self.__habilidade = habilidade
        if isinstance(velocidade, int):
            self.__velocidade = velocidade
        if isinstance(resistencia, int):
            self.__resistencia = resistencia
        if isinstance(tipo, Tipo):
            self.__tipo = tipo

    @property
    def tipo(self) -> Tipo:
        return self.__tipo

    @property
    def energia(self) -> int:
        return self.__energia

    @property
    def habilidade(self) -> int:
        return self.__habilidade

    @property
    def velocidade(self) -> int:
        return self.__velocidade

    @property
    def resistencia(self) -> int:
        return self.__resistencia
