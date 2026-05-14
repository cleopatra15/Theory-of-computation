# main.py
import dfa as tools

def main():
    print("Enter the path to your DFA file (Press Enter for default: 'dfa_1.txt'):")
    file_path = input().strip()
    
    if not file_path:
        file_path = "dfa_1.txt"
        
    print(f"\nReading {file_path}...")
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
    
    print("--- Successfully Loaded Data ---")
    print(f"Alphabet: {raw_alpha}")
    print(f"States: {raw_states}")
    print(f"Initial State: {initial_state}")
    print(f"Final States: {final_states}")
    print("--------------------------------")

    # ==========================================
    # NEW: Display the formatted function table!
    # ==========================================
    tools.print_transition_table(rules, raw_states, raw_alpha)

    # Keep asking for inputs until the user types 'exit'
    while True:
        print("Enter a string to test (or type 'exit' to quit):")
        user_input = input().strip()
        
        if user_input.lower() == 'exit':
            print("Exiting simulator. Goodbye!")
            break 
        
        is_accepted = tools.simulate_dfa(rules, initial_state, final_states, user_input)
        
        if is_accepted:
            print("Result: Accepted!\n")
        else:
            print("Result: Not accepted!\n")

if __name__ == "__main__":
    main()