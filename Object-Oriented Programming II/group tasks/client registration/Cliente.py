from Pessoa import Pessoa

# modelo do padrão MVC
class Cliente(Pessoa):
    def __init__(self, codigo: int, nome: str):
        super().__init__(nome)
        self.__codigo = codigo

    @property
    def codigo(self):
        return self.__codigo
    
    @codigo.setter
    def codigo(self, codigo):
        self.__codigo = codigo

    def __str__(self):
        return f'Nome: {super().nome}, Codigo: {self.__codigo}'
