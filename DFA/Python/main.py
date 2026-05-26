import dfa as tools

def main():
    print("Introduceti calea catre fisierul DFA (Apasati Enter pentru implicit: 'dfa_1.txt'):")
    file_path = input().strip()
    
    if not file_path:
        file_path = "dfa_1.txt"
        
    print(f"\nCitesc din {file_path}...")
    lines = tools.read_clean_lines(file_path)
    
    if not lines:
        return
        
    sections = tools.group_into_sections(lines)
    
    raw_alpha = tools.get_section_data(sections, "[sigma]")
    raw_states = tools.get_section_data(sections, "[stari]")
    raw_initial = tools.get_section_data(sections, "[stare initiala]")
    raw_finals = tools.get_section_data(sections, "[stare finala]")
    raw_funcs = tools.get_section_data(sections, "[functie]")
    
    initial_state = raw_initial[0] if raw_initial else None
    final_states = set(raw_finals)
    rules = tools.parse_transitions(raw_funcs)
    
    print("Am citit urmatoarele date din fisier:")
    print(f"Alfabet: {raw_alpha}")
    print(f"Stari: {raw_states}")
    print(f"Stare initiala: {initial_state}")
    print(f"Stari finale: {final_states}")
    print("\n")

    tools.print_transition_table(rules, raw_states, raw_alpha)

    while True:
        print("Introduceti un cuvant pentru testare (sau 'exit' pentru a iesi):")
        user_input = input().strip()
        
        if user_input.lower() == 'exit':
            print("Iesire...")
            break 
        
        is_accepted = tools.simulate_dfa(rules, initial_state, final_states, user_input)
        
        if is_accepted:
            print("Acceptat!\n")
        else:
            print("Nu a fost acceptat!\n")

if __name__ == "__main__":
    main()
