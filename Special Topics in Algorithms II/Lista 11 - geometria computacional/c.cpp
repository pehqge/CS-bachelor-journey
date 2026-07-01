#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

struct Ponto {
    int x, y;

    bool operator<(const Ponto& p) const {
        return x < p.x || (x == p.x && y < p.y);
    }
};

int produtoVetorial(const Ponto& o, const Ponto& a, const Ponto& b) {
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x);
}

vector<Ponto> fechoConvexo(vector<Ponto>& pontos) {
    int n = pontos.size(), k = 0;
    if (n == 1) return pontos;

    vector<Ponto> fecho(2 * n);

    sort(all(pontos));

    for (int i = 0; i < n; ++i) {
        while (k >= 2 && produtoVetorial(fecho[k - 2], fecho[k - 1], pontos[i]) <= 0) k--;
        fecho[k++] = pontos[i];
    }

    for (int i = n - 1, t = k + 1; i >= 0; --i) {
        while (k >= t && produtoVetorial(fecho[k - 2], fecho[k - 1], pontos[i]) <= 0) k--;
        fecho[k++] = pontos[i];
    }

    fecho.resize(k - 1);
    return fecho;
}

int main() {
    fastIO();

    int n;
    while (cin >> n && n != 0) {
        set<Ponto> conjuntoPontos;
        for (int i = 0; i < n; ++i) {
            Ponto p;
            cin >> p.x >> p.y;
            conjuntoPontos.insert(p);
        }

        vector<Ponto> pontos(all(conjuntoPontos));
        vector<Ponto> fecho = fechoConvexo(pontos);

        auto inicio = min_element(all(fecho));

        cout << fecho.size() << '\n';
        for (auto it = inicio; it != fecho.end(); ++it) {
            cout << it->x << ' ' << it->y << '\n';
        }
        for (auto it = fecho.begin(); it != inicio; ++it) {
            cout << it->x << ' ' << it->y << '\n';
        }
    }

    return 0;
}