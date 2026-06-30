import PySimpleGUI as sg
from Bots.Bot import Bot
from SistemaChatBot.SistemaChatBot import SistemaChatBot as scb


class InterfaceChat:
    def __init__(self, sistema: scb):
        self.__sistema = sistema
    
    @property
    def window(self):
        return self.__window
    
    @property
    def sistema(self):
        return self.__sistema
    
    def tela_selecao_bot(self):
        self.__container = [
            [sg.Text('Por favor selecione um bot', font=('Montserrat', 24, "bold"))],
            [sg.Text('Bot:', font=('Montserrat', 16), pad=(0, 18)), sg.Combo(self.sistema.lista_bots, readonly=True, key='bot')], 
            [sg.Button('Ok', size=(5,1)), sg.Button('Voltar', size=(5,1))]
        ]
        self.__window = sg.Window(
            "Selecao de Bot", self.__container, font=("Montserrat", 14))
        return self.window
        
    def tela_chat(self, bot: Bot):
        self.__container = [
            [sg.Text(f'Sistema ChatBot {self.__sistema.empresa}', font=('Montserrat', 24, "bold"))],
            [sg.Text(f'Você está conversando com o bot {bot.nome}, seja gentil!', font=('Montserrat', 16))],
            [sg.Multiline(size=(72, 20), font=('Montserrat', 14), key='-OUT-', autoscroll=True, disabled=True, pad=(10, 18), default_text="Por favor, selecione uma das perguntas no dropdown e clique em enviar.")],
            [sg.Text(' Selecione sua pergunta:', font=('Montserrat', 16)), sg.Combo(bot.perguntas_respostas, size=(40, 1), readonly=True, key="pergunta"), sg.Button('Enviar', size=(10, 1))], 
            [sg.Button('Voltar', size=(10, 1))]
            ]
        
        self.__window = sg.Window(
            f"ChatBot com {bot.nome}", self.__container, font=("Montserrat", 14))
        return self.window
        