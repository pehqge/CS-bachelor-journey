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
    double x, y;
    Ponto(double x = 0, double y = 0) : x(x), y(y) {}
};

double calcularArea(const vector<Ponto>& vertices) {
    double area = 0.0;
    int n = vertices.size();
    for (int i = 0; i < n; ++i) {
        int j = (i + 1) % n;
        area += vertices[i].x * vertices[j].y;
        area -= vertices[j].x * vertices[i].y;
    }
    return fabs(area) / 2.0;
}

bool pontoNoSegmento(const Ponto& p, const Ponto& a, const Ponto& b) {
    return (min(a.x, b.x) <= p.x && p.x <= max(a.x, b.x) &&
            min(a.y, b.y) <= p.y && p.y <= max(a.y, b.y));
}

int orientacao(const Ponto& a, const Ponto& b, const Ponto& c) {
    double val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y);
    if (fabs(val) < 1e-9) return 0; // colinear
    return (val > 0) ? 1 : 2; // horário ou anti-horário
}

bool segmentosSeInterceptam(const Ponto& p1, const Ponto& q1, const Ponto& p2, const Ponto& q2) {
    int o1 = orientacao(p1, q1, p2);
    int o2 = orientacao(p1, q1, q2);
    int o3 = orientacao(p2, q2, p1);
    int o4 = orientacao(p2, q2, q1);

    if (o1 != o2 && o3 != o4) return true;

    if (o1 == 0 && pontoNoSegmento(p2, p1, q1)) return true;
    if (o2 == 0 && pontoNoSegmento(q2, p1, q1)) return true;
    if (o3 == 0 && pontoNoSegmento(p1, p2, q2)) return true;
    if (o4 == 0 && pontoNoSegmento(q1, p2, q2)) return true;

    return false;
}

bool pontoNoPoligono(const Ponto& p, const vector<Ponto>& vertices) {
    int n = vertices.size();
    if (n < 3) return false;

    Ponto extremo = {1000001, p.y};
    int contagem = 0, i = 0;
    do {
        int proximo = (i + 1) % n;
        if (segmentosSeInterceptam(vertices[i], vertices[proximo], p, extremo)) {
            if (orientacao(vertices[i], p, vertices[proximo]) == 0)
                return pontoNoSegmento(p, vertices[i], vertices[proximo]);
            contagem++;
        }
        i = proximo;
    } while (i != 0);

    return contagem % 2 == 1;
}

int main() {
    int caso = 1;
    int n, w, h, x, y;
    while (cin >> n >> w >> h >> x >> y) {
        vector<Ponto> vertices = {{0, 0}, {static_cast<double>(w), 0}, {static_cast<double>(w), static_cast<double>(h)}, {0, static_cast<double>(h)}};
        vector<vector<Ponto>> regioes = {vertices};

        for (int i = 0; i < n; ++i) {
            int x1, y1, x2, y2;
            cin >> x1 >> y1 >> x2 >> y2;
            Ponto p1(x1, y1), p2(x2, y2);
            vector<vector<Ponto>> novasRegioes;

            for (const auto& regiao : regioes) {
                vector<Ponto> regiao1, regiao2;
                int m = regiao.size();
                for (int j = 0; j < m; ++j) {
                    Ponto atual = regiao[j];
                    Ponto proximo = regiao[(j + 1) % m];
                    if (orientacao(p1, p2, atual) != 2) regiao1.push_back(atual);
                    if (orientacao(p1, p2, atual) != 1) regiao2.push_back(atual);

                    if (segmentosSeInterceptam(p1, p2, atual, proximo)) {
                        double a1 = proximo.y - atual.y;
                        double b1 = atual.x - proximo.x;
                        double c1 = a1 * atual.x + b1 * atual.y;

                        double a2 = p2.y - p1.y;
                        double b2 = p1.x - p2.x;
                        double c2 = a2 * p1.x + b2 * p1.y;

                        double determinante = a1 * b2 - a2 * b1;
                        if (fabs(determinante) > 1e-9) {
                            double intersecX = (b2 * c1 - b1 * c2) / determinante;
                            double intersecY = (a1 * c2 - a2 * c1) / determinante;
                            Ponto intersecao(intersecX, intersecY);
                            regiao1.push_back(intersecao);
                            regiao2.push_back(intersecao);
                        }
                    }
                }
                if (regiao1.size() > 2) novasRegioes.push_back(regiao1);
                if (regiao2.size() > 2) novasRegioes.push_back(regiao2);
            }
            regioes = novasRegioes;
        }

        Ponto fonte(x, y);
        double areaFonte = 0.0;
        for (const auto& regiao : regioes) {
            if (pontoNoPoligono(fonte, regiao)) {
                areaFonte = calcularArea(regiao);
                break;
            }
        }

        cout << fixed << setprecision(3);
        cout << "Case #" << caso << ": " << areaFonte << endl;
        caso++;
    }
    return 0;
}