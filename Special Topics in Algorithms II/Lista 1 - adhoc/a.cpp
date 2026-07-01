#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

int main() {
    fastIO();

    int l, c;
    cin >> l >> c;

    vector<string> matriz(l);

    for (int i = 0; i < l; ++i) {
        cin >> matriz[i];
    }

    int n;
    cin >> n;

    vector<string> palavras(n);
    vector<vector<int>> contagem_palavras(n, vector<int>(26, 0));

    for (int i = 0; i < n; ++i) {
        cin >> palavras[i];
        for (char letra : palavras[i]) {
            contagem_palavras[i][letra - 'A']++;
        }
    }

    vector<vector<int>> mascaras_celulas(l, vector<int>(c, 0));
    int direcoes[4][2] = {{0, 1}, {1, 0}, {1, 1}, {1, -1}}; // Direita, Baixo, Diagonal Direita, Diagonal Esquerda

    for (int p = 0; p < n; ++p) {
        int tamanho = palavras[p].size();
        vector<int> contagem_palavra = contagem_palavras[p];

        for (int i = 0; i < l; ++i) {
            for (int j = 0; j < c; ++j) {
                for (int d = 0; d < 4; ++d) {
                    int x = i, y = j;
                    vector<int> contagem_sequencia(26, 0);
                    vector<pair<int, int>> posicoes;

                    bool valido = true;
                    for (int k = 0; k < tamanho; ++k) {
                        if (x < 0 || x >= l || y < 0 || y >= c) {
                            valido = false;
                            break;
                        }
                        contagem_sequencia[matriz[x][y] - 'A']++;
                        posicoes.push_back({x, y});
                        x += direcoes[d][0];
                        y += direcoes[d][1];
                    }
                    if (!valido)
                        continue;

                    if (contagem_sequencia == contagem_palavra) {
                        for (auto& pos : posicoes) {
                            int xi = pos.first;
                            int yi = pos.second;
                            mascaras_celulas[xi][yi] |= (1 << p);
                        }
                    }
                }
            }
        }
    }

    int especiais = 0;

    for (int i = 0; i < l; ++i) {
        for (int j = 0; j < c; ++j) {
            int contador = __builtin_popcount(mascaras_celulas[i][j]);
            if (contador >= 2) {
                especiais++;
            }
        }
    }

    cout << especiais << "\n";

    return 0;
}