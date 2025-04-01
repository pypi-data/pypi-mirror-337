import sys
from ngm_remove import lib

def main():
    args = sys.argv[1:]
    # print(f"Args: {args}")

    argscount = len(args)

    if argscount == 0:
        print("Usage: remove <path>")
        sys.exit(1)
    
    for item in args:
        lib.remove(item)
