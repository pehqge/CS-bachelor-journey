#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

double f(double x, int p, int q, int r, int s, int t, int u) {
    return p * exp(-x) + q * sin(x) + r * cos(x) + s * tan(x) + t * x * x + u;
}

double bisection(int p, int q, int r, int s, int t, int u) {
    double left = 0;
    double right = 1;
    double mid;

    while ((right - left) > 1e-9) { 
        mid = (left + right) / 2;
        double fmid = f(mid, p, q, r, s, t, u);

        if (fmid * f(left, p, q, r, s, t, u) > 0) {
            left = mid;
        } else {
            right = mid;
        }
    }

    return round((left + right) / 2 * 10000) / 10000.0;
}

int main() {
    fastIO();

    while (true) {
        int p, q, r, s, t, u;
        if (!(cin >> p >> q >> r >> s >> t >> u)) break;

        if (f(0, p, q, r, s, t, u) * f(1, p, q, r, s, t, u) > 0) {
            cout << "No solution\n";
        } else {
            cout << fixed << setprecision(4) << bisection(p, q, r, s, t, u) << "\n";
        }

    }

    return 0;
}