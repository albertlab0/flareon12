import sys

def parse_state_machine(filepath):
    """
    Reads the input file and builds a graph representation of the state machine.

    Args:
        filepath (str): The path to the input file.

    Returns:
        dict: A dictionary where keys are 'from' states and values are another
              dictionary mapping a transition character to a 'to' state.
              e.g., { '0': {'J': '2', 'K': '3'}, '2': {'A': '5'} }
    """
    graph = {}
    try:
        with open(filepath, 'r') as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                
                parts = [p.strip() for p in line.split(',')]
                if len(parts) != 3:
                    print(f"Warning: Skipping malformed line {i+1}: '{line}'")
                    continue
                
                from_state, transition, to_state = parts
                
                # Ensure the from_state key exists
                if from_state not in graph:
                    graph[from_state] = {}
                
                # Add the transition
                graph[from_state][transition] = to_state
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        sys.exit(1)
        
    return graph

def find_all_chains(graph, target_length):
    """
    Finds all valid chains of a specific length in the state machine.

    Args:
        graph (dict): The state machine graph.
        target_length (int): The exact length of the chains to find.

    Returns:
        list: A list of strings, where each string is a valid chain.
    """
    valid_chains = []

    def find_paths_recursive(current_state, current_path):
        """A recursive helper function to perform the Depth-First Search."""
        
        # --- Base Case: Success ---
        # If the path is the desired length, check if it's a valid end state.
        if len(current_path) == target_length:
            # An "end state" is one that has no outgoing transitions.
            # i.e., it is not a key in the main graph dictionary.
            if current_state not in graph:
                valid_chains.append(current_path)
            return # Stop searching this branch, whether it's a solution or not.

        # --- Pruning / Dead End ---
        # If we are at a state with no outgoing transitions, but our path is
        # too short, this path is a dead end.
        if current_state not in graph:
            return

        # --- Recursive Step ---
        # Explore all possible transitions from the current state.
        for transition_char, next_state in graph[current_state].items():
            find_paths_recursive(next_state, current_path + transition_char)

    # --- Initial Calls ---
    # We must start the search from every possible state that has an
    # outgoing transition (i.e., every key in our graph).
    start_states = list(graph.keys())
    print(f"Starting search from {len(start_states)} possible start states...")

    for state in start_states:
        find_paths_recursive(state, "")

    return valid_chains

if __name__ == "__main__":
    # --- Configuration ---
    TARGET_CHAIN_LENGTH = 16
    
    if len(sys.argv) != 2:
        print("Usage: python find_chains.py <input_file_path>")
        sys.exit(1)
        
    input_file = sys.argv[1]

    print("Step 1: Parsing the state machine definition...")
    state_machine = parse_state_machine(input_file)
    if not state_machine:
        print("Could not parse the state machine. Exiting.")
        sys.exit(1)
    
    print(f"Step 2: Finding all chains of length {TARGET_CHAIN_LENGTH}...")
    found_chains = find_all_chains(state_machine, TARGET_CHAIN_LENGTH)

    print("\n--- Results ---")
    if found_chains:
        print(f"Found {len(found_chains)} valid chains of length {TARGET_CHAIN_LENGTH}:")
        for chain in found_chains:
            print(chain)
    else:
        print(f"No valid chains of length {TARGET_CHAIN_LENGTH} were found.")
