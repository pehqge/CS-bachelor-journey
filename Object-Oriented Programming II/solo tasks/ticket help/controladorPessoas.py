from abstractControladorPessoas import AbstractControladorPessoas
from cliente import Cliente
from tecnico import Tecnico


class ControladorPessoas(AbstractControladorPessoas):
    def __init__(self):
        self.__clientes = []
        self.__tecnicos = []

    @property
    def clientes(self):
        return self.__clientes

    @property
    def tecnicos(self):
        return self.__tecnicos

    def incluiCliente(self, codigo: int, nome: str) -> Cliente:
        novoCliente = Cliente(nome, codigo)
        if not novoCliente in self.clientes:
            self.clientes.append(novoCliente)
            return novoCliente

    def incluiTecnico(self, codigo: int, nome: str) -> Tecnico:
        novoTecnico = Tecnico(nome, codigo)
        if not novoTecnico in self.tecnicos:
            self.tecnicos.append(novoTecnico)
            return novoTecnico
