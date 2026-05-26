#pragma once
#include <string>

using namespace std;

namespace Utils {
    inline int primul(string line) {
        for (int i = 0; i < line.length(); i++) {
            if (line[i] != ' ') return i;
        }
        return line.length();
    }

    inline int ultimul(string line) {
        for (int i = line.length() - 1; i >= 0; i--) {
            if (line[i] != ' ') return i + 1;
        }
        return 0;
    }

    inline string trim(string line) {
        int start = primul(line);
        int end = ultimul(line);
        if (start >= end) return "";
        return line.substr(start, end - start);
    }
}
