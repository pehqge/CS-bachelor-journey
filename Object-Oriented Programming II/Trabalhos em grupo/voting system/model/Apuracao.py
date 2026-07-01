import os
import json
from model.Candidato import Candidato
from model.Regiao import Regiao
import matplotlib.pyplot as plt


class Apuracao:
    def __init__(self):
        self.__regioes = []
        self.__candidatos = []
        self.__total = 0

    # funcao que le os arquivos json e cria as regioes

    def computa_regioes(self, path_pasta):
        arquivos = sorted([arquivo for arquivo in os.listdir(
            path_pasta) if arquivo.endswith('.json')]) # lista de arquivos json

        for arquivo in arquivos:
            with open(os.path.join(path_pasta, arquivo), 'r') as f:  # abre o arquivo
                votos = json.load(f) # carrega o dicionario de votos em "votos"
                # se a regiao nao estiver na lista de regioes
                if not "Regiao "+arquivo[:-5] in self.__regioes:
                    # cria uma nova regiao
                    self.__regioes.append(Regiao(arquivo[:-5], votos))
                else:
                    # atualiza os votos da regiao existente
                    self.__regioes[self.__regioes.index("Regiao " + arquivo[:-5])].atualiza_votos(votos)
        self.computa_candidatos()

    # funcao que cria os candidatos e computa os votos de cada um pelas regioes existentes
    def computa_candidatos(self):
        for regiao in self.__regioes:
            self.__total += regiao.total
            for candidato, voto in regiao.votos.items():
                try:
                    self.__candidatos[self.__candidatos.index(
                        candidato)].computa_voto(regiao.nome, voto)  # computa o voto do candidato se caso ele já estiver na região
                except ValueError: # caso ele não exista ainda, cria um novo candidato e computa os votos dele
                    cand_temp = Candidato(candidato)
                    self.__candidatos.append(cand_temp)
                    cand_temp.computa_voto(regiao.nome, voto)
        
    def plotar_grafico_bar_candidatos(self):
        candidatos = []
        votos = []

        for candidato in self.candidatos:
            candidatos.append(candidato.nome)
            votos.append(candidato.total)

        plt.figure(figsize=(15,6))
        plt.bar(candidatos, votos, color="blue")
        plt.title("Resultado da eleição")
        plt.xlabel("Candidato")
        plt.ylabel("Nº de Votos")

        plt.show()
    
    def plotar_grafico_pie_candidatos(self):
        candidatos = []
        votos = []

        for candidato in self.candidatos:
            candidatos.append(candidato.nome)
            votos.append(candidato.total)
        
        plt.pie(votos, labels=candidatos, autopct='%1.1f%%')
        plt.title('Distribuição de Votos por Candidato')

        plt.show()

    def plotar_grafico_bar_regioes(self):
        regioes = []
        votos = []

        for regiao in self.regioes:
            regioes.append(regiao.nome)
            votos.append(regiao.total)

        plt.figure(figsize=(15,6))
        plt.bar(regioes, votos, color="blue")
        plt.title("Relação Região / Nº de Votos")
        plt.xlabel("Região")
        plt.ylabel("Nº de Votos")

        plt.show()

    def plotar_grafico_pie_regioes(self):
        regioes = []
        votos = []

        for regiao in self.regioes:
            regioes.append(regiao.nome)
            votos.append(regiao.total)
        
        plt.pie(votos, labels=regioes, autopct='%1.1f%%')
        plt.title('Distribuição de Votos por Região')

        plt.show()
                    
    def reset(self):
        self.__candidatos = []
        self.__regioes = []

    @property
    def candidatos(self):
        return self.__candidatos

    @property
    def regioes(self):
        return self.__regioes
    
    @property
    def total(self):
        return self.__total

