#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

pair<ll, ll> fibonacciMod(ll n, ll mod) {
    if (n == 0) return {0, 1};
    auto [a, b] = fibonacciMod(n / 2, mod);
    ll c = (a * (2 * b - a + mod)) % mod;
    ll d = (a * a + b * b) % mod;
    if (n % 2 == 0) return {c, d};
    return {d, (c + d) % mod};
}

int main() {
    fastIO();

    ll n, m;
    while (cin >> n >> m) {
        ll mod = 1LL << m;
        cout << fibonacciMod(n, mod).first << "\n";
    }

    return 0;
}