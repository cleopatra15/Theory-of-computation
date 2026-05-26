#pragma once
#include <vector>
#include <string>
#include <iostream>
#include "Structuri.h"

using namespace std;

class DFA {
public:
    vector<string> sigma;
    vector<string> stari;
    string stare_finala;
    string stare_initiala;
    vector<Tranzitie> functie_tranzitie;

    DFA() {
        stare_finala = "";
        stare_initiala = "";
    }

    string cautaTranzitie(string st, string sim);
    void afisare();
    bool testeazaCuvant(string cuvant);
};
