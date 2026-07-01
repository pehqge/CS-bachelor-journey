#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

struct Peca {
    int esquerda, direita;
};

int n, m;
Peca inicio, fim;
vector<Peca> pecas;
vector<bool> usadas;
bool possivel;

void backtrack(int profundidade, int ultimo) {
    if (possivel) return;
    if (profundidade == n) {
        if (ultimo == fim.esquerda) {
            possivel = true;
        }
        return;
    }
    for (int i = 0; i < m; ++i) {
        if (!usadas[i]) {
            usadas[i] = true;
            if (pecas[i].esquerda == ultimo) {
                backtrack(profundidade + 1, pecas[i].direita);
            } else if (pecas[i].direita == ultimo) {
                backtrack(profundidade + 1, pecas[i].esquerda);
            }
            usadas[i] = false;
        }
    }
}

int main() {
    fastIO();

    while (cin >> n && n) {
        cin >> m;
        cin >> inicio.esquerda >> inicio.direita;
        cin >> fim.esquerda >> fim.direita;

        pecas.resize(m);
        usadas.assign(m, false);

        for (int i = 0; i < m; ++i) {
            cin >> pecas[i].esquerda >> pecas[i].direita;
        }

        possivel = false;
        backtrack(0, inicio.direita);

        if (possivel) {
            cout << "YES\n";
        } else {
            cout << "NO\n";
        }
    }

    return 0;
}