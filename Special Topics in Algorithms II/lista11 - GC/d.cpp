#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

struct P {
    ll x, y;
    int id;
};

ll cross(P A, P B, P C) {
    return (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x);
}

int main() {
    fastIO();
    int N; cin >> N;
    vector<P> pts(N);
    for (int i = 0; i < N; i++) {
        cin >> pts[i].x >> pts[i].y;
        pts[i].id = i + 1;
    }
    sort(all(pts), [](auto &a, auto &b) {
        return a.x < b.x || (a.x == b.x && a.y < b.y);
    });

    vector<P> casco;
    for (auto &p : pts) {
        while (casco.size() > 1 && cross(casco[casco.size()-2], casco[casco.size()-1], p) < 0)
            casco.pop_back();
        casco.push_back(p);
    }

    for (int i = N - 2, l = (int)casco.size() + 1; i >= 0; i--) {
        while ((int)casco.size() >= l && cross(casco[casco.size()-2], casco[casco.size()-1], pts[i]) < 0)
            casco.pop_back();
        casco.push_back(pts[i]);
    }

    casco.pop_back();

    vector<bool> infinito(N + 1, false);
    for (auto &p : casco)
        infinito[p.id] = true;

    for (int i = 1; i <= N; i++) {
        if (infinito[i]) cout << i << " ";
    }
    cout << "\n";

    return 0;
}