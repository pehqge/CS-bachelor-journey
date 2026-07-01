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

    int caseNum = 1;

    while (true) {
        int B, S;
        cin >> B >> S;

        if (B == 0 && S == 0)
            break;

        vector<int> bachelorAges(B);
        vector<int> spinsterAges(S);

        for (int i = 0; i < B; ++i) {
            cin >> bachelorAges[i];
        }

        for (int i = 0; i < S; ++i) {
            cin >> spinsterAges[i];
        }

        cout << "Case " << caseNum << ": ";

        if (B <= S) {
            cout << "0\n";
        } else {
            int unmatched = B - S;
            int youngestBachelor = *min_element(all(bachelorAges));
            cout << unmatched << " " << youngestBachelor << "\n";
        }

        caseNum++;
    }

    return 0;
}