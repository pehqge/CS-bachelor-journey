#include <bits/stdc++.h>
using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

unsigned long long generateHash(const string &input) {
    vector<int> primes = {
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 
    31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 
    73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 
    127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 
    179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 
    233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 
    283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 
    353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 
    419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 
    467, 479, 487, 491, 499, 503, 509, 521, 523, 541
};

    unsigned long long hashValue = 1;

    for (char ch : input) {
        if (ch != ' ') {
            // ch = tolower(ch);
            hashValue *= primes[ch - 'a'];
        }
    }

    return hashValue;
}

int main() {
    fastIO();
    
    // input organizer
    int n;
    cin >> n;
    string empty;
    getline(cin, empty);
    getline(cin, empty);

    for (int i = 0; i < n; i++)
    {
    
    // create hashmap
    unordered_map<unsigned long long, vector<string>> anagrams;

    while (true) {
        string word;
        getline(cin, word);

        if (word == "") 
            break;

       unsigned long long hashValue = generateHash(word);
       anagrams[hashValue].push_back(word);
    }

    vector<string> answer;

    for (auto &pair : anagrams) {
        vector<string> &anagram = pair.second;
        if (anagram.size() == 1)
            continue;
        sort(anagram.begin(), anagram.end());

        int anagramSize = anagram.size();
        for (int i = 0; i < anagramSize; i++) {
            for (int j = i+1; j < anagramSize; j++)
            {
                ostringstream oss;
                oss << anagram[i] << " = " << anagram[j] << "\n";
                answer.push_back(oss.str());
            }
            
        }
    }

    sort(answer.begin(), answer.end());

    for (auto a : answer) {
        cout << a;
    }
    if (i != n-1) 
        cout << "\n";
    }

}