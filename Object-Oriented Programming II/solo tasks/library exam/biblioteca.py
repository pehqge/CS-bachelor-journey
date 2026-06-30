from amigo import Amigo
from livro import Livro
from emprestimo import *


class BibliotecaPessoal:
    def __init__(self,
                 amigos: list,
                 livros: list,):
        if (isinstance(amigos, list)
                and all(isinstance(x, Amigo) for x in amigos)):
            self.__amigos = amigos
        if (isinstance(livros, list)
                and all(isinstance(x, Livro) for x in livros)):
            self.__livros = livros
        self.__emprestimos = []

    @property
    def amigos(self):
        return self.__amigos

    @property
    def livros(self):
        return self.__livros

    @property
    def emprestimos(self):
        return self.__emprestimos

    def adiciona_amigo(self, amigo: Amigo):
        if isinstance(amigo, Amigo):
            self.amigos.append(amigo)

    def adiciona_livro(self, livro: Livro):
        if isinstance(livro, Livro):
            self.livros.append(livro)

    def empresta_livro(self,
                       amigo: Amigo,
                       livro: Livro,
                       data: datetime):
        emprestimo = Emprestimo(amigo, livro, data, "")
        self.emprestimos.append(emprestimo)
        self.livros.remove(livro)

    def devolve_livro(self,
                      livro: Livro,
                      data: datetime):
        tirar = [emprestimo for emprestimo in self.emprestimos if livro == emprestimo]
        if tirar == []:
            print("Este livro não está emprestado, tente novamente")
        else:
            tirar[0].data_fim = data
            self.livros.append(livro)

    def ver_livros_emprestados(self):
        return [emprestimo for emprestimo in self.emprestimos if emprestimo.ativo()]
