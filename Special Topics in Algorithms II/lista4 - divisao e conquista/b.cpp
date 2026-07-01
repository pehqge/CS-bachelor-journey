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
        if (!(cin >> n)) break; 

        vector<int> books(n);

        for (int i = 0; i < n; i++) {
            cin >> books[i];
        }

        sort(all(books)); 

        int price;
        cin >> price;

        int minDiff = INT_MAX;
        int book1 = 0;
        int book2 = 0;

        for (int i = 0; i < n; i++) {
            int currentBook = books[i];
            int requiredBook = price - currentBook;

            if (binary_search(all(books), requiredBook)) {
                int diff = abs(currentBook - requiredBook);
                if (diff < minDiff) {
                    book1 = currentBook;
                    book2 = requiredBook;
                    minDiff = diff;
                }}
            }

        cout << "Peter should buy books whose prices are " << book1 << " and " << book2 << ".\n\n";
        }

    return 0;
    }