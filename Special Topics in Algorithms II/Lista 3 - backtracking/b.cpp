#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

struct Restricao {
    int a, b, c;
};

int main() {
    fastIO();

    int n, m;

    while (cin >> n >> m && (n || m)) {
        vector<Restricao> restricoes(m);

        for (int i = 0; i < m; ++i) {
            cin >> restricoes[i].a >> restricoes[i].b >> restricoes[i].c;
        }

        vector<int> pessoas(n);
        for (int i = 0; i < n; ++i) {
            pessoas[i] = i;
        }

        int contador = 0;

        do {
            bool valido = true;
            for (const auto& r : restricoes) {
                int pos_a = find(all(pessoas), r.a) - pessoas.begin();
                int pos_b = find(all(pessoas), r.b) - pessoas.begin();
                int distancia = abs(pos_a - pos_b);

                if (r.c > 0) {
                    if (distancia > r.c) {
                        valido = false;
                        break;
                    }
                } else {
                    if (distancia < -r.c) {
                        valido = false;
                        break;
                    }
                }
            }
            if (valido) {
                contador++;
            }
        } while (next_permutation(all(pessoas)));

        cout << contador << "\n";
    }

    return 0;
}