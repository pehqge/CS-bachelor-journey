from abc import ABC, abstractmethod
from Carta import *
from AbstractJogador import *
import random


class Jogador(AbstractJogador):

    def __init__(self, nome: str):
        self.__nome = nome
        self.__mao = []

    @property
    def nome(self) -> str:
        return self.__nome

    def baixa_carta_da_mao(self) -> Carta:
        tirada = random.choice(self.mao)
        self.mao.remove(tirada)
        return tirada

    @property
    def mao(self) -> list:
        return self.__mao

    def inclui_carta_na_mao(self, carta: Carta):
        if isinstance(carta, Carta):
            self.mao.append(carta)
