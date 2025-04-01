import os
import sys
import shutil

from pathlib import Path
from ngm_remove import log


def remove(entry: str):
    path = Path(entry)

    if path.is_file():
        path.unlink()
        print("file:", entry)
        log.loginfo("file: " + entry)

    elif path.is_dir():
        shutil.rmtree(path)
        print("dir:", entry)
        log.loginfo("dir: " + entry)
    
    else:
        print("not found:", entry)
        log.loginfo("not found: " + entry)
