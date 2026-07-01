#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

struct Resultado {
    ll x, y, d;
};

Resultado gcd_extendido(ll a, ll b) {
    if (b == 0) return {1, 0, a};
    auto r = gcd_extendido(b, a % b);
    return {r.y, r.x - (a / b) * r.y, r.d};
}

int main() {
    fastIO();

    ll n;
    while (cin >> n && n != 0) {
        ll c1, n1, c2, n2;
        cin >> c1 >> n1 >> c2 >> n2;

        auto res = gcd_extendido(n1, n2);
        if (n % res.d != 0) {
            cout << "failed\n";
            continue;
        }

        ll fator = n / res.d;
        ll x0 = res.x * fator;
        ll y0 = res.y * fator;
        ll passo1 = n2 / res.d;
        ll passo2 = n1 / res.d;

        ll t_min = ceil(-1.0 * x0 / passo1);
        ll t_max = floor(1.0 * y0 / passo2);

        if (t_min > t_max) {
            cout << "failed\n";
            continue;
        }

        ll custo1 = c1 * passo1 - c2 * passo2;
        ll melhor_t = custo1 > 0 ? t_min : t_max;

        ll x = x0 + melhor_t * passo1;
        ll y = y0 - melhor_t * passo2;

        cout << x << " " << y << "\n";
    }

    return 0;
}