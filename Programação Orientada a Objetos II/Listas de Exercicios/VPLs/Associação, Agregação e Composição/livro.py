from editora import Editora
from autor import Autor
from capitulo import Capitulo

class Livro:
    def __init__(self, codigo: int, titulo: str, ano: int, editora: Editora, autor: Autor, numeroCapitulo: int, tituloCapitulo: str):
        ...

    @property
    def codigo(self):
        return self.__codigo

    ... Adicionar demais getters

    @codigo.setter
    def codigo(self, codigo):
        self.__codigo = codigo

    ... Adicionar demais setters
    

    def incluirAutor(self, autor: Autor):
        #Nao esqueca de garantir que o objeto recebido pertence a classe Autor...
        ... Nao permitir insercao de Autores duplicados!

    def excluirAutor(self, autor: Autor):
        ...

    def incluirCapitulo(self, numeroCapitulo: int, tituloCapitulo: str):
        ... Nao permitir insercao de Capitulos duplicados!

    def excluirCapitulo(self, tituloCapitulo: str):
        ...

    def findCapituloByTitulo(self, tituloCapitulo: str):
        ...

