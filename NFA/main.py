import nfa as tools

def main():
    # 1. Solicita utilizatorului numele fisierului
    print("Introduceti calea catre fisier (Apasati Enter pentru implicit: 'dfa_1.txt'):")
    file_path = input().strip()
    
    # Seteaza valoarea implicita daca utilizatorul a apasat doar Enter
    if not file_path:
        file_path = "dfa_1.txt"
        
    print(f"\nSe citeste {file_path}...")
    lines = tools.read_clean_lines(file_path)
    
    if not lines:
        return
        
    # 2. Extragerea datelor
    sections = tools.group_into_sections(lines)
    
    raw_alpha = tools.get_section_data(sections, "[sigma]")
    raw_states = tools.get_section_data(sections, "[stari]")
    raw_initial = tools.get_section_data(sections, "[stare initiala]")
    raw_finals = tools.get_section_data(sections, "[stare finala]")
    raw_funcs = tools.get_section_data(sections, "[functie]")
    
    initial_state = raw_initial[0] if raw_initial else None
    final_states = set(raw_finals)
    rules = tools.parse_transitions(raw_funcs)
    
    # 3. Afisarea datelor si a tabelului
    print("--- Datele au fost incarcate cu succes ---")
    print(f"Alfabet: {raw_alpha}")
    print(f"Stari: {raw_states}")
    print(f"Stare initiala: {initial_state}")
    print(f"Stari finale: {final_states}")
    
    tools.print_transition_table(rules, raw_states, raw_alpha)

    # 4. Bucla de testare interactiva
    while True:
        print("Introduceti un cuvant pentru testare (sau tastati 'exit' pentru a iesi):")
        user_input = input().strip()
        
        if user_input.lower() == 'exit':
            print("Se iese din simulator. La revedere!")
            break 
        
        # Testeaza sirul
        is_accepted = tools.simulate_automaton(rules, initial_state, final_states, user_input)
        
        if is_accepted:
            print(">>> Rezultat: Acceptat!\n")
        else:
            print(">>> Rezultat: Neacceptat!\n")

if __name__ == "__main__":
    main()
