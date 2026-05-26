#include <iostream>
#include <string>
#include <vector>
#include "DFA.h"
#include "Parser.h"
#include "Structuri.h"

using namespace std;

int main() {
    string numeFisier;

    cout << "Introdu numele fisierului DFA (default: t1.dfa): ";
    getline(cin, numeFisier);

    if (numeFisier.length() == 0) {
        numeFisier = "t1.dfa";
    }

    DFA *dfa = new DFA();

    vector<Sectiune> date_fisier = Parser::extrageSectiuni(numeFisier);

    if (!Parser::populareDFA(date_fisier, dfa)) {
        cout << "Nu s-au putut incarca datele din fisier." << endl;
        delete dfa;
        return 1;
    }

    dfa->afisare();

    cout << "\nTESTARE CUVINTE" << endl;
    string cuvant;
    while (true) {
        cout << "\nIntroduceti un cuvant de test (sau 'exit' pentru a iesi): ";
        getline(cin, cuvant);

        if (cuvant == "exit") break;

        dfa->testeazaCuvant(cuvant);
    }

    delete dfa;
    return 0;
}
