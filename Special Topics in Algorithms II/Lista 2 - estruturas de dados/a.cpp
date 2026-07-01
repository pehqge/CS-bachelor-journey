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
        string word;
        cin >> word;
        if (word == "#") break;

        next_permutation(all(word)) ? cout << word << "\n" : cout << "No Successor\n";
    }

    return 0;
}