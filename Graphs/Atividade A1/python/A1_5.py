

from A1_1 import Grafo, Vertice
from auxiliar import Auxiliar

def floyd_warshal(grafo : Grafo) -> tuple:
    # Sejam d e p matrizes de ordem grafo.qtdVertices() x grafo.qtdVertices()
    d = [[0 for _ in range(grafo.qtdVertices())] for _ in range(grafo.qtdVertices())] # d[u][v] = distancia entre u e v
    p = [[None for _ in range(grafo.qtdVertices())] for _ in range(grafo.qtdVertices())] # p[u][v] = vertice anterior a v no caminho de u a v

    # Mapear rótulos para índices
    rotulo_para_indice = {rotulo: idx for idx, rotulo in enumerate(grafo.vertices.keys())}

    # foreach u ∈ V do
    #   foreach v ∈ V do
    for u in grafo.vertices.values():
        for v in grafo.vertices.values():

            # Converter rótulos para índices
            u_idx = rotulo_para_indice[u.rotulo]
            v_idx = rotulo_para_indice[v.rotulo]

            # if u = v then
            if u == v:
                # d[u][v] ← 0
                # p[u][v] ← null
                d[u_idx][v_idx] = 0
                p[u_idx][v_idx] = None
            # else
            #  if (u, v) ∈ E then
            #   d[u][v] ← w(u, v)
            #   p[u][v] ← u
            else:
                if grafo.haAresta(u.rotulo, v.rotulo):
                    d[u_idx][v_idx] = grafo.peso(u.rotulo, v.rotulo)
                    p[u_idx][v_idx] = u_idx
                # else
                #   d[u][v] ← ∞
                #   p[u][v] ← null
                else:
                    d[u_idx][v_idx] = float('inf')
                    p[u_idx][v_idx] = None
    
    # foreach k ∈ V do
    #  foreach u ∈ V do
    #   foreach v ∈ V do
    for k in grafo.vertices.values():
        for u in grafo.vertices.values():
            for v in grafo.vertices.values():

                # Converter rótulos para índices
                k_idx = rotulo_para_indice[k.rotulo]
                u_idx = rotulo_para_indice[u.rotulo]
                v_idx = rotulo_para_indice[v.rotulo]

                # if d[u][v] > d[u][k] + d[k][v] then
                if d[u_idx][v_idx] > d[u_idx][k_idx] + d[k_idx][v_idx]:
                    # d[u][v] ← d[u][k] + d[k][v]
                    d[u_idx][v_idx] = d[u_idx][k_idx] + d[k_idx][v_idx]
                    # p[u][v] ← p[k][v]
                    p[u_idx][v_idx] = p[k_idx][v_idx]
    
    return d, p
                

def exibir(grafo : Grafo, d : list, p : list):
    """
    mostrar as distancias para cada par de vertices na tela
    utilizando o formato do exemplo abaixo. Na saıda, cada linha tera as distancias para vertice na ordem crescente
    dos ındices informados no arquivo de entrada.
    1:0,10,3,5
    2:10,0,9,8
    3:3,9,0,11
    4:5,8,11,0
    """

    # Mapear índices para rótulos
    rotulo_para_indice = {str(rotulo): idx for idx, rotulo in enumerate(grafo.vertices.keys())}
    indice_para_rotulo = {idx: str(rotulo) for rotulo, idx in rotulo_para_indice.items()}
    
    for u_idx in range(len(grafo.vertices)):
        linha = f"{indice_para_rotulo[u_idx]}:"
        for v_idx in range(len(grafo.vertices)):
            linha += f"{int(d[u_idx][v_idx])},"
        print(linha[:-1])

if __name__ == '__main__':
    import sys
    arquivo = sys.argv[1]
    aux = Auxiliar(arquivo, ponderado = True)
    d, p = floyd_warshal(aux.grafo)
    exibir(aux.grafo, d, p)
