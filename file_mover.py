import shutil
from category_manager import load
from pathlib import Path

def create_folder(path):
    categories = load()
    for v in set(categories.values()):
        target = Path(path / "Organized" / v)
        target.mkdir(parents=True, exist_ok=True)


def move(new_path, source):
    categories = load()
    create_folder(new_path)
    moved = []

    for file in source.iterdir():
        if not file.is_file():
            continue

        suffix = "".join(file.suffixes)
        if suffix not in categories.keys():
            continue
        
        num = 1
        destination = new_path / "Organized" / categories.get(suffix, "Unknown") / file.name

        while True:
            num += 1
            if file.is_file() and not destination.resolve().exists():
                shutil.move(file.resolve(), destination.resolve())
                moved.append({file.name: categories[suffix]})
                print(f"Moved: {file.name}")
                break

            destination = new_path / "Organized" / categories.get(suffix, "Unkown") / f"{((file.stem).split("."))[0]}_{num}{suffix}"             
    result(moved, new_path)


def result(moved, new_path):
    print(f"\nDestination path: {new_path}")
    for i, item in enumerate(moved, 1):
        for k, v in item.items():
            print(f"{i}. {k} -> {v}")

def destination(source):
    while True:
        destination = input("Destination Path (q to exit): ").strip()
        if destination == 'q':
            break
        new_path = Path(destination)
        if not new_path.exists() or not new_path.is_dir():
            print("Path/Directory does not exists")
            continue
        else:
            move(new_path, source)
            return True
