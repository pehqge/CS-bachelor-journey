class Regiao:
    def __init__(self, nome, votos):
        self.__nome = 'Regiao '+ nome
        self.__votos = votos
        self.__total = sum(votos.values())
    
    @property
    def nome(self):
        return self.__nome
    
    @property
    def votos(self):
        return self.__votos
    
    @property
    def total(self):
        return self.__total
    
    def atualiza_votos(self, votos):
        self.__votos = votos
        self.__total = sum(votos.values())
        
    def __eq__(self, str):
        if self.nome == str:
            return True
        return False