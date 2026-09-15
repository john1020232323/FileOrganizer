from category_manager import load
from file_mover import destination
from pathlib import Path

def dir_details():
    categories = load()
    path = get_path()
    if not path:
        return
    files = {
        'numfiles': 0,
        'unsupported': [],
        'folders': [],
        'supported': [],
    }
    for sub in path.iterdir():
        suffix = "".join(sub.suffixes)
        files['numfiles'] += 1
        if sub.is_dir():
            files["folders"].append(sub.name)
        elif sub.is_file():
            if suffix in categories.keys():
                files['supported'].append(sub.name)
                continue
            files['unsupported'].append(sub.name)
    items = forloop_display(files)
    show_details(path, files, items)


def show_details(path, files, items):
    print(f'''
    =====SUMMARY=====    
    PATH: {path}
    FILES/FOLDERS: {files['numfiles']}

    FOLDERS: {len(files['folders'])}
    {items['folder'].strip()}

    UNSUPPORTED FILES FOR MOVING: {len(files['unsupported'])}
    {items['unsupported'].strip()}

    SUPPORTED FILES FOR MOVING: {len(files['supported'])}
    {items['supported'].strip()}
    ''')
    check_if_move(path)

def check_if_move(path):
    while True:
        choice = input("\nOrganize (Y/N)? ").strip().lower()
        if choice == "y":
            destination(path)
            break
        elif choice == "n":
            break

def forloop_display(files):
    items = {
        'folder': "",
        'unsupported': "",
        'supported': "",
        }
    for i, folders in enumerate(files['folders'], 1):
        items['folder'] += f"    {i}. {folders}\n"
    for i, unsupported in enumerate(files['unsupported'], 1):
        items['unsupported'] += f"    {i}. {unsupported}\n"
    for i, supported in enumerate(files['supported'], 1):
        items['supported'] += f"    {i}. {supported}\n"
    return items
    
def get_path():
    while True:
        path = Path(input("PATH ('q' to exit): "))
        if str(path).lower().strip() == "q":
            return False
        if path.is_dir():
            return path
        else:
            print(path, "not found or is not a valid directory/folder")
        
              
def test():
    print("This runs!")