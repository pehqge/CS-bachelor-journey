#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

const int MAX_N = 2005;
const double EPS = 1e-8;

int T, N;
double A, B, C;
double x[MAX_N], y[MAX_N];
double t_proj[MAX_N];

double x0, y_zero, dx, dy;
double dir_norm;

double total_distance(double t) {
    double xt = x0 + dx * t;
    double yt = y_zero + dy * t;
    double sum = 0.0;
    for (int i = 0; i < N; ++i) {
        double dx_i = x[i] - xt;
        double dy_i = y[i] - yt;
        sum += sqrt(dx_i * dx_i + dy_i * dy_i);
    }
    return sum;
}

int main() {
    fastIO();

    cin >> T;
    while (T--) {
        cin >> N;
        cin >> A >> B >> C;
        for (int i = 0; i < N; ++i) {
            cin >> x[i] >> y[i];
        }

        if (fabs(A) > EPS) {
            y_zero = 0;
            x0 = (-B * y_zero - C) / A;
        } else if (fabs(B) > EPS) {
            x0 = 0;
            y_zero = (-A * x0 - C) / B;
        } else {
            x0 = y_zero = 0;
        }


        dx = B;
        dy = -A;

        dir_norm = dx * dx + dy * dy;

        double t_min = 1e9, t_max = -1e9;

        for (int i = 0; i < N; ++i) {
            
            double numer = (x[i] - x0) * dx + (y[i] - y_zero) * dy;
            double t_i = numer / dir_norm;
            t_proj[i] = t_i;
            t_min = min(t_min, t_i);
            t_max = max(t_max, t_i);
        }

        double left = t_min - 1000;
        double right = t_max + 1000;

       
        for (int iter = 0; iter < 100; ++iter) {
            double m1 = left + (right - left) / 3.0;
            double m2 = right - (right - left) / 3.0;
            double f1 = total_distance(m1);
            double f2 = total_distance(m2);
            if (f1 < f2) {
                right = m2;
            } else {
                left = m1;
            }
        }

        double t_opt = (left + right) / 2.0;
        double min_total_distance = total_distance(t_opt);

        cout << fixed << setprecision(6) << min_total_distance << "\n";
    }

    return 0;
}