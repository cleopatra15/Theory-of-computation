#include "DFA.h"

using namespace std;

string DFA::cautaTranzitie(string st, string sim) {
    for (int i = 0; i < functie_tranzitie.size(); i++) {
        if (functie_tranzitie[i].stare1 == st && functie_tranzitie[i].simbol == sim) {
            return functie_tranzitie[i].stare2;
        }
    }
    return "";
}

void DFA::afisare() {
    cout << "\nRezumat DFA" << endl;
    cout << "Alfabetul(Sigma): ";
    for (int i = 0; i < sigma.size(); i++) {
        cout << " " << sigma[i] << " ";
    }
    cout << endl;

    cout << "Stari: ";
    for (int i = 0; i < stari.size(); i++) {
        cout << " " << stari[i] << " ";
    }
    cout << endl;

    cout << "Stare finala: " << stare_finala << endl;
    cout << "Stare initiala: " << stare_initiala << endl;
}

bool DFA::testeazaCuvant(string cuvant) {
    string stare_curenta = stare_initiala;

    cout << "\nTestare cuvant: \"" << cuvant << "\"" << endl;
    cout << "Stare initiala: " << stare_curenta << endl;

    for (int i = 0; i < cuvant.length(); i++) {
        string simbol(1, cuvant[i]);
        string dest = cautaTranzitie(stare_curenta, simbol);

        if (dest.length() > 0) {
            stare_curenta = dest;
            cout << "  Simbol '" << cuvant[i] << "' -> " << stare_curenta << endl;
        } else {
            cout << "  Simbol '" << cuvant[i] << "' -> EROARE (tranzitie nedefinita)" << endl;
            return false;
        }
    }

    bool acceptat = (stare_curenta == stare_finala);
    cout << "Stare finala atinsa: " << stare_curenta << endl;
    cout << "Rezultat: " << (acceptat ? "ACCEPTAT" : "RESPINS") << endl;

    return acceptat;
}
