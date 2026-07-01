

import sys
from A1_1 import Grafo

class Auxiliar:
    def __init__(self, arquivo : str, ponderado : bool = False) -> None:
        self.arquivo = arquivo

        # Atributos do grafo
        self.ponderado = ponderado
        self.vertices = []
        self.arestas = []

        # Cria o grafo da representação
        self.grafo = Grafo()

        self.ler()

    def ler(self) -> None:
        with open(self.arquivo, 'r') as net:

            # Acessa linhas do arquivo .net
            linhas = net.readlines()

            # Preenche dados do grafo de acordo com padrão adotado na disciplina

            # 1 - Num. de vértices está na primeira linha, após a palavra "*vertices"
                # Exemplo: *vertices 4 -> ["*vertices", "4"]
            linha_tmp = linhas[0].strip().split(' ')[1]

            num_vertices = int(linha_tmp)

            # 2 - Os rótulos dos vértices estão nas linhas seguintes
            linhas_rotulos = linhas[1:num_vertices + 1]

            # 3 - As arestas começam após num_vertices + 1 linhas + 1 linha marcando "*edges"
            linhas_arestas = [linha for linha in linhas[1 + num_vertices + 1:] if linha != "\n"]

            # Preenche vértices do grafo
            for linha in linhas_rotulos:
                rotulo = linha.strip().split(' ')[0]
                self.grafo.cria_vertice(rotulo)

            # Preenche arestas do grafo
            for linha in linhas_arestas:
                u, v, peso = linha.strip().split(' ')
                self.grafo.cria_aresta(u, v, float(peso))
            
        
if __name__ == '__main__':
    arquivo = sys.argv[1]
    aux = Auxiliar(arquivo, ponderado = False)
    