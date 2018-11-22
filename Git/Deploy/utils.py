import os
from sys import exit as exit_program
from hashlib import sha1


def hash_sha1(file, mode='file'):
    '''
    Task: return hash sha1 of file passed
    '''
    if mode == 'file':
        return sha1(b''.join(read_file(file, mode='rb'))).hexdigest()
    return sha1(b''.join([str.encode(f) for f in file])).hexdigest()


def split_dir_file(hash_file):
    return hash_file[:2], hash_file[2:]


def remove_empty_dirs(path):
    head, _ = os.path.split(path)
    # remove directory if it empty directory
    while head:
        if os.listdir(head):
            return
        os.rmdir(head)
        head, _ = os.path.split(head)


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


def get_files_direc(direc='.', mode=''):
    '''
    Task: return list file in subdirectory passed and directory passed
    '''
    dir_direc = [direc]
    file_direc = []
    # find all path of file in src
    while dir_direc:
        # take directory from src
        try:
            direc = dir_direc.pop()
            entry_direc = os.scandir(direc)
            for e in entry_direc:
                # store file in data_dir
                if e.is_file():
                    file_direc.append(rm_head_lgit(os.path.abspath(e.path)))
                # store directory in data_dir
                if e.is_dir() and ".lgit" not in e.path:
                    dir_direc.append(e.path)
        except PermissionError:
            if mode == 'add':
                print("warning: could not open directory '%s/%s/': "
                      "Permission denied " % (os.getcwd(), direc))
                exit_program()
    return file_direc


def rm_head_lgit(path):
    return path.replace(os.getcwd() + "/", '')
