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

    bool first = true;

    while (true) {
        int n;
        cin >> n;
        if (n == 0)
            break;

        if (!first) {
            cout << "\n"; 
        }
        first = false;

        vector<int> dims(n);
        unordered_map<int, int> freq;
        int max_freq = 0;

        for (int i = 0; i < n; ++i) {
            cin >> dims[i];
            freq[dims[i]]++;
            max_freq = max(max_freq, freq[dims[i]]);
        }

        int k = max_freq;
        sort(all(dims)); 

        vector<vector<int>> pieces(k);

        for (int i = 0; i < n; ++i) {
            int idx = i % k;
            pieces[idx].push_back(dims[i]);
        }

        cout << k << "\n";
        for (int i = 0; i < k; ++i) {
            for (int j = 0; j < pieces[i].size(); ++j) {
                if (j > 0)
                    cout << " ";
                cout << pieces[i][j];
            }
            cout << "\n";
        }
    }

    return 0;
}