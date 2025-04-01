import os

def exists(path: str) -> bool:
    
    if os.path.isfile(path):
        return True
    elif os.path.isdir(path):
        return True
    return False
