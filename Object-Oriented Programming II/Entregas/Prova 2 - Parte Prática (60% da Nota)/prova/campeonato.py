from equipe import Equipe
from grupo import Grupo
from jogo import Jogo

class Campeonato:
    def __init__(self, nome: str):
        self.__nome = nome
        self.__equipes = []
        self.__grupos = []
        self.__jogos = []

    def adicionar_equipe(self, nome: str, treinador: str):
        try:
            self.__equipes.append(Equipe(nome, treinador))
        except ValueError:
            print("Nome e treinador precisam ser strings")

    def criar_grupo(self, nome: str):
        try:
            self.__grupos.append(Grupo(nome))
        except ValueError:
            print("O nome do grupo precisa ser uma string")

    def atribuir_equipe(self, equipe: str, grupo: str):
        try:
            equipe_sistema = [equipe_s for equipe_s in self.__equipes if equipe_s.nome == equipe][0]

            grupo_sistema = [grupo_s for grupo_s in self.__grupos if grupo_s.nome == grupo][0]

            grupo_sistema.atribuir_equipe(equipe_sistema)
        except IndexError:
            print("Grupo ou Equipe não cadastrada, tente outra.")


    # fiz o sistema de partida assim, para que a função não tenha que receber uma string com o resultado, e sim o jogo já fala por si mesmo
    def criar_partida(self, equipe1, gol1, equipe2, gol2):
        try:
            equipe_sistema1 = [equipe_s for equipe_s in self.__equipes if equipe_s.nome == equipe1][0]
            equipe_sistema2 = [equipe_s for equipe_s in self.__equipes if equipe_s.nome == equipe2][0]

            self.__jogos.append(Jogo(equipe_sistema1, gol1, equipe_sistema2, gol2))

        except IndexError:
            print("Equipe não cadastrada, tente outra.")



    def mostrar_equipes_grupo(self, grupo: str):
        try:
            grupo_sistema = [grupo_s for grupo_s in self.__grupos if grupo_s.nome == grupo][0]

            print(f"Equipes do {grupo}: {', '.join([equipe.nome for equipe in grupo_sistema.lista_equipe])}")

        except IndexError:
            print("Grupo não cadastrado, tente outro.")


    def mostrar_classificacao_grupo(self, grupo: str):
        try: 
            grupo_sistema = [grupo_s for grupo_s in self.__grupos if grupo_s.nome == grupo][0]

            ordenada = sorted(grupo_sistema.lista_equipe, key=lambda x: x.pontos, reverse=True)

            print(f"Classificação {grupo}:")
            lugar = 1
            for equipe in ordenada:
                print(f"{lugar}o Lugar: {equipe.nome} com {equipe.pontos} pontos")
                lugar +=1

        except IndexError:
            print("Grupo ou Equipe não cadastrada, tente outra.")
