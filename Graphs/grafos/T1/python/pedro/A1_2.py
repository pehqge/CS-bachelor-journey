from A1_1 import Grafo

def busca_largura(grafo : Grafo, s : int) -> list:
    # cria listas C (conhecidos), D (distancia), A (antecessor)
    C = {v : False for v in grafo.vertices.keys()}
    D = {v : float('inf') for v in grafo.vertices.keys()}
    A = {v : None for v in grafo.vertices.keys()}
    
    distancias = {0 : [s]}
    
    # configura vertice de origem
    C[s] = True
    D[s] = 0
    
    # cria fila Q
    Q = [s]
    
    while Q:
        u = Q.pop(0)
        
        for v in grafo.vizinhos(u):
            if not C[v]:
                C[v] = True
                D[v] = D[u] + 1
                A[v] = u
                Q.append(v)
                
                if D[v] not in distancias:
                    distancias[D[v]] = [v]
                else:
                    distancias[D[v]].append(v)

    return distancias

def main():
    import sys
    grafo = Grafo(sys.argv[1])
    
    distancia = busca_largura(grafo, int(sys.argv[2]))
    
    for key in sorted(distancia.keys()):
        print(f"{key}: {','.join(str(d) for d in distancia[key])}")
    
    
if __name__ == '__main__':
    main()