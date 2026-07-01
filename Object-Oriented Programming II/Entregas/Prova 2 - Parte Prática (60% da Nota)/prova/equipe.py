import random

class Equipe:
    def __init__(self, nome, treinador):
        if isinstance(nome, str) and isinstance(treinador, str):
            self.__nome = nome
            self.__treinador = treinador
        else:
            raise ValueError
        self.__pontos = 0

    @property
    def nome(self):
        return self.__nome
    
    @property
    def pontos(self):
        return self.__pontos
    
    @pontos.setter
    def pontos(self, ponto):
        self.__pontos = ponto