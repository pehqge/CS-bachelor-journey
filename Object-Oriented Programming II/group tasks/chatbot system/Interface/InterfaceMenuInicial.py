import PySimpleGUI as sg
from SistemaChatBot.SistemaChatBot import SistemaChatBot as scb

class MenuInicialView:
    def __init__(self, sistema: scb):
        self.__sistema = sistema
        self.__container = []
        self.__window = sg.Window(
            "Menu Inicial", self.__container, font=("Montserrat", 14))
        
    @property
    def window(self):
        return self.__window
    
    def tela_inicial(self):
        self.__container = [
            [sg.Text(f'Bem vindo ao ChatBot da empresa {self.__sistema.empresa}!', font=('Montserrat', 24, "bold"))],
            [sg.Text('Por favor, selecione uma opção:', font=('Montserrat', 18))],
            [sg.Text('', size=(15, 1))],
            [sg.Button('BotMaker', size=(21, 1), pad=(5, 3)), sg.Button('Chat', size=(21, 1), pad=(5, 3)), sg.Button("Sair", size=(10,1), pad=(5,3), button_color=('white', '#cd2525'))]
        ]
        self.__window = sg.Window(
            "Menu Inicial", self.__container, font=("Montserrat", 14))
        return self.window
    