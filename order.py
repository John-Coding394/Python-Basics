print("Hello, what is your main dish?")
dish = input()
print("Ok, what side do you want?")
side = input()
print("What drink?")
drink = input()
print("Is there anything else?")
any = input().lower()  # Converting input to lowercase for easy comparison

# Initialize 'odl' to an empty string in case nothing is added
odl = ""

# Check if the user wants to add something else
if any == "yes":
    odl = input("Ok, what is it? ")
elif any == "no":
    print("Great, let's review your order.")
else:
    print("Please respond with 'yes' or 'no'.")

# Print the final order
if odl:  # If there is something in 'odl', include it in the order
    print("So your order is: " + dish + " with " + side + " and " + drink + " and " + odl)
else:
    print("So your order is: " + dish + " with " + side + " and " + drink)
