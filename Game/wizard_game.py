import pda 

ACTION_DESCRIPTIONS = {
    'n': 'Go North',
    's': 'Go South',
    'r': 'Go Right',
    'l': 'Go Left',
    'g': 'Grab item in the room',
    'u': 'Use the item at the top of your inventory stack',
    'd': 'Drop the top item from your bag'  
}

def get_room_narrative(current_state):
    narrative = ""
    if current_state == 'q0':
        narrative = "You are in your cozy dormitory. Head North into the Hallway to start your escape."
    elif current_state == 'q1':
        narrative = "You are in the dark Hallway. To the North is the Iron Gate, and beyond that, the Magical Barrier.\n" \
                    "PUZZLE HINT: Your bag is magical (LIFO - Last-In, First-Out). You will need to use an item at the Iron Gate FIRST, " \
                    "and an item at the Magical Barrier SECOND. Therefore, you must pick up the item for the Barrier FIRST so it sits at the bottom of your bag!"
    elif current_state == 'q2':
        narrative = "You are in the Library. You spot a glowing Spellbook that can break Magical Barriers! Grab (g) it."
    elif current_state == 'q3':
        narrative = "You are in the Potions Dungeon. You spot a vial of Acidic Potion that can melt Iron Gates! Grab (g) it."
    elif current_state == 'q4':
        narrative = "You stand before a massive Iron Gate. You cannot go further North until you melt it.\n" \
                    "You must Use (u) the Acidic Potion. (It must be at the top of your inventory!)"
    elif current_state == 'q5':
        narrative = "You are in the moonlit Courtyard! The melted Iron Gate is to the South. " \
                    "The final Magical Barrier is just to the North."
    elif current_state == 'q6':
        narrative = "A shimmering Magical Barrier blocks your escape. \n" \
                    "You must Use (u) the Spellbook to cast Alohomora. (It must be at the top of your inventory!)"
    
    return narrative

def print_wizard_map(current_state, inventory):
    def mark(name, state):
        player = "🧙"
        return f"{name:^14}{player}" if current_state == state else f"{name:^15}"

    book = "📘" if 'B' in inventory else "  "
    potion = "🧪" if 'P' in inventory else "  "

    print(f"""
=========================================================
                        +---------------+
                        |{mark('BARRIER', 'q6')}| <- Use Spellbook
                        +-------|-------+
                                |
                        +---------------+
                        |{mark('COURTYARD', 'q5')}|
                        +-------|-------+
                                | 
                        +---------------+
                        |{mark('IRON GATE', 'q4')}| <- Use Potion 
                        +-------|-------+
                                | 
+---------------+       +---------------+       +---------------+
|{mark('POTIONS', 'q3')}|-------|{mark('HALLWAY', 'q1')}|-------|{mark('LIBRARY', 'q2')}|
+---------------+       +-------|-------+       +---------------+
                                |
                        +---------------+
                        |{mark('DORMITORY', 'q0')}|
                        +---------------+

    Inventory Stack: {inventory}
    Items: Spellbook[{book}] | Potion[{potion}]
=========================================================
""")

def play_game(rules, initial_state):
    current_state = initial_state
    inventory = ['$']  
    
    print("\n" )
    print("WELCOME TO THE WIZARDING SCHOOL ESCAPE")
    print("Type 'exit' to quit at any time.\n")

    while True:
        print_wizard_map(current_state, inventory)

        # Updated Win Condition to q7
        if current_state == 'q7' and len(inventory) == 1 and inventory[0] == '$':
            print("\n" + "*"*60)
            print("ALOHOMORA! The magical lock opens!")
            print("You step out into the cool night air. You have escaped!")
            print("\n")
            break

        print("STORY:")
        print(get_room_narrative(current_state))
        print("-" * 50)

        print("Available actions here:")
        available_inputs = set()
        
        # Load PDA actions for this room
        if current_state in rules:
            for transition in rules[current_state]:
                input_char = transition[0]
                available_inputs.add(input_char)
                
       
        if len(inventory) > 1:
            available_inputs.add('d')
            
        if available_inputs:
            for act in available_inputs:
                desc = ACTION_DESCRIPTIONS.get(act, f"Unknown action '{act}'")
                print(f"  [{act}] - {desc}")
        else:
            print("  No actions available. You are trapped!")

        action = input("\nEnter your choice: ").strip().lower()

        if action == 'exit':
            print("Cowardly retreating to bed. Game over!")
            break

        if action == 'd' and 'd' in available_inputs:
            dropped_item = inventory.pop()
            print(f"\nYou threw away a '{dropped_item}' from your bag!")
            continue

        valid_transition = False
        
        if current_state in rules:
            for transition in rules[current_state]:
                input_char, pop_sym, push_sym, dest = transition

                if input_char == action:
                    if pop_sym == 'e' or (len(inventory) > 0 and inventory[-1] == pop_sym):
                        
                        if pop_sym != 'e':
                            inventory.pop()
                            print(f"\n Used '{pop_sym}' from inventory!")
                        if push_sym != 'e':
                            inventory.append(push_sym)
                            print(f"\n Picked up '{push_sym}'!")

                        current_state = dest
                        valid_transition = True
                        break 

        if not valid_transition:
            print(f"\nInvalid move! Either you can't go that way, or you are trying to use the wrong item from the top of your stack!")

def main():
    file_path = "wizard_pda.txt"
    print(f"Loading school map from {file_path}...\n")
    
    lines = pda.read_lines(file_path)
    if not lines:
        return

    sections = pda.group_into_sections(lines)
    raw_states = pda.get_section_data(sections, "[STATES]")
    raw_funcs = pda.get_section_data(sections, "[FUNCTION]")

    initial_state = raw_states[0] if raw_states else None
    rules = pda.parse_pda_transitions(raw_funcs)

    if rules and initial_state:
        play_game(rules, initial_state)
    else:
        print("Error reading PDA rules.")

if __name__ == "__main__":
    main()
