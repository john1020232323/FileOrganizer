import category_manager
from sys import exit
from folder_analyzer import dir_details

def main():
    while True:
        try:
            choice = menu()

            if choice == 3:
                exit("Exiting program. Goodbye <3")

        except ValueError as e:
            print(f"\n[Invalid input] {e}")
        else:
            match choice:
                case 1:
                    print("\nTHIS OPTION LET'S YOU ANALYZE A FOLDER AND DECIDE WETHER TO ORGANIZE FILES")
                    dir_details()
                case 2:
                    print("\nMANAGE EXTENSIONS")
                    category_manager.menu()
                case _:
                    print("Invalid input, must be numbers from 1 to 3 only.")


def menu():
    print(f"""
===FILE ORGANIZER===
1. Analyze Folder
2. Extensions
3. Exit
""")
    user_input = input("Choice (1-3): ").strip()
    if not user_input.isdigit():
        raise ValueError("Please enter a valid number (digits only).")

    choice = int(user_input)
    if choice not in [1,2,3]:
        raise ValueError("Please choose a number from 1 to 3.")
    
    return choice


if __name__ == "__main__":
    main()