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

    int T;
    cin >> T;

    for (int caseNum = 1; caseNum <= T; ++caseNum) {
        int N;
        cin >> N;
        string field;
        cin >> field;

        int count = 0;
        int i = 0;

        while (i < N) {
            if (field[i] == '.') {
                count++;
                i += 3; 
            } else {
                i++;
            }
        }

        cout << "Case " << caseNum << ": " << count << "\n";
    }

    return 0;
}