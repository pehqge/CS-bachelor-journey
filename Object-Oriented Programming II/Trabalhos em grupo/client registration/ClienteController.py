from ClienteView import ClienteView
from Cliente import Cliente
from ClienteDAO import ClienteDAO
import PySimpleGUI as sg 

class ClienteController:
    def __init__(self):
        self.__telaCliente = ClienteView(self)
        self.__clienteDAO =  ClienteDAO()

    def inicia(self):
        self.__telaCliente.tela_consulta()
        
        # Loop de eventos
        rodando = True
        resultado = ''
        while rodando:
            event, values = self.__telaCliente.le_eventos()

            if event == sg.WIN_CLOSED:
                rodando = False
            elif event == 'Cadastrar':
                try:
                    if int(values["codigo"]) in self.__clienteDAO.cache:
                        raise KeyError
                    if values["nome"] == "":
                        raise ValueError
                    self.adiciona_cliente(int(values["codigo"]), values["nome"])
                    self.__telaCliente.tela_adicionado(values["nome"])
                    print("cadastrei")
                except KeyError:
                    self.__telaCliente.erro_cliente_existente()
                except ValueError:
                    self.__telaCliente.erro_vazio()
                    
            elif event == 'Consultar':
                if values["codigo"] != '':
                    self.__telaCliente.mostrar_cliente(self.busca_codigo(int(values["codigo"])))
                else:
                    if values["nome"] != '':
                        self.__telaCliente.mostrar_cliente(self.busca_nome(values["nome"]))
                    else:
                        self.__telaCliente.erro_vazio()

        self.__telaCliente.fim()


    def busca_codigo(self, codigo):
        try:
            return self.__clienteDAO.get(codigo)
        except KeyError:
            raise KeyError

    # cria novo OBJ cliente e adiciona ao dict
    def adiciona_cliente(self, codigo, nome):
        self.__clienteDAO.add(Cliente(codigo, nome))
    
    def busca_nome(self, nome):
        if isinstance(nome, str):
            return self.__clienteDAO.busca_nome(nome)
    
    def cliente_existente(self, codigo):
        if codigo in self.__clienteDAO.cache:
            raise KeyError