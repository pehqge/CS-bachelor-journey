#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

int N;
map<int, vector<char>> code_to_chars; 
string encrypted_str;
set<string> resultados;
int test_case_num = 1;
const int max_results = 100;

void decode(int pos, string current) {
    if (resultados.size() >= max_results) return;

    if (pos == encrypted_str.size()) {
        resultados.insert(current);
        return;
    }

    for (int len = 1; len <= 3 && pos + len <= encrypted_str.size(); ++len) {
        string code_str = encrypted_str.substr(pos, len);
        string code_str_no_leading_zeros = code_str;
       
        while (code_str_no_leading_zeros.length() > 1 && code_str_no_leading_zeros[0] == '0') {
            code_str_no_leading_zeros.erase(0, 1);
        }

        if (code_str_no_leading_zeros.empty()) continue;

        int code_int = stoi(code_str_no_leading_zeros);
        if (code_int > 99) continue; 

        if (code_to_chars.count(code_int)) {
            for (char ch : code_to_chars[code_int]) {
                decode(pos + len, current + ch);
                if (resultados.size() >= max_results) return;
            }
        }
    }
}

int main() {
    fastIO();

    while (cin >> N && N != 0) {
        code_to_chars.clear();
        resultados.clear();
        for (int i = 0; i < N; ++i) {
            char letter;
            int code;
            cin >> letter >> code;
            code_to_chars[code].push_back(letter);
        }
        cin.ignore(); 
        getline(cin, encrypted_str);

        decode(0, "");

        cout << "Case #" << test_case_num << "\n";
        if (resultados.empty()) {
            cout << "\n";
        } else {
            vector<string> vec_resultados(all(resultados));
            sort(all(vec_resultados));
            int count = 0;
            for (const auto& res : vec_resultados) {
                cout << res << "\n";
                count++;
                if (count >= max_results) break;
            }
        }
        cout << "\n";
        test_case_num++;
    }

    return 0;
}