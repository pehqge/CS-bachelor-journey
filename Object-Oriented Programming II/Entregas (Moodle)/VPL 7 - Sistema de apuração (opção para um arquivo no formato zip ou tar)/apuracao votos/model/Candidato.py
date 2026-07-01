class Candidato:
    def __init__(self, nome):
        self.__nome = nome
        self.__votos_regiao = {}
        self.__total = 0

    @property
    def votos_regiao(self):
        return self.__votos_regiao

    @votos_regiao.setter
    def votos_regiao(self, votos_regiao):
        self.__votos_regiao = votos_regiao

    @property
    def nome(self):
        return self.__nome

    @property
    def total(self):
        return self.__total

    @total.setter
    def total(self, total):
        self.__total = total

    def computa_voto(self, nome_regiao, voto):
        try:
            self.votos_regiao[nome_regiao] = voto
            self.total += voto
        except KeyError:
            print("candidato não encontrado")
            
    def __eq__(self, str):
        if self.nome == str:
            return True
        else:
            return False
