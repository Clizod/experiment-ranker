from os import mkdir
from os.path import join, exists

def create_directory(root:str, directories:list[str]):
    path = root
    for d in directories:
        path = join(path, d)
        if not exists(path): 
            mkdir(path)

    return path