#pragma once
#include <string>
#include <vector>

using namespace std;

class Tranzitie {
public:
    string stare1;
    string simbol;
    string stare2;

    Tranzitie() {
        stare1 = "";
        simbol = "";
        stare2 = "";
    }

    Tranzitie(string s1, string sim, string s2) {
        stare1 = s1;
        simbol = sim;
        stare2 = s2;
    }
};

struct Sectiune {
    string nume;
    vector<string> linii;
};
