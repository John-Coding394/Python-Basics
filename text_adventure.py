# Text Adventure Game
# Simple commands: go, take, use, look, inventory, help, quit

# Define the game world
rooms = {
    'start': {
        'description': 'You are in a dimly lit room. There is a door to the north and a window to the east.',
        'exits': {'north': 'hallway', 'east': 'garden'},
        'items': ['key']
    },
    'hallway': {
        'description': 'A long hallway stretches before you. There are doors to the north and south.',
        'exits': {'south': 'start', 'north': 'treasure_room'},
        'items': ['torch']
    },
    'garden': {
        'description': 'A beautiful garden with colorful flowers. There is a door to the west.',
        'exits': {'west': 'start'},
        'items': ['flower']
    },
    'treasure_room': {
        'description': 'A room filled with gold and jewels! There is a door to the south.',
        'exits': {'south': 'hallway'},
        'items': ['treasure']
    }
}

# Game state
current_room = 'start'
inventory = []

def show_help():
    print("\nAvailable commands:")
    print("go [direction] - Move in a direction (north, south, east, west)")
    print("take [item] - Pick up an item")
    print("use [item] - Use an item")
    print("look - Look around the current room")
    print("inventory - Check your inventory")
    print("help - Show this help message")
    print("quit - Exit the game")

def look_around():
    print(f"\n{rooms[current_room]['description']}")
    if rooms[current_room]['items']:
        print("You see:", ', '.join(rooms[current_room]['items']))
    print("Exits:", ', '.join(rooms[current_room]['exits'].keys()))

def take_item(item):
    if item in rooms[current_room]['items']:
        inventory.append(item)
        rooms[current_room]['items'].remove(item)
        print(f"You took the {item}.")
    else:
        print(f"There is no {item} here.")

def use_item(item):
    if item in inventory:
        if item == 'key' and current_room == 'treasure_room':
            print("You use the key to open a hidden chest. You win!")
            return True
        else:
            print(f"You use the {item}, but nothing happens.")
    else:
        print(f"You don't have a {item}.")
    return False

def move(direction):
    global current_room
    if direction in rooms[current_room]['exits']:
        current_room = rooms[current_room]['exits'][direction]
        print(f"You go {direction}.")
        look_around()
    else:
        print("You can't go that way.")

# Start the game
print("Welcome to the Text Adventure Game!")
print("Type 'help' to see available commands.")
look_around()

# Main game loop
while True:
    command = input("\nWhat would you like to do? ").lower().split()
    
    if not command:
        continue
        
    if command[0] == 'quit':
        print("Thanks for playing!")
        break
        
    elif command[0] == 'help':
        show_help()
        
    elif command[0] == 'look':
        look_around()
        
    elif command[0] == 'inventory':
        if inventory:
            print("Your inventory:", ', '.join(inventory))
        else:
            print("Your inventory is empty.")
            
    elif command[0] == 'go' and len(command) > 1:
        move(command[1])
        
    elif command[0] == 'take' and len(command) > 1:
        take_item(command[1])
        
    elif command[0] == 'use' and len(command) > 1:
        if use_item(command[1]):
            print("Congratulations! You've won the game!")
            break
            
    else:
        print("I don't understand that command. Type 'help' for available commands.") 