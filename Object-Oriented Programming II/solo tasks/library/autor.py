class Autor:
    def __init__(self, codigo: int, nome: str):
        #verificacao de tipagem
        if isinstance(codigo, int):
            self.__codigo = codigo
        if isinstance(nome, str):
            self.__nome = nome

    # getters e setters
    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo):
        self.__codigo = codigo

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome
