from A1_1 import Grafo
import auxiliar

def hierholzer(grafo : Grafo):
    # cria lista C
    C = {frozenset(edge) : False for edge in grafo.arestas.keys()}
    
    # seleciona um vertice arbitrario v
    v = list(grafo.vertices.keys())[0]
    
    # executa a busca do ciclo
    (r, ciclo) = buscarSubcicloEuleriano(grafo, v, C)
    
    if not r or any(C[x] == False for x in C):
        print(0)  # nao eh euleriano
    else:
        print(1)  # eh euleriano
        print(",".join(ciclo))

    
def buscarSubcicloEuleriano(grafo: Grafo, v: str, C: dict) -> tuple:
    ciclo = [v]
    t = v

    while True:
        
       # Só prossegue se existir uma aresta não-visitada conectada a Ciclo.
       
       # if ∄u ∈ N(v) : C(v, u) = false then
        if not any(C[frozenset((v, u))] == False for u in grafo.vizinhos(v)):
            return (False, [])  

        else:
            # Selecionar uma aresta e ∈ E tal que C[e] = false
            for u in grafo.vizinhos(v):
                if not C[frozenset((v, u))]:
                    C[frozenset((v, u))] = True  
                    v = u
                    ciclo.append(v) 
                    break

            
            if v == t:
                break

   # foreach x ∈ {u ∈ Ciclo : ∃(u, w) ∈ {e ∈ E : C[e] = false}} do
    for x in ciclo:
       
        if any(not C[frozenset((x, w))] for w in grafo.vizinhos(x)):
            r, subciclo = buscarSubcicloEuleriano(grafo, x, C)
            if not r:
                return False, [] 
            
            # Substitui o x pelo subciclo
            ciclo = ciclo[:ciclo.index(x)] + subciclo + ciclo[ciclo.index(x) + 1:]

    return True, ciclo

if __name__ == '__main__':
    import sys
    arquivo = sys.argv[1]
    aux = auxiliar.Auxiliar(arquivo, ponderado = False)
    hierholzer(aux.grafo)