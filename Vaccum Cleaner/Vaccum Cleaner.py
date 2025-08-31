#Vacuum Cleaner Homework

print("Vacuum Cleaner Shapes and Advantages:")
print("1. Circular  - Moves smoothly around furniture and tight spaces.")
print("2. Square    - Cleans edges and walls more effectively.")
print("3. Triangle  - Reaches corners better than other shapes.")
print("4. Hexagon   - Covers large open areas efficiently in honeycomb pattern.")

choice = input("\nEnter the number of the shape you want (1/2/3/4): ")

if choice == "1":
    shape = "Circular"
elif choice == "2":
    shape = "Square"
elif choice == "3":
    shape = "Triangle"
elif choice == "4":
    shape = "Hexagon"
else:
    shape = "Circular"
    print("Oops , choose an option from the given options , defaulting to Circular.")

print("\nYou chose:", shape, "Vacuum Cleaner")

print("\nType commands: start, stop, left, right, dock")
print("Type 'exit' to quit.\n")

while True:
    command = input("Enter command: ")
    
    if command == "exit":
        print(" Your room is cleaned! ")
        break
    elif command == "start":
        print(shape, "vacuum started cleaning.")
    elif command == "stop":
        print(shape, "vacuum stopped.")
    elif command == "left":
        print(shape, "vacuum moved left.")
    elif command == "right":
        print(shape, "vacuum moved right.")
    elif command == "dock":
        print(shape, "vacuum returned to dock.")
    else:
        print("Oops , choose an option from the given options.")
