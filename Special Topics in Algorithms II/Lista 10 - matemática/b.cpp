#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

ll phi(ll n) {
    ll result = n;
    for (ll i = 2; i * i <= n; ++i) {
        if (n % i == 0) {
            while (n % i == 0) {
                n /= i;
            }
            result -= result / i;
        }
    }
    if (n > 1) {
        result -= result / n;
    }
    return result;
}

int main() {
    fastIO();

    ll n;
    while (cin >> n && n != 0) {
        cout << phi(n) << "\n";
    }

    return 0;
}