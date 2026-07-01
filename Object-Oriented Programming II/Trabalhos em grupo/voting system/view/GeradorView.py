import PySimpleGUI as sg

class GeradorView:
    def __init__(self):
        self.tela_consulta()

    def tela_consulta(self):
        sg.theme('DarkTeal1')
        
        self.__container = [
        [sg.Text('Gerador de Votos', font=("Comic Sans MS", 25), pad=(60, 20))],
        [sg.Text('Selecione uma pasta para salvar os votos gerados:', font=("Comic Sans MS", 15))],
        [sg.InputText(key="-FOLDER-", enable_events=True, size=(45, 10)),
        sg.FolderBrowse(button_text="Procurar")],
        [sg.Text('Escreva quantos candidatos e regiões deseja gerar:', font=("Comic Sans MS", 15))],
        [sg.Text('Candidatos:', font=("Comic Sans MS", 15)), sg.InputText(key="-CANDIDATOS-", size=(5, 1)),
        sg.Text('Regiões:', font=("Comic Sans MS", 15)), sg.InputText(key="-REGIOES-", size=(5, 20))],
        [sg.Text('')],
        [sg.Button('Gerar Votos', font=("Comic Sans MS", 15), pad=(20,0)), sg.Button('Voltar', font=("Comic Sans MS", 15),button_color='red', pad=(0, 0))],
        [sg.Text('')],
    ]
        self.__window = sg.Window("Gerador de votos", self.__container)
    
    def mostra_resultado(self):
        pass

    def le_eventos(self):
        return self.__window.read()
    
    def fim(self):
        return self.__window.close()

    