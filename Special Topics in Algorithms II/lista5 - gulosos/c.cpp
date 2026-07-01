#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

struct Interval {
    int left, right;
};

int main() {
    fastIO();

    while (true) {
        int L, G;
        cin >> L >> G;
        if (L == 0 && G == 0)
            break;

        vector<Interval> intervalos;
        for (int i = 0; i < G; ++i) {
            int x, r;
            cin >> x >> r;
            int left = max(0, x - r);
            int right = min(L, x + r);
            if (left >= L || right <= 0)
                continue; 
            intervalos.push_back({left, right});
        }

        sort(all(intervalos), [](const Interval& a, const Interval& b) {
            if (a.left == b.left)
                return a.right > b.right;
            return a.left < b.left;
        });

        int count = 0;
        int idx = 0;
        int current = 0;
        int max_right = 0;
        bool possible = true;

        while (current < L) {
            max_right = current;
            while (idx < intervalos.size() && intervalos[idx].left <= current) {
                max_right = max(max_right, intervalos[idx].right);
                idx++;
            }
            if (max_right == current) {
                possible = false;
                break;
            }
            current = max_right;
            count++;
        }

        if (!possible) {
            cout << "-1\n";
        } else {
            int result = G - count;
            cout << result << "\n";
        }
    }

    return 0;
}