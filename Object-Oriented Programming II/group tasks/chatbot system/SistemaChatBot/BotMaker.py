from Bots.Bot import Bot
from Bots.PerguntaResposta import PerguntaResposta
from SistemaChatBot import SistemaChatBot as scb

class BotMaker:
    def __init__(self, sistema: scb):
        self.__sistema = sistema
        self.__perguntas_respostas = []
        self.__valores_padrao = {"nome": "", "apresentacao": "", "boas_vindas": "", "despedida": "", "pergunta_resposta": ""}
        self.__bot = None
    
    @property
    def sistema(self):
        return self.__sistema
    
    @property
    def bot(self):
        return self.__bot
    
    @property
    def perguntas_respostas(self):
        return self.__perguntas_respostas

    @property
    def valores_padrao(self):
        return self.__valores_padrao
    
    @valores_padrao.setter
    def valores_padrao(self, valores_padrao):
        self.__valores_padrao = valores_padrao
        
    @bot.setter
    def bot(self, bot):
        self.__bot = bot
        
    def selecionar_bot(self, bot: Bot):
        self.__bot = bot
        self.__perguntas_respostas = bot.perguntas_respostas
        self.__valores_padrao = {"nome": bot.nome, "apresentacao": bot.apresentacao, "boas_vindas": bot.boas_vindas, "despedida": bot.despedida}

    def add_pergunta_resposta(self, pergunta, resposta):
        self.__perguntas_respostas.append(PerguntaResposta(pergunta, resposta))
        
    def remove_pergunta_resposta(self, pergunta_resposta: PerguntaResposta):
        if pergunta_resposta in self.__perguntas_respostas:
            self.__perguntas_respostas.remove(pergunta_resposta)
        else:
            raise ValueError("Não é uma pergunta e resposta válida ou não está na lista de perguntas e respostas")
        
    def editar_pergunta_resposta(self, pergunta_resposta: PerguntaResposta, pergunta_nova: str, resposta_nova: str):
        pergunta_resposta.pergunta = pergunta_nova
        pergunta_resposta.resposta = resposta_nova
        
    def cria_bot(self, nome, apresentacao, boas_vindas, despedida):
        if nome in [bot.nome for bot in self.sistema.lista_bots]:
            raise ValueError("Já existe um bot com esse nome")
        elif nome == "" or apresentacao == "" or boas_vindas == "" or despedida == "" or self.__perguntas_respostas == []:
            raise ValueError("Por favor, preencha todos os dados do bot")
        else:
            self.sistema.addbot(Bot(nome, apresentacao, boas_vindas, despedida, self.__perguntas_respostas))
            self.clean()
    
    def remove_bot(self, bot: Bot):
        if bot in self.sistema.lista_bots:
            self.sistema.removebot(bot)
        else:
            raise ValueError("Não é um bot válido ou não está na lista de bots")
        
    def editar_bot(self, nome_novo: str, apresentacao_nova: str, boas_vindas_nova: str, despedida_nova: str):
        if not nome_novo in [bot.nome for bot in self.sistema.lista_bots if bot.nome != self.__bot.nome]:
            self.__bot.nome = nome_novo
            self.__bot.apresentacao = apresentacao_nova
            self.__bot.boas_vindas = boas_vindas_nova
            self.__bot.despedida = despedida_nova
            self.__bot.perguntas_respostas = self.perguntas_respostas
            self.sistema.editbot(self.__bot)
        else:
            raise ValueError("Já existe um bot com este nome. Por favor, escolha outro nome")
        
    def clean(self):
        self.__perguntas_respostas = []
        self.__bot = None
        self.__valores_padrao = {"nome": "", "apresentacao": "", "boas_vindas": "", "despedida": "", "pergunta_resposta": ""}