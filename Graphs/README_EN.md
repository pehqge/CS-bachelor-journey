[<kbd><img title="Português" alt="Português" src="https://flagicons.lipis.dev/flags/4x3/br.svg" width="22"></kbd> Versão em português](README.md)

# INE5413 - Graphs

These are the assignments and code I wrote for the Graph Theory course. Three practical assignments in Python, each with its own PDF report inside its folder. I also kept a C++ exercise, my notes and the exam.

The code runs on top of my own graph library (classes `Grafo` and `Vertice`, plus the `auxiliar.py` module that reads `.net` files in Pajek format). Test graphs live in `pequenas` (A1) and `dirigidos` (A3).

## Assignments

| Assignment | Folder | Report | What I implemented |
|---|---|---|---|
| A1 | [Atividade A1](Atividade%20A1) | [Relatorio.pdf](Atividade%20A1/Relatorio.pdf) | Graph representation, breadth-first search (BFS), Eulerian cycle (Hierholzer), Dijkstra and Floyd-Warshall |
| A2 | [Atividade A2](Atividade%20A2) | [Relatorio.pdf](Atividade%20A2/Relatorio.pdf) | Strongly connected components (Kosaraju) and topological sort |
| A3 | [Atividade A3](Atividade%20A3) | [Relatorio.pdf](Atividade%20A3/Relatorio.pdf) | Maximum flow (Edmonds-Karp), bipartite matching (Hopcroft-Karp) and vertex coloring (Lawler) |

## Code details

| Item | Where | Description |
|---|---|---|
| A1 code | [Atividade A1/python](Atividade%20A1/python) | `A1_1` to `A1_5`: representation, BFS, Eulerian cycle, Dijkstra and Floyd-Warshall. Includes `min_heap.py` and `auxiliar.py`, C++ versions (`A1_1.cpp`, `A1_3.cpp`, `A1_4.cpp`) and the report text in [Atividade A1/README.md](Atividade%20A1/README.md) |
| A1 test graphs | [Atividade A1/pequenas](Atividade%20A1/pequenas) | Classic networks in Pajek format (karate, dolphins, lesmis, football, jazz and others) |
| A2 code | [Atividade A2/python](Atividade%20A2/python) | `A2_1` strongly connected components, `A2_2` topological sort |
| A3 code | [Atividade A3/python](Atividade%20A3/python) | `A3_1` Edmonds-Karp, `A3_2` Hopcroft-Karp, `A3_3` Lawler |
| A3 directed graphs | [Atividade A3/python/dirigidos](Atividade%20A3/python/dirigidos) | Directed test networks, including maps of SC cities |
| C++ exercise | [Exercícios](Exercícios) | `E_1.cpp` and the `grafo.txt` it reads |

## Study material

| Item | Where | Description |
|---|---|---|
| Notes | [Aulas/Anotações Grafos.pdf](Aulas/Anotações%20Grafos.pdf) | My course notes |
| Exam | [Provas/prova1.pdf](Provas/prova1.pdf) | First exam |
