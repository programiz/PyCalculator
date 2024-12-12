# Function for addition
def add(x, y):
    return x + y

# Function for subtraction
def subtract(x, y):
    return x - y

# Main program loop
while True:
    # Ask the user for operation
    print("Select operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Exit")

    choice = input("Enter choice (1/2/3): ")

    if choice == '3':
        print("Exiting the program...")
        break

    # Get user input for numbers
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))

    # Perform the selected operation
    if choice == '1':
        print(f"{num1} + {num2} = {add(num1, num2)}")
    elif choice == '2':
        print(f"{num1} - {num2} = {subtract(num1, num2)}")
    else:
        print("Invalid input. Please try again.")
