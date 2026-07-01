#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

vector<ll> gerarFibonacci(ll limite) {
    vector<ll> fibonacci = {1, 2};
    while (true) {
        ll prox = fibonacci[fibonacci.size() - 1] + fibonacci[fibonacci.size() - 2];
        if (prox > limite) break;
        fibonacci.push_back(prox);
    }
    return fibonacci;
}

int main() {
    fastIO();

    ll t;
    cin >> t;

    vector<ll> fibonacci = gerarFibonacci(INT_MAX);

    while (t--) {
        ll n;
        cin >> n;

        vector<ll> indices(n);
        for (int i = 0; i < n; ++i) {
            cin >> indices[i];
        }

        string cifrado;
        cin.ignore();
        getline(cin, cifrado);

        unordered_map<ll, char> mapa;
        int posicao = 0;

        for (char c : cifrado) {
            if (isupper(c)) {
                mapa[indices[posicao++]] = c;
                if (posicao == n) break;
            }
        }

        string resultado(fibonacci.size(), ' ');
        for (int i = 0; i < fibonacci.size(); ++i) {
            if (mapa.count(fibonacci[i])) {
                resultado[i] = mapa[fibonacci[i]];
            }
        }

        while (!resultado.empty() && resultado.back() == ' ') {
            resultado.pop_back();
        }

        cout << resultado << "\n";
    }

    return 0;
}