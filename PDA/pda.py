# pda.py - simuleaza un pushdown automaton (PDA) pe baza unei descrieri dintr-un fisier

def read_lines(file_name):
    clean_lines = []
    try:
        with open(file_name, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    clean_lines.append(line)
        return clean_lines;                
    except FileNotFoundError:
        print(f"Eroare, nu a putut fi gasit fisierul {file_name}.")

def group_into_sections(lines):
    sections = {}
    current_section = ""
    for line in lines:
        if line.startswith('[') and line.endswith(']'):
            current_section = line.upper()
            sections[current_section] = []
        elif current_section:
            sections[current_section].append(line)
    return sections

def get_section_data(sections_dict, section_name):
    section_name = section_name.upper()
    if section_name in sections_dict:
        return sections_dict[section_name]
    return[]

def parse_pda_transitions(transition_lines):
    """
    tranzitiile sunt formatate: origine input, push, pop destinatie
    exemplu: q0 a, e, A, q0
    """
    rules = {}
    for line in transition_lines:
        parts = line.split()
        if len(parts) == 3:
            origin = parts[0]
            conditions = parts[1].split(',')
            dest = parts[2]

            if len(conditions) == 3:
                input_char, pop_sym, push_sym = conditions[0], conditions[1], conditions[2]

                if origin not in rules:
                    rules[origin] = []
                rules[origin].append((input_char, pop_sym, push_sym, dest))
    return rules


def simulate_pda(rules, initial_state, input_string):
    # initial pe stack avem semnul $, astfel stim ca acolo e baza si nu mai avem elemente
    initial_stack = ['$']
    return pda_branch_search(rules, initial_state, input_string, initial_stack)

def pda_branch_search(rules, current_state, remaining_input, stack):
    # exploreaza caile recursiv

    # cazul de baza: accepta stack ul gol
    if len(remaining_input) == 0 and len(stack) == 1 and stack[0] == '$':
        return True
    
    if current_state in rules:
        for transition in rules[current_state]:
            input_char, pop_sym, push_sym, dest = transition

            is_valid_epsilon = (input_char == 'e')
            is_valid_input = (len(remaining_input) > 0 and input_char == remaining_input[0])

            if is_valid_epsilon or is_valid_input:
                if pop_sym == 'e' or (len(stack) > 0 and stack[-1] == pop_sym):
                    new_stack = list(stack)

                    if pop_sym != 'e':
                        new_stack.pop()
                    if push_sym != 'e':
                        new_stack.append(push_sym)

                    next_input = remaining_input if is_valid_epsilon else remaining_input[1:]

                    if pda_branch_search(rules, dest, next_input, new_stack):
                        return True
        return False                    
