import PySimpleGUI as sg
from Bots.PerguntaResposta import PerguntaResposta
from SistemaChatBot.SistemaChatBot import SistemaChatBot as scb
from Bots.Bot import Bot
from SistemaChatBot.BotMaker import BotMaker

class BotMakerView:
    def __init__(self, sistema: scb, botmaker: BotMaker):
        self.__sistema = sistema
        self.__container = []
        self.__botmaker = botmaker
        self.__window = sg.Window(
            "Criador de Bots", self.__container, font=("Montserrat", 14))

    @property
    def sistema(self):
        return self.__sistema
    
    @property
    def window(self):
        return self.__window
    
    @property
    def botmaker(self):
        return self.__botmaker
    
    def tela_selecao_inicial(self):
        self.__container = [
            [sg.Text('BotMaker selecionado!', font=('Montserrat', 24, "bold"))],
            [sg.Text('Por favor, selecione uma opção:', font=('Montserrat', 16))],
            [sg.Button('Criar', size=(12, 1), pad=(20, 0)), sg.Button('Editar', size=(12, 1), pad=(20, 15))],
            [sg.Button('Voltar', size=(12, 1), pad=(100, 0), button_color=('white', 'gray'))],
        ]
        self.__window = sg.Window(
            "Selecionador do BotMaker", self.__container, font=("Montserrat", 14))
        return self.window
    
    def tela_criacao(self):
        self.__container = [
            [sg.Text('Criar um novo Bot', font=('Montserrat', 24, "bold"))],
            [sg.Text('Por favor, preencha os dados abaixo:', font=('Montserrat', 16))],
            [sg.Text('', size=(15, 1))],
            [sg.Text('Nome do bot:  '), sg.Text('', size=(12, 1)), sg.InputText(key="nome", default_text=self.botmaker.valores_padrao["nome"], size=(56, 1))],
            [sg.Text('Apresentação do bot:'), sg.Text('', size=(7, 1)), sg.InputText(key="apresentacao", size=(56, 1), default_text=self.botmaker.valores_padrao["apresentacao"])],
            [sg.Text('Mensagem de boas vindas:'), sg.Text('', size=(3, 1)), sg.InputText(key="boas_vindas", size=(56, 1), default_text=self.botmaker.valores_padrao["boas_vindas"])],
            [sg.Text('Mensagem de despedida:'), sg.Text('', size=(4, 1)), sg.InputText(key="despedida", size=(56, 1), default_text=self.botmaker.valores_padrao["despedida"])],
            [sg.Text('Perguntas e respostas:'), sg.Text('', size=(6, 1)), sg.Combo(self.botmaker.perguntas_respostas, size=(30, 1), key="pergunta_resposta", readonly=True), sg.Button('Editar', size=(10, 1)), sg.Button('Novo', size=(10, 1))],
            [sg.Text('', size=(15, 1))],
            [sg.Button('Criar', size=(25, 1), pad=(5, 0)), sg.Button('Voltar', size=(25, 1), pad=(5, 0), button_color=('white', 'gray'))],
        ]
        self.__window = sg.Window(
            "Criador de Bots", self.__container, font=("Montserrat", 14))
        return self.window
    
    def tela_criar_pergunta_resposta(self):
        self.__container = [
            [sg.Text('Criador de Perguntas e Respostas:', font=('Montserrat', 24, "bold"))],
            [sg.Text('Pergunta:', font=('Montserrat', 16)), sg.InputText(key="pergunta", pad=(0, 10))],
            [sg.Text('Resposta:', font=('Montserrat', 16)), sg.InputText(key="resposta")],
            [sg.Button('Salvar', size=(12,1), pad=(0, 15)), sg.Button('Voltar', size=(12,1), pad=(20, 15), button_color=('white', 'gray'))]
        ]
        self.__window = sg.Window(
            "Criador de Pergunta", self.__container, font=("Montserrat", 14))
        return self.window
        
    def tela_editar_pergunta_resposta(self, pergunta: PerguntaResposta):
        self.__container = [
            [sg.Text('Editor de Perguntas e Respostas:', font=('Montserrat', 24, "bold"))],
            [sg.Text('Pergunta:', font=('Montserrat', 16)), sg.InputText(key="pergunta", default_text=pergunta.pergunta, pad=(0, 10))],
            [sg.Text('Resposta:', font=('Montserrat', 16)), sg.InputText(key="resposta", default_text=pergunta.resposta)],
            [sg.Button('Salvar', size=(12,1), pad=(0, 15)), sg.Button('Voltar', size=(12,1), pad=(20, 15), button_color=('white', 'gray'))]]
        
        self.__window = sg.Window(
            "Editor de Pergunta", self.__container, font=("Montserrat", 14))
        return self.window
        
    def tela_selecao_bot(self):
        self.__container = [
            [sg.Text('Por favor, selecione um bot para editar', font=('Montserrat', 24, "bold"))],
            [sg.Text('Bot:', font=('Montserrat', 16), pad=(0, 18)), sg.Combo(self.sistema.lista_bots, key="bot", size=(40, 1), readonly=True)],
            [sg.Button('Ok', size=(5,1)), sg.Button('Voltar', size=(6,1), pad=(6, 7), button_color=('white', 'gray'))]]
        self.__window = sg.Window(
            "Selecao de Bot", self.__container, font=("Montserrat", 14))
        return self.window
        
    def tela_edicao_bot(self, bot: Bot):
        self.__container = [
            [sg.Text('Editar Bot', font=('Montserrat', 24, "bold"))],
            [sg.Text('Por favor, altere os dados abaixo:', font=('Montserrat', 16))],
            [sg.Text('', size=(15, 1))],
            [sg.Text('Nome do bot:'), sg.Text('', size=(7, 1)), sg.InputText(key="nome", default_text=self.botmaker.valores_padrao["nome"])],
            [sg.Text('Apresentação do bot:'), sg.InputText(key="apresentacao", default_text=self.botmaker.valores_padrao["apresentacao"], size=(40, 1))],
            [sg.Text('Mensagem de boas vindas:'), sg.InputText(key="boas_vindas", default_text=self.botmaker.valores_padrao["boas_vindas"], size=(36, 1))],
            [sg.Text('Mensagem de despedida:'), sg.InputText(key="despedida", default_text=self.botmaker.valores_padrao["despedida"], size=(38, 1))],
            [sg.Text('Perguntas e respostas:'), sg.Combo(self.botmaker.perguntas_respostas, size=(30, 1), key="pergunta_resposta", readonly=True), sg.Button('Editar', size=(10, 1)), sg.Button('Novo', size=(10, 1))],
            [sg.Text('', size=(15, 1))],
            [sg.Button('Confirmar', size=(25, 1), pad=(5, 0)), sg.Button('Voltar', size=(25, 1), pad=(5, 0))],
        ]
        self.__window = sg.Window(
            "Editor de Bot", self.__container, font=("Montserrat", 14))
        return self.window
       

    
        