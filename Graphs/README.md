[<kbd><img title="English" alt="English" src="https://flagicons.lipis.dev/flags/4x3/us.svg" width="22"></kbd> English version](README_EN.md)

# INE5413 - Grafos

Aqui estão os trabalhos e códigos que fiz na disciplina de Grafos. São três atividades práticas em Python, cada uma com seu relatório em PDF na própria pasta. Também guardei um exercício em C++, minhas anotações e a prova.

O código roda sobre uma biblioteca de grafos própria (classes `Grafo` e `Vertice`, mais o módulo `auxiliar.py` que lê arquivos `.net` no formato Pajek). Os grafos de teste ficam em `pequenas` (A1) e `dirigidos` (A3).

## Atividades

| Atividade | Pasta | Relatório | O que implementei |
|---|---|---|---|
| A1 | [Atividade A1](Atividade%20A1) | [Relatorio.pdf](Atividade%20A1/Relatorio.pdf) | Representação do grafo, busca em largura (BFS), ciclo euleriano (Hierholzer), Dijkstra e Floyd-Warshall |
| A2 | [Atividade A2](Atividade%20A2) | [Relatorio.pdf](Atividade%20A2/Relatorio.pdf) | Componentes fortemente conexas (Kosaraju) e ordenação topológica |
| A3 | [Atividade A3](Atividade%20A3) | [Relatorio.pdf](Atividade%20A3/Relatorio.pdf) | Fluxo máximo (Edmonds-Karp), emparelhamento bipartido (Hopcroft-Karp) e coloração de vértices (Lawler) |

## Detalhe dos códigos

| Item | Onde | Descrição |
|---|---|---|
| Código A1 | [Atividade A1/python](Atividade%20A1/python) | `A1_1` a `A1_5`: representação, BFS, ciclo euleriano, Dijkstra e Floyd-Warshall. Inclui `min_heap.py` e `auxiliar.py`, versões em C++ (`A1_1.cpp`, `A1_3.cpp`, `A1_4.cpp`) e o texto do relatório em [Atividade A1/README.md](Atividade%20A1/README.md) |
| Grafos de teste A1 | [Atividade A1/pequenas](Atividade%20A1/pequenas) | Redes clássicas em formato Pajek (karate, dolphins, lesmis, football, jazz e outras) |
| Código A2 | [Atividade A2/python](Atividade%20A2/python) | `A2_1` componentes fortemente conexas, `A2_2` ordenação topológica |
| Código A3 | [Atividade A3/python](Atividade%20A3/python) | `A3_1` Edmonds-Karp, `A3_2` Hopcroft-Karp, `A3_3` Lawler |
| Grafos dirigidos A3 | [Atividade A3/python/dirigidos](Atividade%20A3/python/dirigidos) | Redes dirigidas de teste, incluindo mapas de cidades de SC |
| Exercício em C++ | [Exercícios](Exercícios) | `E_1.cpp` e o `grafo.txt` que ele lê |

## Material de estudo

| Item | Onde | Descrição |
|---|---|---|
| Anotações | [Aulas/Anotações Grafos.pdf](Aulas/Anotações%20Grafos.pdf) | Minhas anotações da disciplina |
| Prova | [Provas/prova1.pdf](Provas/prova1.pdf) | Primeira prova |
