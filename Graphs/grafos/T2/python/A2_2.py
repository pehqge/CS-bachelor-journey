
import sys
from auxiliar import *

def ord_topologica(grafo : Grafo) -> list:
    # Input : Grafo dirigido g=(V,E)

    # Vértices começam com atributo
    #   v.acessado = false

    # o ← < >
    o = list()

    # foreach u ∈ V do
    for u in grafo.vertices:
        # if Cu = false then
        if not u.visitado:
          visita(grafo, u, o)  

    return o

def visita(grafo : Grafo, v : Vertice, o : list) -> None:
   
   # Cv ← true
    v.acessado =  True

   # foreach u ∈ N+(v) do
    for u in v.vizinhos:
      # if Cu = false then
      if not u.acessado:
         visita(grafo, u, o)
    
    o.insert(0, v)
