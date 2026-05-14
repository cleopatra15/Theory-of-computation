# dfa_tools.py

def read_clean_lines(file_name):
    """Reads the file and removes empty lines and spaces."""
    clean_lines = []
    try:
        with open(file_name, 'r') as f:
            for line in f:
                line = line.strip()
                # Ignore empty lines and comments
                if line and not line.startswith('#'):
                    clean_lines.append(line)
        return clean_lines
    except FileNotFoundError:
        print(f"Error: Could not find '{file_name}'")
        return []

def group_into_sections(lines):
    """Groups the flat list of lines into a dictionary of sections based on [headers]."""
    sections = {}
    current_section = ""
    
    for line in lines:
        if line.startswith('[') and line.endswith(']'):
            current_section = line.lower() # e.g., '[stari]'
            sections[current_section] = []
        elif current_section:
            sections[current_section].append(line)
            
    return sections

def get_section_data(sections_dict, section_name):
    """Retrieves the list of items for a specific section."""

    section_name = section_name.lower()
    if section_name in sections_dict:
        return sections_dict[section_name]
    return []

def parse_transitions(transition_lines):
    """
    Turns a list of strings like "(q0,0)-q0" into a nested dictionary.
    No binary search needed! Lookups will be instant.
    """
    rules = {}
    for line in transition_lines:
   
        clean_line = line.replace('(', '').replace(')', '')
        
      
        left_side, dest_state = clean_line.split('-')
        
     
        origin_state, symbol = left_side.split(',')
        
     
        if origin_state not in rules:
            rules[origin_state] = {}
        if symbol not in rules[origin_state]:
            rules[origin_state][symbol] = []
            
        # Append to a list so this perfectly supports NFAs later
        rules[origin_state][symbol].append(dest_state)
        
    return rules

def print_transition_table(rules, states, alphabet):
    """Prints the transition rules as a formatted table."""
    

    header = f"{'State':<10} | " + " | ".join([f"{sym:<10}" for sym in alphabet])
    
    print("\n" + "=" * len(header))
    print("TRANSITION TABLE")
    print("-" * len(header))
    print(header)
    print("-" * len(header))

    # Create a row for each state
    for state in sorted(states):
        row_string = f"{state:<10} | "
        
        for sym in alphabet:
            # Check if this state has a transition for this symbol
            if state in rules and sym in rules[state]:

                destinations = ",".join(rules[state][sym])
                row_string += f"{destinations:<10} | "
            else:

                row_string += f"{'-':<10} | "
                
        print(row_string)
        
    print("=" * len(header) + "\n")

def simulate_dfa(rules, initial_state, final_states, input_string):
    """Runs the logic to test a string."""
    current_state = initial_state
    
    for symbol in input_string:

        if current_state in rules and symbol in rules[current_state]:

            current_state = rules[current_state][symbol][0]
        else:
           
            print(f"No transition found for state {current_state} with symbol '{symbol}'.")
            return False
            
    return current_state in final_states
