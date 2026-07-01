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
        int n;
        cin >> n;

        if (n == 0) break;

        priority_queue<int, vector<int>, greater<int>> pq;
        for (int i = 0; i < n; i++) {
            int x;
            cin >> x;
            pq.push(x);
        }

        int g_ans = 0;
        while (pq.size() > 1) {
            int ans = 0;
            ans += pq.top();
            pq.pop();
            ans += pq.top();
            pq.pop();
            pq.push(ans);
            g_ans += ans;
        }

        cout << g_ans << "\n";

    }

    return 0;
}