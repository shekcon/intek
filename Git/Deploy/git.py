#!/usr/bin/env python3

from os import mkdir, environ, scandir, getcwd, chdir
from os.path import join, getmtime, exists, isfile, isdir
from datetime import datetime
from argparse import ArgumentParser
from time import time


def hash_sha1(file):
    from hashlib import sha1
    with open(file, 'rb') as f:
        return sha1(f.read()).hexdigest()


def split_dir_file(hash_file):
    return hash_file[:2], hash_file[2:]


def get_info_index(line):
    line = line.strip().split(' ')
    # format timestamp, hash current, hash add, hash commit, path
    return  line[0], line[1], line[2], line[3], line[-1]


def map_index(files):
    '''
    return dictionary of mapping index of each file if have in index file
    '''
    file_mapping = {}
    for index, line in enumerate(read_file()):
        for f in files:
            if get_name(line) == f:
                file_mapping[f] = index
    return file_mapping


def read_file(file):
    with open(file, 'r') as f:
        return f.readlines()


def write_file(data, file):
    # data is a list of string element
    # default write index file
    with open(file, 'w') as f:
        f.writelines(data)


def get_all_name():
    data = read_file()
    files = [get_name(line) for line in data]
    return files

def move_directory(direc):
    if direc == 'lgit':
        chdir()


def create_object(files):
    for f in files:
        hash_f = hash_sha1(f)
        direc, file = split_dir_file(hash_f)
        path = join('objects', direc)
        if not exists(path):
            mkdir(path)
        file = join(path, file)
        if not exists(file):
            write_file(data=read_file(f), file=file)


def add_git(files):
    chdir(lgit_path)
    update_index(files, mode='add', mapping=map_index(files))
    create_object(files)


def get_files_src(src="."):
    dir_src = [src]
    file_src = []
    # find all path of file in src
    while dir_src:
        # take directory from src
        data_dir = scandir(dir_src.pop())
        for item in data_dir:
            # store file in data_dir
            if item.is_file():
                file_src.append(item.path.strip('./'))
            # store directory in data_dir
            if item.is_dir() and "./.lgit/" not in item.path:
                dir_src.append(item.path)
    return file_src


def print_status():
    pass


def get_unstaged_staged(file_index):
    all_files = get_files_src()
    unstaged_file = [f for f in all_files if f not in file_index]
    staged_file = []
    data_index = read_file()
    for line in data_index:
        if get_current(line) != get_add(line):
            unstaged_file.append(get_name(line))
        if get_add(line) != get_commit(line):
            staged_file.append(get_name(line))
    return staged_file, unstaged_file


def status_git():
    chdir(lgit_path)
    files = get_all_name(cwd_path)
    update_index(files, mode='status')
    staged_file, unstaged_file = get_unstaged_staged(files)




def commit_git(message):
    chdir(lgit_path)
    files = get_all_name()
    update_index(files, mode='commit')
    time_ns = format_time(time(), second=False)
    create_commit(message, time_ns, join('commits', time_ns))
    create_snapshots(files, join('snapshots', time_ns))


def create_commit(message, time_ns, path):
    # save commit message and author
    author = read_file(file='.lgit/config')[0] + '\n'
    time_s = time_ns.split('.')[0] + '\n' + '\n'
    write_file([author, time_s, message], file=path)


def create_snapshots(files, path):
    data_index = read_file()
    data_snap = []
    for index, f in enumerate(files):
        hash_com = data_index[index].split(' ')[3]
        data_snap.append(hash_com + " " + f + '\n')
    write_file(data_snap, file=path)


def update_index(files, mode, mapping=''):
    data_index = read_file('index')
    for i, file in enumerate(files):
        path = join(cwd_path, file)
        h_current = hash_sha1(path)
        if mode == 'add':
            # get index from mapping index of file
            # hash add equal hash of file right now
            # commit maybe nothing or have before
            line = mapping.get(file, -1)
            h_add = h_current
            if line != -1:
                _, _, _, h_commit, _ = get_info_index(data_index[line])
            else:
                h_commit = ''
        else:
            # index equal enunumerate coz run all name file in index file
            # hash add equal last time add of file
            # commit equal hash add if commit else still be same in last time
            line = i
            _, _, h_add, h_commit, _ = get_info_index(data_index[line])
            if mode == 'commit':
                h_commit = h_add
        # only git add maybe have file so need add new one in index file
        # else override on that line of that name file
        if line != -1:
            data_index[line] = format_index(format_time(
                getmtime(path)), h_current, h_add, h_commit, path)
        else:
            data_index.append(format_index(format_time(
                getmtime(path)), h_current, h_add, h_commit, path))
    write_file(data_index, file='index')


# TODO: haven't completed yet, need time to handle error and refactor code
def init_git():
    init = {'dir': ('objects', 'commits', 'snapshots'),
            'file': ('index', 'config')}
    if not exists(lgit_path):
        mkdir(lgit_path)
    elif isfile(lgit_path):
        print('fatal: Invalid gitfile format: ' + lgit_path)
        return
    chdir(lgit_path)
    for dir in init['dir']:
        if not exists(dir):
            mkdir(dir)
        elif isfile(dir):
            print(join(lgit_path, dir) + ": Not a directory")
    for file in init['file']:
        if not isdir(file):
            with open(file, 'x') as f:
                if file == 'config':
                    # get log name of env
                    f.write(environ.get('LOGNAME'))
        else:
            print('error: unable to mmap ' + join(lgit_path, file) + ' Is a directory')

def format_time(time, second=True):
    time = datetime.fromtimestamp(time)
    if second:
        return time.strftime('%Y%m%d%H%M%S')
    return time.strftime('%Y%m%d%H%M%S.%f')


# get string format index
def format_index(timestamp, current, add, commit, path):
    return '%s %s %s %40s %s\n' % (timestamp, current, add, commit, path)


def get_args():
    parser = ArgumentParser(prog="lgit")
    parser.add_argument('command', help="command options")
    parser.add_argument('files', nargs="*",
                        help=" Add file contents to the index")
    parser.add_argument('-m', '--message',
                        help="description about what you do")
    parser.add_argument('--author', help="set author for commit",)
    return parser.parse_args()


def main():
    global cwd_path, lgit_path
    args = get_args()
    cwd_path = getcwd()
    lgit_path = join(cwd_path, '.lgit')
    try:
        if args.command == 'init':
            init_git()
        elif args.command == 'add':
            add_git(args.files)
        elif args.command == 'status':
            status_git()
        elif args.command == 'commit':
            commit_git(args.message)
        elif args.command == 'config':
            write_file([args.author], file='config')
        else:
            print("Git: '" + args.command + "' is not a git command.")
    except NotADirectoryError:
        if args.command == 'init':
            pass
        else:
            print('error not is a git directory')

if __name__ == '__main__':
    main()
