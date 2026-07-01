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

    int caso = 1;

    while (true) {
        int Z, I, M, L;
        cin >> Z >> I >> M >> L;

        if (Z == 0 && I == 0 && M == 0 && L == 0) break;

        unordered_map<int, int> visitado;
        int atual = L, contador = 0;

        while (visitado.find(atual) == visitado.end()) {
            visitado[atual] = contador++;
            atual = (Z * atual + I) % M;
        }

        cout << "Case " << caso++ << ": " << contador - visitado[atual] << "\n";
    }

    return 0;
}