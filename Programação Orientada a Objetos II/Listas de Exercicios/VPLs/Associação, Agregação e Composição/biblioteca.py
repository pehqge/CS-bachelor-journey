from livro import Livro


class Biblioteca:
    def __init__(self):
        self.__livros = []

    def incluirLivro(self, livro: Livro):
        #Nao esqueca de garantir que o objeto recebido pertence a classe Livro...
        ...

    def excluirLivro(self, livro: Livro):
        ...

    @property
    def livros(self):
        return self.__livros
