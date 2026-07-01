from amigo import Amigo
from livro import Livro
from datetime import datetime


class Emprestimo:
    def __init__(self,
                 amigo: Amigo,
                 livro: Livro,
                 data_inicio: datetime,
                 observacao: str):
        if isinstance(amigo, Amigo):
            self.__amigo = amigo
        if isinstance(livro, Livro):
            self.__livro = livro
        if isinstance(data_inicio, datetime):
            self.__data_inicio = data_inicio
        self.__data_fim = None
        if isinstance(observacao, str):
            self.__observacao = observacao

    @property
    def amigo(self):
        return self.__amigo

    @property
    def livro(self):
        return self.__livro

    @property
    def data_inicio(self):
        return self.__data_inicio

    @property
    def data_fim(self):
        return self.__data_fim

    @property
    def observacao(self):
        return self.__observacao

    @data_fim.setter
    def data_fim(self, data):
        self.__data_fim = data

    def ativo(self):
        if self.data_fim == None:
            return True
        else:
            return False

    def __str__(self):
        if self.ativo():
            return f"O livro {self.livro.titulo} está emprestado para {self.amigo.nome}"
        else:
            return f"O livro foi devolvido"

    def __eq__(self, livro):
        if isinstance(livro, Livro):
            return (self.livro == livro and self.ativo())
        else:
            return False
