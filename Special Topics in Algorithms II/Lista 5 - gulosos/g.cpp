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

    int n;

    while (cin >> n) {
        if (n == 0) break;

        bool flag = false;

        for (int i = 0; i < n; ++i) {
            int x;
            cin >> x;

            if (x == 0){
                continue;
            }

            if (flag) {
                cout << " ";
            }
            else {
                flag = true;
            }
            cout << x;
            
        }
        
        if (!flag) {
            cout << 0;
        }

        cout << "\n";

    }
    return 0;

}