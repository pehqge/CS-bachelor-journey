from tipoChamado import TipoChamado
from abstractControladorChamados import AbstractControladorChamados
from tipoChamado import TipoChamado
from chamado import Chamado
from datetime import date as Date
from cliente import Cliente
from tecnico import Tecnico
from collections import defaultdict


class ControladorChamados(AbstractControladorChamados):
    def __init__(self):
        self.__tipoChamados = []
        self.__chamados = []

    def totalChamadosPorTipo(self, tipo: TipoChamado) -> int:
        return len([i for i in self.__chamados if i.tipo == tipo])

    def incluiChamado(self, data: Date, cliente: Cliente,
                      tecnico: Tecnico, titulo: str, descricao: str,
                      prioridade: int, tipo: TipoChamado) -> Chamado:
        if (isinstance(data, Date) and
            isinstance(cliente, Cliente) and
            isinstance(tecnico, Tecnico) and
            isinstance(titulo, str) and
            isinstance(descricao, str) and
            isinstance(prioridade, int) and
                isinstance(tipo, TipoChamado)):
            cadastro_chamado = Chamado(
                data, cliente, tecnico, titulo, descricao, prioridade, tipo)
            if not cadastro_chamado in self.__chamados:
                self.__chamados.append(cadastro_chamado)
                return cadastro_chamado

    def incluiChamado(self, data, cliente, tecnico,
                      titulo, descricao, prioridade, tipo):
        if (isinstance(data, Date) and
                isinstance(cliente, Cliente) and
                isinstance(tecnico, Tecnico) and
                isinstance(titulo, str) and
                isinstance(descricao, str) and
                isinstance(prioridade, int) and
                isinstance(tipo, TipoChamado)):
            chamado = Chamado(data,
                              cliente,
                              tecnico,
                              titulo,
                              descricao,
                              prioridade,
                              tipo)
            call_already_exists = False
            for call in self.__chamados:
                if call == chamado:
                    call_already_exists = True
                    break
            if not call_already_exists:
                self.__chamados.append(chamado)
            return chamado

    def incluiTipoChamado(self, codigo: int, nome: str,
                          descricao: str) -> TipoChamado:
        cadastro_tipo = TipoChamado(codigo, descricao, nome)
        if not cadastro_tipo in self.__tipoChamados:
            self.__tipoChamados.append(cadastro_tipo)
            return cadastro_tipo

    @property
    def tipoChamados(self):
        return self.__tipoChamados
