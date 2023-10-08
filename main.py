import argparse
from pathlib import Path
from shutil import copyfile
from tqdm import tqdm
import logging
import sys
import time
import threading



# --- Частина для потоків ---

# Парсер аргументів командного рядка
parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")
args = vars(parser.parse_args())
source = Path(args.get("source"))
output = Path(args.get("output"))

# Функція, яка повертає список підкаталогів
def grabs_folder(path: Path) -> list[Path]:
    folders = []
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            inner_dir = grabs_folder(el)
            if len(inner_dir):
                folders = folders + inner_dir
    return folders

# Функція копіювання файлів
def copy_file(path: Path) -> None:
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix[1:]
            ext_folder = output / ext
            try:
                ext_folder.mkdir(exist_ok=True, parents=True)
                copyfile(el, ext_folder / el.name)
            except OSError as err:
                logging.error(err)
                sys.exit(1)

# Головна частина
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")

    folders = [source, *grabs_folder(source)]

    def thread_copy_file(path):
        for el in path.iterdir():
            if el.is_file():
                ext = el.suffix[1:]
                ext_folder = output / ext
                try:
                    ext_folder.mkdir(exist_ok=True, parents=True)
                    copyfile(el, ext_folder / el.name)
                except OSError as err:
                    logging.error(err)
                    sys.exit(1)

# Використовуємо tqdm для створення прогрес-бару
    for folder in tqdm(folders, desc="Copying files"):
        thread = threading.Thread(target=thread_copy_file, args=(folder,))
        thread.start()
        thread.join()

    print(f"Можна видалять {source}")


# --- Частина для процесів ---
from factorize import parallel_factorize

if __name__ == "__main__":
    start_time = time.time()

    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")

if __name__ == '__main__':
    a, b, c, d = parallel_factorize([128, 255, 99999, 10651060])

    print("a:", a)
    print("b:", b)
    print("c:", c)
    print("d:", d)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,1521580, 2130212, 2662765, 5325530, 10651060]

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Час виконання: {execution_time} секунд")