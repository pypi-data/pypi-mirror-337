import os
import sys
import shutil

from pathlib import Path
from ngm_remove import log

def remove(entry: str):
    fullpath = os.path.abspath(entry)
    path = Path(fullpath)

    if path.is_file():
        try:
            path.unlink()
            print("file:", fullpath)
            log.loginfo("file: " + fullpath)
        except Exception as e:
            print(e)

    elif path.is_dir():
        try:
            shutil.rmtree(fullpath)
            print("dir:", fullpath)
            log.loginfo("dir: " + fullpath)
        except Exception as e:
            print(e)
    
    else:
        print("not found:", fullpath)
        log.loginfo("not found: " + fullpath)
