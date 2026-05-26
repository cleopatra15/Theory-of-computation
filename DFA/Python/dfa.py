def read_clean_lines(file_name):
    """Citeste liniile dintr-un fisier, eliminand spatiile si comentariile."""
    clean_lines = []
    try:
        with open(file_name, 'r') as f:
            for line in f:
                line = line.strip()
                # CORECAT: Ne oprim daca intalnim [end]
                if line == "[end]":
                    break
                if line and not line.startswith('#'):
                    clean_lines.append(line)
        return clean_lines
    except FileNotFoundError:
        print(f"Eroare: Nu s-a gasit fisierul '{file_name}'")
        return []

def group_into_sections(lines):
    """Grupeaza liniile in sectiuni bazate pe titluri de forma [nume_sectiune]."""
    sections = {}
    current_section = ""
    
    for line in lines:
        if line.startswith('[') and line.endswith(']'):
            current_section = line.lower() 
            sections[current_section] = []
        elif current_section:
            sections[current_section].append(line)
            
    return sections

def get_section_data(sections_dict, section_name):
    """Returneaza datele dintr-o sectiune specifica, sau o lista goala daca sectiunea nu exista."""
    section_name = section_name.lower()
    if section_name in sections_dict:
        return sections_dict[section_name]
    return []

def parse_transitions(transition_lines):
    """
    Parseaza liniile de tranzitie in formatul (origine, simbol) - destinatie si returneaza un dictionar de reguli.
    """
    rules = {}
    for line in transition_lines:
        clean_line = line.replace('(', '').replace(')', '')
        
        left_side, dest_state = clean_line.split('-')
        origin_state, symbol = left_side.split(',')
        
        # CORECTAT: Eliminam spatiile in exces pentru a evita erori la cautarea tranzitiilor
        origin_state = origin_state.strip()
        symbol = symbol.strip()
        dest_state = dest_state.strip()
        
        if origin_state not in rules:
            rules[origin_state] = {}
        if symbol not in rules[origin_state]:
            rules[origin_state][symbol] = []
            
        rules[origin_state][symbol].append(dest_state)
        
    return rules

def print_transition_table(rules, states, alphabet):
    """Afiseaza o tabela de tranzitie, aratand ce stare se atinge pentru fiecare combinatie de stare si simbol."""
    
    header = f"{'State':<10} | " + " | ".join([f"{sym:<10}" for sym in alphabet])
    
    print("\n" + "=" * len(header))
    print("TRANSITION TABLE")
    print("-" * len(header))
    print(header)
    print("-" * len(header))

    for state in sorted(states):
        row_string = f"{state:<10} | "
        
        for sym in alphabet:
            # Verifica daca exista o tranzitie pentru aceasta stare si simbol
            if state in rules and sym in rules[state]:
                destinations = ",".join(rules[state][sym])
                row_string += f"{destinations:<10} | "
            else:
                row_string += f"{'-':<10} | "
                
        print(row_string)
        
    print("=" * len(header) + "\n")

def simulate_dfa(rules, initial_state, final_states, input_string):
    current_state = initial_state
    
    for symbol in input_string:
        if current_state in rules and symbol in rules[current_state]:
            current_state = rules[current_state][symbol][0]
        else:
            print(f"Nu exista tranzitie pentru starea {current_state} si simbolul '{symbol}'.")
            return False
            
    return current_state in final_states
