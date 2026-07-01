#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

bool divide_factorial(ll n, ll m) {
    if (m == 0) return false;
    if (m == 1) return true;
    
    for (ll i = 2; i * i <= m; ++i) {
        int count_m = 0, count_n = 0;
        while (m % i == 0) {
            m /= i;
            ++count_m;
        }
        ll power = i;
        while (power <= n) {
            count_n += n / power;
            if (power > n / i) break; 
            power *= i;
        }
        if (count_n < count_m) return false;
    }
    if (m > 1 && n < m) return false;
    return true;
}

int main() {
    fastIO();

    ll n, m;
    while (cin >> n >> m) {
        if (divide_factorial(n, m)) {
            cout << m << " divides " << n << "!\n";
        } else {
            cout << m << " does not divide " << n << "!\n";
        }
    }

    return 0;
}