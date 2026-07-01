class Capitulo:
    def __init__(self, numero: int, titulo: str):
        #verificacao de tipagem
        if isinstance(numero, int):
            self.__numero = numero
        if isinstance(titulo, str):
            self.__titulo = titulo

    #getters e settes
    @property
    def numero(self):
        return self.__numero

    @numero.setter
    def numero(self, numero):
        self.__numero = numero

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, titulo):
        self.__titulo = titulo
