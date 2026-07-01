from editora import Editora
from autor import Autor
from capitulo import Capitulo


class Livro:
    def __init__(self, codigo: int, titulo: str,
                 ano: int, editora: Editora, autor: Autor,
                 numeroCapitulo: int, tituloCapitulo: str):
        # verificacao de tipagem
        if isinstance(codigo, int):
            self.__codigo = codigo
        if isinstance(titulo, int):
            self.__titulo = titulo
        if isinstance(ano, int):
            self.__ano = ano
        if isinstance(editora, Editora):
            self.__editora = editora
        if isinstance(autor, Autor):
            self.__autores = [autor]
        if isinstance(numeroCapitulo, int) and isinstance(tituloCapitulo, str):
            self.__capitulos = [Capitulo(numeroCapitulo, tituloCapitulo)]

    # getters e setters
    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo):
        self.__codigo = codigo

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, titulo):
        self.__titulo = titulo

    @property
    def ano(self):
        return self.__ano

    @ano.setter
    def ano(self, ano):
        self.__ano = ano

    @property
    def editora(self):
        return self.__editora

    @editora.setter
    def editora(self, editora):
        self.__editora = editora

    @property
    def autores(self):
        return self.__autores

    def incluirAutor(self, autor: Autor):
        if isinstance(autor, Autor) and not autor in self.autores:
            self.autores.append(autor)

    def excluirAutor(self, autor: Autor):
        if isinstance(autor, Autor) and autor in self.autores:
            self.autores.remove(autor)

    def incluirCapitulo(self, numeroCapitulo: int, tituloCapitulo: str):
        if not self.findCapituloByTitulo(tituloCapitulo) in self.__capitulos:
            if isinstance(numeroCapitulo, int):
                if isinstance(tituloCapitulo, str):
                    self.__capitulos.append(
                        Capitulo(numeroCapitulo, tituloCapitulo))

    def excluirCapitulo(self, tituloCapitulo: str):
        if self.findCapituloByTitulo(tituloCapitulo) in self.__capitulos:
            if isinstance(tituloCapitulo, str):
                self.__capitulos.remove(
                    self.findCapituloByTitulo(tituloCapitulo))

    def findCapituloByTitulo(self, tituloCapitulo: str):
        if isinstance(tituloCapitulo, str):
            for capitulo in self.__capitulos:
                if capitulo.titulo == tituloCapitulo:
                    return capitulo
        return None
