import PySimpleGUI as sg

# View do padrão MVC


class ClienteView():
    def __init__(self, controlador):
        self.__controlador = controlador
        self.__container = []
        self.__window = sg.Window(
            "Consulta de clientes", self.__container, font=("Helvetica", 14))

    def tela_consulta(self):
        self.__container = [
            [sg.Text('       Banco de Clientes', font=('Futura', 24))],
            [sg.Text('', size=(15, 1))],
            [sg.Text('Nome  '), sg.InputText(key="nome")],
            [sg.Text('Código  '), sg.InputText(key="codigo")],
            [sg.Text('', size=(15, 1))],
            [sg.Button('Cadastrar', size=(55, 1)),
             sg.Button('Consultar', size=(55, 1))]
        ]
        self.__window = sg.Window(
            "Consulta de clientes", self.__container, font=("Helvetica", 14))

    def erro_cliente_existente(self):
        sg.popup_error(
            "Este cliente já existe em nosso banco de dados. Tente novamente.")

    def tela_adicionado(self, nome):
        sg.popup(f"O cliente {nome} foi adicionado com sucesso!")

    def mostrar_cliente(self, cliente):
        sg.popup(f"Seu cliente foi encontrado:\n {cliente}")

    def erro_vazio(self):
        sg.popup_error("Por favor, escreva algo nas caixas")
        
    def le_eventos(self):
        return self.__window.read()

    def fim(self):
        self.__window.close()
