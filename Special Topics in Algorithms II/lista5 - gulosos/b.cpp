#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

int main() {
    fastIO();

    while (true) {
        int n, d, r;
        cin >> n >> d >> r;

        if (n == 0 && d == 0 && r == 0)
            break;

        vector<int> morning(n);
        vector<int> evening(n);

        for (int i = 0; i < n; ++i) {
            cin >> morning[i];
        }

        for (int i = 0; i < n; ++i) {
            cin >> evening[i];
        }

        sort(all(morning));            
        sort(all(evening));
        reverse(all(evening)); 

        ll total_overtime = 0;

        for (int i = 0; i < n; ++i) {
            int total_length = morning[i] + evening[i];
            if (total_length > d) {
                total_overtime += (total_length - d) * r;
            }
        }

        cout << total_overtime << "\n";
    }

    return 0;
}