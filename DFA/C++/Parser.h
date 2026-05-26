#pragma once
#include <string>
#include <vector>
#include "DFA.h"
#include "Structuri.h"

using namespace std;

class Parser {
public:
    static vector<Sectiune> extrageSectiuni(string numeFisier);
    static vector<string> getLiniiSectiune(vector<Sectiune> sectiuni, string numeCautat);
    static bool populareDFA(vector<Sectiune> sectiuni, DFA *dfa_ptr);

private:
    static void parsfunctieDFA(string line, DFA *dfa_ptr);
};
