import PySimpleGUI as sg


class MenuView:
    def __init__(self):
        self.tela_consulta()

    def tela_consulta(self):
        sg.theme('DarkTeal1')
        
        self.__container = [
            [sg.Text("Escolha uma opção: ", font=("Comic Sans MS", 20), pad=(100, 20))],
            [sg.Button("Gerar Votos", size=(13, 2), pad=(10, 0), font=("Comic Sans MS", 13)),
             sg.Button("Computar Votos", size=(13, 2), pad=(10, 0), font=("Comic Sans MS", 13))],
            [sg.Text('')]
        ]

        self.__window = sg.Window(
            'Menu', self.__container, font=("Helvetica", 14))

    def le_eventos(self):
        return self.__window.read()

    def fim(self):
        return self.__window.close()

    @property
    def window(self):
        return self.__window.close()