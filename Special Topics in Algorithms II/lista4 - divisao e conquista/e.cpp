#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

int n, m;
vector<int> vasos;

bool check(ll capacidade_maxima) {
    int cont_containers = 1;
    ll soma = 0;
    for (int i = 0; i < n; ++i) {
        if (vasos[i] > capacidade_maxima)
            return false;
        if (soma + vasos[i] > capacidade_maxima) {
            cont_containers++;
            soma = vasos[i];
        } else {
            soma += vasos[i];
        }
    }
    return cont_containers <= m;
}

int main() {
    fastIO();

    while (cin >> n >> m) {
        vasos.resize(n);
        int max_vaso = 0;
        ll soma_vasos = 0;
        for (int i = 0; i < n; ++i) {
            cin >> vasos[i];
            max_vaso = max(max_vaso, vasos[i]);
            soma_vasos += vasos[i];
        }

        ll low = max_vaso;
        ll high = soma_vasos;

        ll resposta = high;

        while (low <= high) {
            ll mid = low + (high - low) / 2;
            if (check(mid)) {
                resposta = mid;
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }

        cout << resposta << "\n";
    }

    return 0;
}