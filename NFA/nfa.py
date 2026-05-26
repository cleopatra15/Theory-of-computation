def read_clean_lines(file_name):
    """Citeste fisierul si elimina liniile goale si spatiile."""
    clean_lines = []
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Ignora liniile goale si comentariile
                if line and not line.startswith('#'):
                    clean_lines.append(line)
        return clean_lines
    except FileNotFoundError:
        print(f"Eroare: Nu s-a putut gasi '{file_name}'")
        return []

def group_into_sections(lines):
    """Grupeaza lista simpla de linii intr-un dictionar de sectiuni."""
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
    """Returneaza lista de elemente pentru o sectiune specifica."""
    section_name = section_name.lower()
    if section_name in sections_dict:
        return sections_dict[section_name]
    return []

def parse_transitions(transition_lines):
    """Transforma o lista de siruri precum '(q0,0)-q1' intr-un dictionar imbricat."""
    rules = {}
    for line in transition_lines:
        clean_line = line.replace('(', '').replace(')', '')
        left_side, dest_state = clean_line.split('-')
        origin_state, symbol = left_side.split(',')
        
        # Eliminam spatiile pentru siguranta
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
    """Afiseaza regulile de tranzitie sub forma unui tabel formatat."""
    # Adauga epsilon la antetul alfabetului daca exista oriunde in reguli
    display_alpha = list(alphabet)
    for state in rules:
        if 'ε' in rules[state] and 'ε' not in display_alpha:
            display_alpha.append('ε')

    header = f"{'Stare':<10} | " + " | ".join([f"{sym:<10}" for sym in display_alpha])
    
    print("\n" + "=" * len(header))
    print("TABEL DE TRANZITIE")
    print("-" * len(header))
    print(header)
    print("-" * len(header))

    for state in sorted(states):
        row_string = f"{state:<10} | "
        for sym in display_alpha:
            if state in rules and sym in rules[state]:
                destinations = ",".join(rules[state][sym])
                row_string += f"{destinations:<10} | "
            else:
                row_string += f"{'-':<10} | "
        print(row_string)
        
    print("=" * len(header) + "\n")

# --- LOGICA DE SIMULARE ---

def simulate_automaton(rules, initial_state, final_states, input_string):
    """Functie wrapper pentru a initia cautarea recursiva pe ramuri."""
    return branch_search(rules, initial_state, final_states, input_string, set())

def branch_search(rules, current_state, final_states, remaining_input, visited_eps):
    """Exploreaza recursiv caile una cate una, ramificandu-se."""
    
    # 1. Cazul de baza: Sirul este gol SI ne aflam intr-o stare finala
    if len(remaining_input) == 0 and current_state in final_states:
        return True

    # 2. Tip de ramificare A: Salturi Epsilon (ε)
    if current_state in rules and 'ε' in rules[current_state]:
        for dest in rules[current_state]['ε']:
            if dest not in visited_eps:
                visited_eps.add(dest)
                # Ramifica fara a consuma caractere
                if branch_search(rules, dest, final_states, remaining_input, visited_eps):
                    return True
                # Revino (backtrack) daca a esuat
                visited_eps.remove(dest)

    # 3. Tip de ramificare B: Consumarea unui caracter
    if len(remaining_input) > 0:
        symbol = remaining_input[0] 
        
        if current_state in rules and symbol in rules[current_state]:
            for dest in rules[current_state][symbol]:
                # Ramifica, trimitand restul sirului si un set curat pentru urmarirea salturilor epsilon
                if branch_search(rules, dest, final_states, remaining_input[1:], set()):
                    return True

    # 4. Fundatura (Cale gresita)
    return False
