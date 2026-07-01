import PySimpleGUI as sg

class ComputaView:
    def __init__(self):
        self.tela_consulta()
     
    def tela_consulta(self):
        sg.theme('DarkTeal1')
        
        self.__container = [
        [sg.Text('Computação de Votos', font=("Comic Sans MS", 25), pad=(100, 20))],
        [sg.InputText(key="-FOLDER-",enable_events=True, size=(45, 0)), sg.FolderBrowse(button_text="Selecionar", font=("Comic Sans MS", 12))],
        [sg.Text('Selecione o tipo do gráfico:', font=("Comic Sans MS", 15)), sg.Combo(['bar','pie'], size=(17,0), key='-COMBO-', default_value=None, font=("Comic Sans MS", 15))],
        [sg.Text('')],
        [sg.Button('Computa Região', font=("Comic Sans MS", 15)), sg.Button('Computa Candidatos', font=("Comic Sans MS", 15)), sg.Button('Voltar', font=("Comic Sans MS", 15),button_color='red')]]  
        self.__window = sg.Window('Computacao de votos', self.__container, font=("Helvetica", 14))
        
    def mostra_resultado(self):
        pass

    def le_eventos(self):
        return self.__window.read()
    
    def fim(self):
        return self.__window.close()

    