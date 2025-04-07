# Define menu items and their prices
menu = {
    "main_dishes": {
        "burger": 8.99,
        "pizza": 12.99,
        "salad": 7.99,
        "pasta": 10.99
    },
    "sides": {
        "fries": 3.99,
        "soup": 4.99,
        "salad": 4.99,
        "bread": 2.99
    },
    "drinks": {
        "soda": 2.99,
        "water": 1.99,
        "juice": 3.99,
        "tea": 2.99
    }
}

def get_valid_input(prompt, options):
    while True:
        print(prompt)
        print(f"Available options: {', '.join(options)}")
        choice = input().lower()
        if choice in options:
            return choice
        print("Invalid choice. Please try again.")

def get_price(category, item):
    return menu[category][item]

# Get main dish
dish = get_valid_input("What is your main dish?", menu["main_dishes"].keys())
dish_price = get_price("main_dishes", dish)

# Get side
side = get_valid_input("What side do you want?", menu["sides"].keys())
side_price = get_price("sides", side)

# Get drink
drink = get_valid_input("What drink?", menu["drinks"].keys())
drink_price = get_price("drinks", drink)

# Initialize additional items list
additional_items = []
additional_prices = []

# Ask for additional items
while True:
    print("Is there anything else? (yes/no)")
    response = input().lower()
    
    if response == "no":
        break
    elif response == "yes":
        print("What would you like to add? (Type 'done' when finished)")
        while True:
            item = input().lower()
            if item == "done":
                break
            if item in menu["main_dishes"] or item in menu["sides"] or item in menu["drinks"]:
                additional_items.append(item)
                if item in menu["main_dishes"]:
                    additional_prices.append(get_price("main_dishes", item))
                elif item in menu["sides"]:
                    additional_prices.append(get_price("sides", item))
                else:
                    additional_prices.append(get_price("drinks", item))
            else:
                print("Item not found in menu. Please try again.")
    else:
        print("Please respond with 'yes' or 'no'.")

# Calculate total price
total_price = dish_price + side_price + drink_price + sum(additional_prices)

# Print order summary
print("\nOrder Summary:")
print(f"Main Dish: {dish} - ${dish_price:.2f}")
print(f"Side: {side} - ${side_price:.2f}")
print(f"Drink: {drink} - ${drink_price:.2f}")
if additional_items:
    print("Additional Items:")
    for item, price in zip(additional_items, additional_prices):
        print(f"- {item} - ${price:.2f}")
print(f"\nTotal Price: ${total_price:.2f}")

# Ask for confirmation
print("\nWould you like to confirm this order? (yes/no)")
confirmation = input().lower()
if confirmation == "yes":
    print("Order confirmed! Thank you for your order.")
else:
    print("Order cancelled. Please start over if you'd like to place a new order.")
