from auxiliar import GrafoNaoDirigido, Auxiliar
import sys

def lawler(grafo: GrafoNaoDirigido):
    n = len(grafo.vertices)
    vertices = list(grafo.vertices.keys()) 
    X = [float('inf')] * (1 << n) 
    X[0] = 0  
    coloracao = {}

    for s in range(1, 1 << n):  
        S = {vertices[i] for i in range(n) if (s & (1 << i))}  
        subgrafo = grafo.subgrafo(S)
        independentes = subgrafo.conjuntos_independentes()

        for I in independentes:
            i = sum(1 << vertices.index(v) for v in (S - I))  
            if X[i] + 1 < X[s]:
                X[s] = X[i] + 1
                coloracao[s] = (I, i)
                
    s = (1 << n) - 1
    cor_atual = 1
    cores = {}
    while s > 0:
        I, i = coloracao[s]
        for v in I:
            cores[v] = cor_atual
        cor_atual += 1
        s = i

    return X[(1 << n) - 1], cores


if __name__ == '__main__':
    arquivo = sys.argv[1]
    aux = Auxiliar(arquivo, type="naodirigido")

    numero_cromatico, cores = lawler(aux.grafo)

    print(numero_cromatico)

    cores_ordenadas = [str(cores[v]) for v in sorted(cores.keys())]
    print(", ".join(cores_ordenadas))