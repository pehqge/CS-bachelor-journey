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
    Ponto(int x = 0, int y = 0) : x(x), y(y) {}
    bool operator<(const Ponto &outro) const {
        return x < outro.x || (x == outro.x && y < outro.y);
    }
    Ponto operator-(const Ponto &outro) const {
        return Ponto(x - outro.x, y - outro.y);
    }
    ll cruzamento(const Ponto &outro) const {
        return (ll)x * outro.y - (ll)y * outro.x;
    }
    ll distancia2(const Ponto &outro) const {
        return (ll)(x - outro.x) * (x - outro.x) + (ll)(y - outro.y) * (y - outro.y);
    }
};

vector<Ponto> fechoConvexo(vector<Ponto> &pontos) {
    sort(all(pontos));
    vector<Ponto> fecho;
    for (int fase = 0; fase < 2; ++fase) {
        auto inicio = fecho.size();
        for (auto &p : pontos) {
            while (fecho.size() >= inicio + 2 &&
                   (fecho[fecho.size() - 1] - fecho[fecho.size() - 2]).cruzamento(p - fecho[fecho.size() - 1]) <= 0) {
                fecho.pop_back();
            }
            fecho.push_back(p);
        }
        fecho.pop_back();
        reverse(all(pontos));
    }
    return fecho;
}

double calculaDistanciaMaxima(vector<Ponto> &fecho) {
    int n = fecho.size();
    if (n < 2) return 0;
    ll maxDist2 = 0;
    for (int i = 0, j = 1; i < n; ++i) {
        while (true) {
            ll distAtual = fecho[i].distancia2(fecho[j]);
            ll distProxima = fecho[i].distancia2(fecho[(j + 1) % n]);
            if (distProxima > distAtual) j = (j + 1) % n;
            else break;
        }
        maxDist2 = max(maxDist2, fecho[i].distancia2(fecho[j]));
    }
    return sqrt((double)maxDist2);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int c;
    cin >> c;
    vector<Ponto> pontos(c);
    for (int i = 0; i < c; ++i) {
        cin >> pontos[i].x >> pontos[i].y;
    }

    vector<Ponto> fecho = fechoConvexo(pontos);
    double maiorDistancia = calculaDistanciaMaxima(fecho);

    cout << fixed << setprecision(7) << maiorDistancia << "\n";

    return 0;
}