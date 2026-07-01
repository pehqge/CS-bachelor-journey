#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

const int MAXN = 1000005;
const int ALPHA = 52;

int next_pos[MAXN][ALPHA];
int char_to_index(char c) {
    if (c >= 'A' && c <= 'Z') {
        return c - 'A'; 
    } else {
        return c - 'a' + 26;
    }
}

int main() {
    fastIO();

    string S;
    cin >> S;
    int len_S = S.length();


    for (int i = 0; i < ALPHA; ++i) {
        next_pos[len_S][i] = len_S;
    }

    
    for (int i = len_S - 1; i >= 0; --i) {
        for (int j = 0; j < ALPHA; ++j) {
            next_pos[i][j] = next_pos[i + 1][j];
        }
        int idx = char_to_index(S[i]);
        next_pos[i][idx] = i;
    }

    int Q;
    cin >> Q;
    cin.ignore(); 

    for (int q = 0; q < Q; ++q) {
        string SS;
        getline(cin, SS);

        int pos = 0;
        int start = -1, end = -1;
        bool matched = true;

        for (size_t i = 0; i < SS.length(); ++i) {
            int idx = char_to_index(SS[i]);
            pos = next_pos[pos][idx];
            if (pos == len_S) {
                matched = false;
                break;
            }
            if (i == 0) {
                start = pos;
            }
            if (i == SS.length() - 1) {
                end = pos;
            }
            pos++; 
        }

        if (matched) {
            cout << "Matched " << start << " " << end << "\n";
        } else {
            cout << "Not matched\n";
        }
    }

    return 0;
}