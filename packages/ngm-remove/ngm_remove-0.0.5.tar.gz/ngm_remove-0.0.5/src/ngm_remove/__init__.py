import sys
import argparse

from importlib.metadata import version
from ngm_remove import lib

def main():
    
    parser = argparse.ArgumentParser(description="Remove files/folders")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    # parser.add_argument("--option", help="some option", type=str, default="default_value")
    parser.add_argument("paths", nargs="*", help="Files/Folders to Remove")

    args = parser.parse_args()

    if args.version:
        print(version("ngm-remove"))
        exit(0)
    
    # args = sys.argv[1:]
    # # print(f"Args: {args}")

    argscount = len(args.paths)

    if argscount == 0:
        print("Usage: remove <path>")
        sys.exit(1)
    
    for item in args.paths:
        lib.remove(item)
