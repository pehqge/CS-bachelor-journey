#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

int t, n;
vector<int> numeros;
set<vector<int>> resultados;
vector<int> atual;

void backtrack(int idx, int soma) {
    if (soma == t) {
        resultados.insert(atual);
        return;
    }
    int anterior = -1;
    for (int i = idx; i < n; ++i) {
        if (soma + numeros[i] <= t && numeros[i] != anterior) {
            int count_total = count(numeros.begin(), numeros.end(), numeros[i]);
            int count_atual = count(atual.begin(), atual.end(), numeros[i]);
            if (count_atual < count_total) {
                atual.push_back(numeros[i]);
                backtrack(i + 1, soma + numeros[i]);
                atual.pop_back();
                anterior = numeros[i];
            }
        }
    }
}

bool compara(const vector<int>& a, const vector<int>& b) {
    for (size_t i = 0; i < min(a.size(), b.size()); ++i) {
        if (a[i] != b[i])
            return a[i] > b[i];
    }
    return a.size() > b.size();
}

int main() {
    fastIO();

    string linha;
    while (getline(cin, linha)) {
        stringstream ss(linha);
        ss >> t >> n;
        if (n == 0) break;

        numeros.clear();
        int num;
        while (ss >> num) {
            numeros.push_back(num);
        }

        sort(all(numeros), greater<int>());
        n = numeros.size();
        resultados.clear();
        atual.clear();

        cout << "Sums of " << t << ":\n";
        backtrack(0, 0);

        if (resultados.empty()) {
            cout << "NONE\n";
        } else {
            vector<vector<int>> vec_resultados(resultados.begin(), resultados.end());
            sort(vec_resultados.begin(), vec_resultados.end(), compara);

            for (const auto& res : vec_resultados) {
                for (size_t i = 0; i < res.size(); ++i) {
                    if (i > 0) cout << "+";
                    cout << res[i];
                }
                cout << "\n";
            }
        }
    }

    return 0;
}