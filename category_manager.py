import re
import csv

def load():
    try:
        with open('category.csv', 'r') as file:
            reader = csv.DictReader(file)
            categories = {row['extension']: row['category'] for row in reader}
            return categories
    except FileNotFoundError:
        return {}

def display():
    categories = load()
    print("\nCATEGORIES AND FOLDER:")
    for i, (k, v) in enumerate(categories.items(), 1):
        print(f'{i}. {k} ---> {v}')

def menu():
    while True:
        print("=========================================================")
        categories = load()
        if not categories:
            print("\nNo extensions added yet")
            if not confirm():
                break
        else:
            display()
            if not confirm():
                break

def add():
    categories = load()
    while True:
        try:
            ext = input("\nExtension (q to exit): ").strip()
            if ext == "q":
                break
            validate_ext(ext)
            folder = input("Folder: ").title().strip()
        except ValueError as e:
            print(e)
        else:
            categories[ext] = folder
            save(categories)
            display()

def validate_ext(ext):
    if re.findall(r"^(?:[\w-]+\.?)+$", ext):
        raise ValueError("Must start with a dot")
    elif not re.findall(r"^(?:\.[\w-]+)+$", ext):
        raise ValueError("Contains weird characters or combinations")
    if ext in load().keys():
        raise ValueError(f"{ext} already in the list")

def save(categories):
    ext = [{'extension': k, 'category': v} for k, v in categories.items()]
    with open('category.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['extension', 'category'])
        writer.writeheader()
        writer.writerows(ext)
    print("Saved successfully")

def confirm():
    action = choose_action()
    if not action:
        return False
    else:
        while True:
            choice = input(f"{action.__name__.title()} extension (Y/N)? ").lower().strip()
            if choice == 'y':
                action()
                return True
            elif choice == "n":
                break
            else:
                print("Must be Y or N")

def choose_action():
    while True:
        print("""
1. Add
2. Delete
3. Exit
""")    
        try:
            choice = input("Choice: ").strip()
            if choice not in ['1', '2', '3']:
                raise ValueError("Must be 1, 2, and 3")
            if choice == '3':
                return False
        except ValueError as e:
            print(e)
        else:
            if int(choice) == 1:
                return add
            else:
                return delete

def delete():
    if not load():
        print("No extensions added yet")
        return 
    while True:
        categories = {i: {k: v} for i, (k, v) in enumerate(load().items(), 1)}
        try:
            toDelete = input("ID to delete (q to exit): " ).strip()
            if toDelete == "q":
                break
            elif toDelete not in str(categories.keys()):
                raise ValueError("Error: ID not in the list")
        except ValueError as e:
            print(e)
        else:
            new_categories = {ky: vl for k, v in categories.items() if k != int(toDelete) for ky, vl in v.items()}
            save(new_categories)
            display()
