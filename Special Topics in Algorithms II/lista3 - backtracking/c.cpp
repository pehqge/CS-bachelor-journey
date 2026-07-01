#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

int t, n, p;
vector<int> barras;
bool possivel;

void backtrack(int idx, int soma) {
    if (soma == n) {
        possivel = true;
        return;
    }
    if (soma > n || idx == p || possivel) {
        return;
    }
    backtrack(idx + 1, soma + barras[idx]);
    backtrack(idx + 1, soma);
}

int main() {
    fastIO();

    cin >> t;

    while (t--) {
        cin >> n;
        cin >> p;

        barras.resize(p);
        for (int i = 0; i < p; ++i) {
            cin >> barras[i];
        }

        possivel = false;
        backtrack(0, 0);

        if (possivel) {
            cout << "YES\n";
        } else {
            cout << "NO\n";
        }
    }

    return 0;
}