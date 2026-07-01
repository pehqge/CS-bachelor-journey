#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

int contaPontos(vector<pair<int, int>>& pontos) {
    int n = pontos.size();
    int contador = 0;

    for (int i = 0; i < n; ++i) {
        unordered_map<ll, int> frequenciaDistancia;
        for (int j = 0; j < n; ++j) {
            if (i == j) continue;
            ll dx = pontos[j].first - pontos[i].first;
            ll dy = pontos[j].second - pontos[i].second;
            ll distanciaQuadrada = dx * dx + dy * dy;
            frequenciaDistancia[distanciaQuadrada]++;
        }
        for (const auto& [_, frequencia] : frequenciaDistancia) {
            contador += frequencia * (frequencia - 1) / 2;
        }
    }

    return contador;
}

int main() {
    fastIO();

    while (true) {
        int n;
        cin >> n;
        if (n == 0) break;

        vector<pair<int, int>> pontos(n);
        for (int i = 0; i < n; ++i) {
            cin >> pontos[i].first >> pontos[i].second;
        }

        cout << contaPontos(pontos) << "\n";
    }

    return 0;
}