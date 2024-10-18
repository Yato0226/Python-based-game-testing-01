import os
import json
from collections import Counter
import time

# File path to save the progress
SAVE_FILE = 'game_progress.json'

# Define how long 1 in-game day lasts (in seconds)
SECONDS_PER_DAY = 60 * 60 * 24  # Adjust this value for gameplay time (1 day = 86400 seconds in real-time)

# Save progress function
def save_progress(action, elapsed_time):
    # Load existing data
    data = load_progress()
    
    # Add elapsed time and action
    entry = {'elapsed_time': elapsed_time, 'action': action}
    data.append(entry)
    
    # Clean old progress (older than 3 in-game days)
    data = [entry for entry in data if entry['elapsed_time'] > elapsed_time - (SECONDS_PER_DAY * 3)]
    
    # Save to JSON
    with open(SAVE_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Load progress function
def load_progress():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as file:
            return json.load(file)
    return []

# AI Learns from past actions
def learn_from_past(progress):
    # Extract only actions from progress
    actions = [entry['action'] for entry in progress]
    
    # Count occurrences of actions in the progress
    action_counter = Counter(actions)
    
    # Suggest based on the most common action
    if action_counter:
        most_common = action_counter.most_common(1)[0][0]
        print(f"AI suggests you to: {most_common} (based on your past actions)")

# Display scenario-specific options and allow custom input, with AI suggestions
def get_choices(scenario):
    print(f"Current scenario: {scenario}")
    
    if scenario == "forest":
        print("1. Explore the forest")
        print("2. Hunt animals")
        print("3. Gather resources")
        print("4. Custom command")
    elif scenario == "town":
        print("1. Trade with merchants")
        print("2. Talk to townspeople")
        print("3. Rest at the inn")
        print("4. Custom command")
    
    choice = input("Enter your choice (or type): ")
    
    if scenario == "forest":
        if choice == "1":
            return "You explored the forest."
        elif choice == "2":
            return "You hunted some animals."
        elif choice == "3":
            return "You gathered resources."
        elif choice == "4":
            custom = input("Type your custom command: ")
            return f"You chose to: {custom}"
        else:
            return "Invalid choice."
    
    elif scenario == "town":
        if choice == "1":
            return "You traded with merchants."
        elif choice == "2":
            return "You talked to some townspeople."
        elif choice == "3":
            return "You rested at the inn."
        elif choice == "4":
            custom = input("Type your custom command: ")
            return f"You chose to: {custom}"
        else:
            return "Invalid choice."

# Analyze progress (a simple example of processing previous data)
def analyze_progress():
    progress = load_progress()
    if not progress:
        return "No previous progress found."
    
    # Simple analysis: count specific actions
    forest_count = sum(1 for entry in progress if "forest" in entry['action'])
    town_count = sum(1 for entry in progress if "town" in entry['action'])
    
    return f"You explored the forest {forest_count} times and visited the town {town_count} times."

# Main game loop
def game_loop():
    print("Welcome to the game!")
    
    # Initialize playtime
    start_time = time.time()
    
    # Load and display previous progress
    previous_progress = load_progress()
    total_playtime = sum(entry['elapsed_time'] for entry in previous_progress) if previous_progress else 0
    
    if previous_progress:
        print("Previous progress found:")
        for entry in previous_progress:
            print(f"Elapsed Time: {entry['elapsed_time']} seconds, Action: {entry['action']}")
    
    # Initialize the current scenario (e.g., start in a forest)
    current_scenario = "forest"
    
    while True:
        # Calculate elapsed time in current session
        current_elapsed_time = time.time() - start_time + total_playtime
        
        # AI learns from past progress and suggests an action
        learn_from_past(previous_progress)
        
        # Get player's choice based on the current scenario
        result = get_choices(current_scenario)
        print(result)
        
        # Save the result with the current elapsed time
        save_progress(result, current_elapsed_time)
        
        # Update the progress data
        previous_progress = load_progress()
        
        # Analyze current progress
        analysis = analyze_progress()
        print(f"Current Analysis: {analysis}")
        
        # Allow the player to change the scenario
        change_scenario = input("Do you want to change the scenario? (yes/no): ").lower()
        if change_scenario == "yes":
            current_scenario = input("Enter new scenario (forest/town): ").lower()
            if current_scenario not in ["forest", "town"]:
                print("Invalid scenario, defaulting to forest.")
                current_scenario = "forest"
        
        # Option to exit
        cont = input("Continue playing? (yes/no): ").lower()
        if cont != 'yes':
            print("Exiting game...")
            break

# Start the game
if __name__ == "__main__":
    game_loop()