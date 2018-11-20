from os.path import join, abspath, split
from os import rmdir, getcwd, listdir, scandir
from hashlib import sha1


def hash_sha1(file):
    '''
    Task: return hash sha1 of file passed
    '''
    return sha1(b''.join(read_file(file, mode='rb'))).hexdigest()


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


def read_file(file, mode='r'):
    with open(file, mode) as f:
        return f.readlines()


def write_file(data, file, mode='w'):
    '''
    Task: overwrite content of file from content passed
    Param:
        + data: list of string element
        + file: path of file to write
    '''
    with open(file, mode) as f:
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
        try:
            entry_direc = scandir(dir_direc.pop())
            for e in entry_direc:
                # store file in data_dir
                if e.is_file():
                    file_direc.append(rm_head_lgit(abspath(e.path)))
                # store directory in data_dir
                if e.is_dir() and ".lgit" not in e.path:
                    dir_direc.append(e.path)
        except PermissionError:
            # print("permission error ")
            pass
    return file_direc


def rm_head_lgit(path):
    return path.replace(getcwd() + "/", '')
