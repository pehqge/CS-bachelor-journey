#include <bits/stdc++.h>

#define ll long long
#define all(x) x.begin(), x.end()

using namespace std;

void fastIO() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
}

struct Competidor {
    int id;
    int problemas_resolvidos = 0;
    int tempo_penalidade = 0;
    bool participou = false;
    int tentativas[10];          
    bool problema_resolvido[10]; 

    Competidor() {
        memset(tentativas, 0, sizeof(tentativas));
        memset(problema_resolvido, false, sizeof(problema_resolvido));
    }
};

int main() {
    fastIO();

    int casos;
    cin >> casos;
    cin.ignore(); 

    string linha;
    getline(cin, linha); 

    for (int caso = 0; caso < casos; ++caso) {
        vector<Competidor> competidores(101); 

        for (int i = 1; i <= 100; ++i) {
            competidores[i].id = i;
        }

        while (true) {
            if (!getline(cin, linha) || linha.empty()) {
                break;
            }

            stringstream ss(linha);
            int id, problema, tempo;
            char resultado;
            ss >> id >> problema >> tempo >> resultado;

            Competidor& c = competidores[id];
            c.participou = true;

            if (resultado == 'C') {
                if (!c.problema_resolvido[problema]) {
                    c.problemas_resolvidos++;
                    c.problema_resolvido[problema] = true;
                    c.tempo_penalidade += tempo;
                    c.tempo_penalidade += c.tentativas[problema] * 20;
                }
            } else if (resultado == 'I') {
                if (!c.problema_resolvido[problema]) {
                    c.tentativas[problema]++;
                }
            }
            
        }

        vector<Competidor> participantes;
        for (int i = 1; i <= 100; ++i) {
            if (competidores[i].participou) {
                participantes.push_back(competidores[i]);
            }
        }

        sort(all(participantes), [](const Competidor& a, const Competidor& b) {
            if (a.problemas_resolvidos != b.problemas_resolvidos)
                return a.problemas_resolvidos > b.problemas_resolvidos;
            if (a.tempo_penalidade != b.tempo_penalidade)
                return a.tempo_penalidade < b.tempo_penalidade;
            return a.id < b.id;
        });

        for (const auto& c : participantes) {
            cout << c.id << " " << c.problemas_resolvidos << " " << c.tempo_penalidade << "\n";
        }

        if (caso != casos - 1)
            cout << "\n"; 
    }

    return 0;
}