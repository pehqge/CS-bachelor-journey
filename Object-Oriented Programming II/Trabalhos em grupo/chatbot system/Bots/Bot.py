class Bot:
    def __init__(self, nome, apresentacao, boas_vindas, despedida, perguntas_respostas):
        self.__nome = nome
        self.__perguntas_respostas = perguntas_respostas
        self.__apresentacao = apresentacao
        self.__boas_vindas = boas_vindas
        self.__despedida = despedida

    @property
    def perguntas_respostas(self):
        return self.__perguntas_respostas
    
    @perguntas_respostas.setter
    def perguntas_respostas(self, perguntas_respostas):
        self.__perguntas_respostas = perguntas_respostas
            
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def despedida(self):
        return self.__despedida
    
    @despedida.setter
    def despedida(self, despedida):
        self.__despedida = despedida

    @property
    def apresentacao(self):
        return self.__apresentacao
    
    @apresentacao.setter
    def apresentacao(self, apresentacao):
        self.__apresentacao = apresentacao
    
    @property
    def boas_vindas(self):
        return self.__boas_vindas

    @boas_vindas.setter
    def boas_vindas(self, boas_vindas):
        self.__boas_vindas = boas_vindas
        
    def __str__(self):
        return f'{self.nome}: "{self.apresentacao}"'