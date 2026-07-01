from Bots.PerguntaResposta import PerguntaResposta


class Chat:
    def __init__(self):
        self.__bot = None
        self.__mensagem = ''
        
    @property
    def mensagem(self):
        return self.__mensagem
    

    @mensagem.setter
    def mensagem(self, mensagem):
        self.__mensagem = mensagem

    @property
    def bot(self):
        return self.__bot
    
    @bot.setter
    def bot(self, bot):
        self.__bot = bot

    def boas_vindas(self):
        return f"{self.bot.nome}: {self.bot.boas_vindas}"

    def despedida(self):
        return f"{self.bot.nome}: {self.bot.despedida}"
    
    def mostrar_pergunta_resposta(self, pergunta):
        return f"Usuário: {pergunta}\n\nBot {self.bot.nome}: {pergunta.resposta}\n\n"
    
    def clean(self):
        self.mensagem = ''
        self.bot = None
    
    # fim