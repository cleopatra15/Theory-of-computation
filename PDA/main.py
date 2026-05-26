# main.py - punctul de intrare pentru simularea PDA
import pda as tools

def main():
    print("Introduceti fisierul pentru pda: (default config.txt): ")
    file_path = input().strip()

    if not file_path:
        file_path = "config.txt"

    print(f"\n Se citeste {file_path}...")
    lines = tools.read_lines(file_path)
    if not lines:
        return

    sections = tools.group_into_sections(lines)
    raw_states = tools.get_section_data(sections, "[STATES]") 
    raw_funcs = tools.get_section_data(sections,"[FUNCTION]")

    initial_state = raw_states[0] if raw_states else None
    rules = tools.parse_pda_transitions(raw_funcs)

    print("Am incarcat cu succes informatiile din PDA. ")
    print(f"Stare initiala: {initial_state}")

    while True:
        print("Introduceti un sir: (sau tastati exit pentru a iesi): ")
        user_input = input().replace(" ","").strip()

        if user_input.lower() == 'exit':
            print("Iesire...")
            break

        is_accepted = tools.simulate_pda(rules, initial_state, user_input)

        if is_accepted:
            print("Sir acceptat! ")
        else:
            print("Sirul nu a fost acceptat! ")

if __name__ == "__main__":
    main()


