from abstractChamado import AbstractChamado
from tipoChamado import TipoChamado
from datetime import date as Date
from cliente import Cliente
from tecnico import Tecnico


class Chamado(AbstractChamado):
    def __init__(
            self,
            data: Date,
            cliente: Cliente,
            tecnico: Tecnico,
            titulo: str,
            descricao: str,
            prioridade: int,
            tipo: TipoChamado):
        if isinstance(data, Date):
            self.__data = data
        if isinstance(cliente, Cliente):
            self.__cliente = cliente
        if isinstance(tecnico, Tecnico):
            self.__tecnico = tecnico
        if isinstance(titulo, str):
            self.__titulo = titulo
        if isinstance(descricao, str):
            self.__descricao = descricao
        if isinstance(prioridade, int):
            self.__prioridade = prioridade
        if isinstance(tipo, TipoChamado):
            self.__tipo = tipo

    @property
    def cliente(self):
        return self.__cliente

    @property
    def data(self):
        return self.__data

    @property
    def descricao(self):
        return self.__descricao

    @property
    def prioridade(self):
        return self.__prioridade

    @property
    def tecnico(self):
        return self.__tecnico

    @property
    def tipo(self):
        return self.__tipo

    @property
    def titulo(self):
        return self.__titulo

    # data, cliente, técnico e tipo de chamado.
    def __eq__(self, outro: object) -> bool:
        if isinstance(outro, Chamado):
            return (outro.data == self.data
                    and outro.tecnico == self.tecnico
                    and outro.tipo == self.tipo
                    and outro.cliente == self.cliente)
        else:
            return False
