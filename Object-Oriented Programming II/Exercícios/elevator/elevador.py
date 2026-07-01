from abstractElevador import AbstractElevador
from elevadorCheioException import ElevadorCheioException
from elevadorJahNoTerreoException import ElevadorJahNoTerreoException
from elevadorJahNoUltimoAndarException import ElevadorJahNoUltimoAndarException
from elevadorJahVazioException import ElevadorJahVazioException
from comandoInvalidoException import ComandoInvalidoException


class Elevador(AbstractElevador):
    def __init__(self,
                 andarAtual,
                 totalAndaresPredio,
                 capacidade,
                 totalPessoas):
        if isinstance(capacidade, int) and capacidade >= 0:
            self.__capacidade = capacidade
        else:
            raise ComandoInvalidoException
        if isinstance(totalAndaresPredio, int) and totalAndaresPredio >= 0:
            self.__totalAndaresPredio = totalAndaresPredio
        else:
            raise ComandoInvalidoException
        if (isinstance(andarAtual, int)
            and andarAtual >= 0
                and andarAtual < self.__totalAndaresPredio):
            self.__andarAtual = andarAtual
        else:
            raise ComandoInvalidoException
        if (isinstance(totalPessoas, int)
            and totalPessoas >= 0
                and totalPessoas <= self.__capacidade):
            self.__totalPessoas = totalPessoas
        else:
            raise ComandoInvalidoException

    def descer(self):
        try:
            if self.__andarAtual == 0:
                raise ElevadorJahNoTerreoException
            self.__andarAtual -= 1
            return f"O elevador agora está no andar {self.__andarAtual}"
        except ElevadorJahNoTerreoException:
            raise ElevadorJahNoTerreoException

    def entraPessoa(self):
        try:
            if self.capacidade == self.totalPessoas:
                raise ElevadorCheioException
            self.__totalPessoas += 1
            return f"Agora o elevador está com {self.__totalPessoas} Pessoas"
        except ElevadorCheioException:
            raise ElevadorCheioException

    def saiPessoa(self):
        try:
            if self.totalPessoas == 0:
                raise ElevadorJahVazioException
            self.__totalPessoas -= 1
            return f"Agora o elevador está com {self.__totalPessoas} Pessoas"
        except ElevadorJahVazioException:
            raise ElevadorJahVazioException

    def subir(self):
        try:
            if self.__andarAtual + 1 == self.__totalAndaresPredio:
                raise ElevadorJahNoUltimoAndarException
            self.__andarAtual += 1
            return f"O elevador agora está no andar {self.__andarAtual}"
        except ElevadorJahNoUltimoAndarException:
            raise ElevadorJahNoUltimoAndarException

    @property
    def capacidade(self):
        return self.__capacidade

    @property
    def totalPessoas(self):
        return self.__totalPessoas

    @property
    def totalAndaresPredio(self):
        return self.__totalAndaresPredio

    @property
    def andarAtual(self):
        return self.__andarAtual

    @totalAndaresPredio.setter
    def totalAndaresPredio(self, totalAndaresPredio):
        self.__totalAndaresPredio = totalAndaresPredio
