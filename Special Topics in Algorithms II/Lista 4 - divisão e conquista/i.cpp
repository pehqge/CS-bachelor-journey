#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

const double EPS = 1e-8;
const int MAX_T = 15;

int T;
double CF[MAX_T];

double NPV(double IRR) {
    double npv = CF[0];
    for (int i = 1; i <= T; ++i) {
        npv += CF[i] / pow(1.0 + IRR, i);
    }
    return npv;
}

int sign(double x) {
    if (fabs(x) < EPS) return 0;
    return x > 0 ? 1 : -1;
}

int main() {
    fastIO();

    while (cin >> T && T != 0) {
        for (int i = 0; i <= T; ++i) {
            cin >> CF[i];
        }

        vector<double> roots;
        vector<double> test_points;


        test_points.push_back(-0.99999);

       
        for (double exp = -10; exp <= 10; exp += 0.5) {
            double irr = pow(10, exp) - 1.0;
            test_points.push_back(irr);
        }


        sort(all(test_points));
        test_points.erase(unique(all(test_points)), test_points.end());

       
        vector<pair<double, double>> intervals;

        for (size_t i = 1; i < test_points.size(); ++i) {
            double IRR1 = test_points[i - 1];
            double IRR2 = test_points[i];

            if (IRR1 <= -1 + EPS) continue;

            double NPV1 = NPV(IRR1);
            double NPV2 = NPV(IRR2);

            if (isnan(NPV1) || isnan(NPV2)) continue;

            if (sign(NPV1) != sign(NPV2)) {
                intervals.emplace_back(IRR1, IRR2);
            } else if (sign(NPV1) == 0) {
                roots.push_back(IRR1);
            }
        }

        
        for (auto interval : intervals) {
            double low = interval.first;
            double high = interval.second;
            double mid;
            int iterations = 0;

            while (high - low > EPS && iterations < 100) {
                mid = (low + high) / 2.0;
                double npv_mid = NPV(mid);

                if (isnan(npv_mid)) {
                    high = mid;
                } else if (sign(npv_mid) == 0) {
                    break;
                } else if (sign(npv_mid) == sign(NPV(low))) {
                    low = mid;
                } else {
                    high = mid;
                }
                iterations++;
            }
            double root = (low + high) / 2.0;
            roots.push_back(root);
        }

       
        sort(all(roots));
        vector<double> unique_roots;
        for (size_t i = 0; i < roots.size(); ++i) {
            if (i == 0 || fabs(roots[i] - roots[i - 1]) > EPS) {
                unique_roots.push_back(roots[i]);
            }
        }

      
        vector<double> valid_roots;
        for (double r : unique_roots) {
            if (r > -1 + EPS) {
                valid_roots.push_back(r);
            }
        }

        if (valid_roots.size() == 0) {
            cout << "No\n";
        } else if (valid_roots.size() == 1) {
            double irr = valid_roots[0];
            irr += EPS; 
            cout << fixed << setprecision(2) << irr << "\n";
        } else {
            cout << "Too many\n";
        }
    }

    return 0;
}