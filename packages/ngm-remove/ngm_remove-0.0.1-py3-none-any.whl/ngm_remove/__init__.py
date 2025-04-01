import os
import sys
import shutil
from pathlib import Path

from remove import log

def remove(entry: str):
    path = Path(entry)
    print(entry)

    log.loginfo(entry)

    if path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)

    # if os.path.isdir(path):
    #     os.removedirs(path)
    # else:
    #     os.remove(path)

def main():
    args = sys.argv[1:]
    # print(f"Args: {args}")

    argscount = len(args)

    if argscount == 0:
        print("Usage: remove <path>")
        sys.exit(1)
    
    for item in args:
        remove(item)

if __name__ == "__main__":
    main()
