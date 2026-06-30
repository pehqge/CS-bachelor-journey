from livro import Livro


class Biblioteca:
    def __init__(self):
        self.__livros = []

    def incluirLivro(self, livro: Livro):
        if isinstance(livro, Livro) and not livro in self.livros:
            self.livros.append(livro)

    def excluirLivro(self, livro: Livro):
        if isinstance(livro, Livro) and livro in self.livros:
            self.livros.remove(livro)

    @property
    def livros(self):
        return self.__livros
