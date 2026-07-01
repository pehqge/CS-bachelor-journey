from AbstractPersonagem import *


class Personagem(AbstractPersonagem):
    def __init__(self, energia, habilidade, velocidade, resistencia, tipo):
        self.__energia = energia
        self.__habilidade = habilidade
        self.__velocidade = velocidade
        self.__resistencia = resistencia
        self.__tipo = tipo

    @property
    def energia(self):
        return self.__energia

    @property
    def habilidade(self):
        return self.__habilidade

    @property
    def velocidade(self):
        return self.__velocidade

    @property
    def resistencia(self):
        return self.__resistencia

    @property
    def tipo(self):
        return self.__tipo
