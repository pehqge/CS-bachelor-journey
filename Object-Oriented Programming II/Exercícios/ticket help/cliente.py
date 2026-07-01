from pessoa import Pessoa


class Cliente(Pessoa):
    def __init__(self, nome: str, codigo: int):
        if isinstance(nome, str):
            self.__nome = nome
        if isinstance(codigo, int):
            self.__codigo = codigo

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo):
        self.__codigo = codigo

    def __eq__(self, outro: object) -> bool:
        if isinstance(outro, Cliente):
            return outro.codigo == self.codigo
        else:
            return False
