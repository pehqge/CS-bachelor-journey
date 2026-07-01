from abstractControladorElevador import AbstractControladorElevador
from elevador import Elevador
from comandoInvalidoException import ComandoInvalidoException


class ControladorElevador(AbstractControladorElevador):
    def __init__(self):
        self.__elevador = None

    def subir(self):
        return self.__elevador.subir()

    def descer(self):
        return self.__elevador.descer()

    def entraPessoa(self):
        return self.__elevador.entraPessoa()

    def saiPessoa(self):
        return self.__elevador.saiPessoa()

    def inicializarElevador(self,
                            andarAtual: int,
                            totalAndaresPredio: int,
                            capacidade: int,
                            totalPessoas: int):
        self.__elevador = Elevador(andarAtual,
                                   totalAndaresPredio,
                                   capacidade,
                                   totalPessoas)

    @property
    def elevador(self):
        return self.__elevador
