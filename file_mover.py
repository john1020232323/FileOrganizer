import shutil
import threading
import time
import sys

from category_manager import load
from pathlib import Path

def global_loading_screen(global_stop_signal):
    timed_out = not global_stop_signal.wait(timeout=5)

    if timed_out:
        print("\n==================================================")
        print("[BATCH NOTICE: Processing a very large folder...]")
        print("==================================================")
        

def file_loading_screen(file_stop_signal, filename):
    timed_out = not file_stop_signal.wait(timeout=5)

    if timed_out:
        print(f"Large file detected: {filename}")
        animation = ["|", "/", "--", "\\"]
        idx = 0
        while not file_stop_signal.is_set():
            sys.stdout.write(f"\rMoving {filename}... {animation[idx % len(animation)]}")
            sys.stdout.flush()
            idx += 1
            time.sleep(0.1)
        sys.stdout.write("\r" + " " * 40 + "\r")
        sys.stdout.flush()

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

    global_stop_signal = threading.Event()
    global_thread = threading.Thread(target=global_loading_screen, args=(global_stop_signal,))
    global_thread.start()
    try:
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
                    file_stop_signal = threading.Event()
                    file_thread = threading.Thread(target=file_loading_screen, args=(file_stop_signal, file.name))
                    file_thread.start()
                    try:
                        shutil.move(file.resolve(), destination.resolve())
                    finally:
                        file_stop_signal.set()
                        file_thread.join()
                    moved.append({file.name: 'No Extension'} if suffix == "" else {file.name: categories[suffix]})
                    break

                num += 1
                destination = new_path / "Organized" / category / f"{((file.stem).split("."))[0]}_{num}{suffix}"
    finally:
        global_stop_signal.set()
        global_thread.join()

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
