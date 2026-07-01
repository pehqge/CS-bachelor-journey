class PerguntaResposta:
    def __init__(self, pergunta: str, resposta: str):
        self.__pergunta = pergunta
        self.__resposta = resposta
    
    @property
    def pergunta(self):
        return self.__pergunta
    
    @property
    def resposta(self):
        return self.__resposta
    
    @pergunta.setter
    def pergunta(self, pergunta):
        self.__pergunta = pergunta
    
    @resposta.setter
    def resposta(self, resposta):
        self.__resposta = resposta
    
    def __str__(self):
        return self.pergunta