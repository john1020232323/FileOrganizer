import shutil
from category_manager import load
from pathlib import Path

def create_folder(path, choice):
    categories = load()
    for v in set(categories.values()):
        target = Path(path / "Organized" / v)
        target.mkdir(parents=True, exist_ok=True)
    if choice == 'y':
        target = Path(path / "Organized" / "No Extension")
        target.mkdir(parents=True, exist_ok=True)


def move(new_path, source, choice):
    categories = load()
    create_folder(new_path, choice)
    moved = []

    for file in source.iterdir():
        if not file.is_file():
            continue

        suffix = "".join(file.suffixes)
        if suffix not in categories and (suffix != "" or choice == "n"):
            continue    
        num = 1

        while True:
            category = "No Extension" if suffix == "" and choice == "y" else categories.get(suffix, "Unknown")
            if num == 1:
                destination = new_path / "Organized" / category / file.name
            if not destination.resolve().exists():
                shutil.move(file.resolve(), destination.resolve())
                moved.append({file.name: 'No Extension'} if suffix == "" else {file.name: categories[suffix]})
                print(f"Moved: {file.name}")
                break

            num += 1
            destination = new_path / "Organized" / category / f"{((file.stem).split("."))[0]}_{num}{suffix}"

    result(moved, new_path)


def result(moved, new_path):
    print(f"\nDestination path: {new_path}")
    for i, item in enumerate(moved, 1):
        for k, v in item.items():
            print(f"{i}. {k} -> {v}")

def destination(source, choice):
    while True:
        destination = input("\nDestination Path (q to exit): ").strip()
        if destination == 'q':
            break
        new_path = Path(destination)
        if not new_path.exists() or not new_path.is_dir():
            print("Path/Directory does not exists")
            continue
        else:
            move(new_path, source, choice)
            return True
