#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

const int LIMIT = 20000000;
vector<int> primes;
vector<pair<int, int>> twin_primes;

void sieve() {
    vector<bool> is_prime(LIMIT + 1, true);
    for (int i = 2; i * i <= LIMIT; ++i) {
        if (is_prime[i]) {
            for (int j = i * i; j <= LIMIT; j += i) {
                is_prime[j] = false;
            }
        }
    }
    for (int i = 2; i <= LIMIT; ++i) {
        if (is_prime[i]) primes.push_back(i);
    }
    for (size_t i = 0; i < primes.size() - 1; ++i) {
        if (primes[i + 1] - primes[i] == 2) {
            twin_primes.emplace_back(primes[i], primes[i + 1]);
        }
    }
}

int main() {
    fastIO();

    sieve();

    int s;
    while (cin >> s) {
        auto [p1, p2] = twin_primes[s - 1];
        cout << "(" << p1 << ", " << p2 << ")\n";
    }

    return 0;
}