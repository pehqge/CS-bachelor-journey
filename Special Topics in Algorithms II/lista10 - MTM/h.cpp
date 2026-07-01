#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

ll catalan(int nodes) {
    ll resultado = 1;
    for (int i = 0; i < nodes; ++i) {
        resultado = resultado * (2 * nodes - i) / (i + 1);
    }
    return resultado / (nodes + 1);
}

int main() {
    fastIO();

    ll n;
    while (cin >> n) {
        int nodes = 1;
        while (catalan(nodes) <= n) {
            ++nodes;
        }
        cout << nodes - 1 << "\n";
    }

    return 0;
}