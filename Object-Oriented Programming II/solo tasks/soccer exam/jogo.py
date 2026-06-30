class Jogo:
    def __init__(self, equipe1, gols1, equipe2, gols2):
        self.__equipe1 = [equipe1, gols1]
        self.__equipe2 = [equipe2, gols2]
        self.calcula_resultado()

    def calcula_resultado(self):
        if self.__equipe1[1] > self.__equipe2[1]: # vitoria equipe 1
            self.__equipe1[0].pontos += 3
        elif self.__equipe2[1] > self.__equipe1[1]: # vitoria equipe 2
            self.__equipe2[0].pontos += 3
        else: # empate
            self.__equipe1[0].pontos += 1
            self.__equipe2[0].pontos += 1