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


        // cada bloco de teste
        while (true) {

            queue<int> output;
            queue<int> a;
            stack<int> b;

            // cria a fila de trens
            for (int i = 1; i <= n; i++) a.push(i);


            int x;
            cin >> x;
            if (x == 0) break;

            output.push(x);

            for (int i = 1; i < n; i++) {
                cin >> x;
                output.push(x);
            }

            while (!a.empty()) {

                if (!b.empty() and output.front() == b.top()) {
                    b.pop();
                    output.pop();
                } else if (a.front() == output.front()) {
                    a.pop();
                    output.pop();
                } else {
                    b.push(a.front());
                    a.pop();
                }
            }

            while (!b.empty() and b.top() == output.front()) {
                b.pop();
                output.pop();
            }

            if (output.empty()) cout << "Yes\n";
            else cout << "No\n";

        }

        cout << "\n";
    }

    return 0;
}