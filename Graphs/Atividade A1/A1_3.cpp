#include <iostream>
#include <vector>
#include <tuple>
#include <unordered_map>
#include <utility> // para usar std::pair
#include "A1_1.cpp"

using namespace std;

template<typename T>
// Função hash personalizada para pair<int, int> para usar no unordered_map
/*
unordered_map é uma espécie de dicinário, e nele estamos utilizando chaves em formato de tupla para representar
a ligação entre os vértice, por exemplo: arestas_visitadas[vertice1, vertic2] = valor

*/
struct hash_pair {
    template <class T1, class T2>
    size_t operator() (const pair<T1, T2>& p) const {
        auto hash1 = hash<T1>{}(p.first);
        auto hash2 = hash<T2>{}(p.second);
        return hash1 ^ hash2; // combinação dos dois hashes
    }
};
template<typename T>
// Busca um subciclo euleriano a partir do vértice 'vertice'
tuple<bool, vector<int>> buscaSubcicloEuleriano(Grafo<T>& grafo, int vertice, unordered_map<pair<int, int>, bool, hash_pair> &arestas_visitadas) {
    vector<int> ciclo; 
    ciclo.push_back(vertice); // iniciamos o ciclo com o vértice inicial
    
    int t = vertice;  // variável auxiliar

    while (true) {
        vector<int> vizinhos; // armazenar os vizinhos que ainda têm arestas não visitadas
        
        // Encontrar os vizinhos que têm arestas não visitadas
        for (const auto& adj : grafo.vizinhos(vertice)) {
            pair<int, int> aresta1 = {vertice, adj};
            pair<int, int> aresta2 = {adj, vertice}; // como o grafo é não-dirigido, consideramos ambos os sentidos
            
            // Se a aresta ainda não foi visitada em nenhum dos dois sentidos
            if (!arestas_visitadas[aresta1] && !arestas_visitadas[aresta2]) {
                vizinhos.push_back(adj); 
            }
        }

        // Verificar se não há mais vizinhos com arestas não visitadas
        if (vizinhos.empty()) {
            return {false, {}}; // Não há ciclo euleriano partindo desse vértice
        } else {
            // Seleciona um vizinho e marca a aresta como visitada
            int u = vizinhos.back(); // seleciona o último vizinho disponível
            vizinhos.pop_back(); // remove o vizinho selecionado
            
            arestas_visitadas[{vertice, u}] = true; // marca a aresta como visitada
            arestas_visitadas[{u, vertice}] = true; // para ambos os sentidos (não-dirigido)
            
            vertice = u; // move para o próximo vértice
            ciclo.push_back(vertice); // adiciona o vértice ao ciclo
        }

        // Se voltamos ao vértice inicial, encerramos o ciclo
        if (vertice == t) {
            break;
        }
    }

    // Verifica se há vértices no ciclo com arestas não-visitadas
    for (const auto& v : ciclo) {
        vector<int> vizinhos_nao_visitados; 
        for (const auto& x : grafo.vizinhos(v)) {
            if (!arestas_visitadas[{v, x}]) { // verificando a aresta não visitada
                vizinhos_nao_visitados.push_back(x);
            }
        }

        if (!vizinhos_nao_visitados.empty()) {
            auto [r, subciclo] = buscaSubcicloEuleriano(grafo, v, arestas_visitadas); // busca novo subciclo a partir de x
            if (!r) {
                return {false, {}}; // falha ao encontrar subciclo
            } else {
                // Insere o subciclo no ciclo principal
                auto it = find(ciclo.begin(), ciclo.end(), v);
                ciclo.insert(it, subciclo.begin(), subciclo.end());
            }
        }
    }

    return {true, ciclo}; // Retorna o ciclo encontrado
} // end function
template<typename T>
tuple<bool, vector<int>> hierholzer(Grafo<T>& grafo) {
    unordered_map<pair<int, int>, bool, hash_pair> arestas_visitadas; // Mapa (dicionario) para arestas visitadas

    for (const auto& aresta : grafo.adjacencias) { // verificae esse loop depois
        for (const auto& vertice: aresta) {
            arestas_visitadas[{a, vertice.first}] = false;
        } // end for
    } // end for

    int v = 1; //seleciona um vértice qualquer que esteja conectado a uma aresta
    auto [r,ciclo] = buscaSubcicloEuleriano(grafo, v, arestas_visitadas);
    if (!r) {
        return {false, {}};
    }

    // verifica se todas as arestas foram visitadas
    for (const auto& e: arestas_visitadas) {
        if (!e.second) {
            return {false, {}};
        } // end if
    } // end for

    return {true, ciclo};

} // end hierholzer

