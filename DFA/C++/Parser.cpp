#include "Parser.h"
#include "Utils.h"
#include <iostream>
#include <fstream>

using namespace std;
using namespace Utils;

vector<Sectiune> Parser::extrageSectiuni(string numeFisier) {
    vector<Sectiune> toate_sectiunile;
    ifstream file(numeFisier);

    if (file.fail()) {
        cerr << "Eroare: Nu pot deschide fisierul " << numeFisier << endl;
        return toate_sectiunile;
    }

    string line;
    Sectiune sectiune_curenta;
    sectiune_curenta.nume = "";

    while (getline(file, line)) {
        string trimmed = trim(line);
        if (trimmed.empty()) continue;
        
        if (trimmed == "[end]") break;

        // FIXED: Check the first character using trimmed[0]
        if (trimmed[0] == '[' && trimmed[trimmed.length() - 1] == ']') {
            if (sectiune_curenta.nume != "") {
                toate_sectiunile.push_back(sectiune_curenta);
            }
            sectiune_curenta.nume = trimmed;
            sectiune_curenta.linii.clear();
        } 
        else {
            if (sectiune_curenta.nume != "") {
                sectiune_curenta.linii.push_back(trimmed);
            }
        }
    }
    
    if (sectiune_curenta.nume != "") {
        toate_sectiunile.push_back(sectiune_curenta);
    }

    file.close();
    return toate_sectiunile;
}

vector<string> Parser::getLiniiSectiune(vector<Sectiune> sectiuni, string numeCautat) {
    for (int i = 0; i < sectiuni.size(); i++) {
        if (sectiuni[i].nume == numeCautat) {
            return sectiuni[i].linii;
        }
    }
    return vector<string>();
}

void Parser::parsfunctieDFA(string line, DFA *dfa_ptr) {
    string trimmed = trim(line);
    // FIXED: Check the first character using trimmed[0]
    if (trimmed.length() == 0 || trimmed[0] != '(') return;

    int comma_pos = -1, close_paren = -1, arrow_pos = -1;
    for (int i = 0; i < trimmed.length(); i++) {
        if (trimmed[i] == ',') comma_pos = i;
        else if (trimmed[i] == ')') close_paren = i;
        else if (trimmed[i] == '-') arrow_pos = i;
    }

    if (comma_pos != -1 && close_paren != -1 && arrow_pos != -1) {
        string stare1 = trim(trimmed.substr(1, comma_pos - 1));
        string simbol = trim(trimmed.substr(comma_pos + 1, close_paren - comma_pos - 1));
        string stare2 = trim(trimmed.substr(arrow_pos + 1));

        if (stare1.length() > 0 && simbol.length() > 0 && stare2.length() > 0) {
            Tranzitie t(stare1, simbol, stare2);
            dfa_ptr->functie_tranzitie.push_back(t);
        }
    }
}

bool Parser::populareDFA(vector<Sectiune> sectiuni, DFA *dfa_ptr) {
    if (sectiuni.empty()) return false;

    vector<string> linii_sigma = getLiniiSectiune(sectiuni, "[sigma]");
    for (int i = 0; i < linii_sigma.size(); i++) {
        dfa_ptr->sigma.push_back(linii_sigma[i]);
    }

    vector<string> linii_stari = getLiniiSectiune(sectiuni, "[stari]");
    for (int i = 0; i < linii_stari.size(); i++) {
        dfa_ptr->stari.push_back(linii_stari[i]);
    }

    vector<string> linii_init = getLiniiSectiune(sectiuni, "[stare initiala]");
    // FIXED: Assign the first element of the vector
    if (linii_init.size() > 0) dfa_ptr->stare_initiala = linii_init[0];

    vector<string> linii_fin = getLiniiSectiune(sectiuni, "[stare finala]");
    // FIXED: Assign the first element of the vector
    if (linii_fin.size() > 0) dfa_ptr->stare_finala = linii_fin[0];

    vector<string> linii_functii = getLiniiSectiune(sectiuni, "[functie]");
    for (int i = 0; i < linii_functii.size(); i++) {
        parsfunctieDFA(linii_functii[i], dfa_ptr);
    }

    return true;
}
