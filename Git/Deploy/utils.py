from os.path import join, listdir, abspath, scandir, split
from os import rmdir
from hashlib import sha1


def hash_sha1(file):
    '''
    Task: return hash sha1 of file passed
    '''
    with open(file, 'rb') as f:
        return sha1(f.read()).hexdigest()


def split_dir_file(hash_file):
    return hash_file[:2], hash_file[2:]


def remove_empty_dirs(path):
    head, _ = split(path)
    # remove directory if it empty directory
    while head:
        if listdir(head):
            return
        rmdir(head)
        head, _ = split(head)


def read_file(file):
    with open(file, 'r') as f:
        return f.readlines()


def write_file(data, file):
    '''
    Task: overwrite content of file from content passed
    Param:
        + data: list of string element
        + file: path of file to write
    '''
    with open(file, 'w') as f:
        f.writelines(data)


def get_files_direc(direc='.'):
    '''
    Task: return list file in subdirectory passed and directory passed
    '''
    dir_direc = [direc]
    file_direc = []
    # find all path of file in src
    while dir_direc:
        # take directory from src
        entry_direc = scandir(dir_direc.pop())
        for e in entry_direc:
            # store file in data_dir
            if e.is_file():
                path = abspath(e.path).replace(getcwd() + "/", '')
                file_direc.append(path)
            # store directory in data_dir
            if e.is_dir() and ".lgit" not in e.path:
                dir_direc.append(e.path)
    return file_direc
