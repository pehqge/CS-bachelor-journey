#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

struct Ponto {
    ll x, y;
};

static ll cross(const Ponto &A, const Ponto &B, const Ponto &C) {
    return (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x);
}

static vector<Ponto> fechoConvexo(vector<Ponto> &pts) {
    sort(all(pts), [](const Ponto &a, const Ponto &b){
        return (a.x < b.x) || (a.x == b.x && a.y < b.y);
    });
    vector<Ponto> hull;
    for (auto &p : pts) {
        while (hull.size() > 1 && cross(hull[hull.size()-2], hull[hull.size()-1], p) <= 0)
            hull.pop_back();
        hull.push_back(p);
    }
    for (int i = (int)pts.size()-2, l = (int)hull.size()+1; i >= 0; i--) {
        while ((int)hull.size() >= l && cross(hull[hull.size()-2], hull[hull.size()-1], pts[i]) <= 0)
            hull.pop_back();
        hull.push_back(pts[i]);
    }
    hull.pop_back();
    return hull;
}

static bool pontoNoFecho(const vector<Ponto> &hull, const Ponto &p) {
    int n = (int)hull.size();
    if (n < 3) {
        if (n == 1) {
            return (p.x == hull[0].x && p.y == hull[0].y);
        } else if (n == 2) {
            ll cross_val = cross(hull[0], hull[1], p);
            if (cross_val == 0) {
                if (min(hull[0].x, hull[1].x) <= p.x && p.x <= max(hull[0].x, hull[1].x) &&
                    min(hull[0].y, hull[1].y) <= p.y && p.y <= max(hull[0].y, hull[1].y))
                    return true;
            }
            return false;
        }
        return false;
    }
   
    for (int i = 0; i < n; i++) {
        ll c = cross(hull[i], hull[(i+1)%n], p);
        if (c < 0) return false; 
    }
    return true;
}

int main() {
    fastIO();
    int c, r, o;
    int caso = 1;
    while (true) {
        cin >> c >> r >> o;
        if (!cin || (c == 0 && r == 0 && o == 0)) break;

        vector<Ponto> cops(c), robbers(r), outros(o);
        for (int i = 0; i < c; i++) cin >> cops[i].x >> cops[i].y;
        for (int i = 0; i < r; i++) cin >> robbers[i].x >> robbers[i].y;
        for (int i = 0; i < o; i++) cin >> outros[i].x >> outros[i].y;

        vector<Ponto> fechoCops = fechoConvexo(cops);
        vector<Ponto> fechoRobbers = fechoConvexo(robbers);

        cout << "Data set " << caso++ << ":\n";
        for (auto &cit : outros) {
            bool dentroCops = pontoNoFecho(fechoCops, cit);
            bool dentroRobbers = pontoNoFecho(fechoRobbers, cit);
            cout << "Citizen at (" << cit.x << "," << cit.y << ") is ";
            if (dentroCops) cout << "safe.\n";
            else if (!dentroCops && dentroRobbers) cout << "robbed.\n";
            else cout << "neither.\n";
        }
        cout << "\n";
    }
    return 0;
}
