#!/usr/bin/env python3

from os import mkdir, environ, scandir, getcwd
from os.path import join, getmtime, exists
from datetime import datetime
from argparse import ArgumentParser
from time import time


def hash_sha1(file):
    from hashlib import sha1
    with open(file, 'rb') as f:
        return sha1(b''.join(map(bytes, f.readlines()))).hexdigest()


def split_dir_file(text):
    return text[:2], text[2:]


def get_name(data):
    return list(filter(None, (data.strip().split(' ')[4:])))[0]


def get_commit(data):
    return data.strip().split(' ')[3]


def map_index(files):
    '''
    return dictionary of mapping index of each file
    '''
    file_map = {}
    for i, line in enumerate(read_file()):
        for f in files:
            if get_name(line) == f:
                file_map[f] = i
    return file_map


def read_file(file='.lgit/index'):
    with open(file, 'r') as f:
        return f.readlines()


def write_file(data, file='.lgit/index'):
    # data is a list of string element
    # default write index file
    with open(file, 'w') as f:
        f.writelines(data)


def get_all_name():
    data = read_file()
    files = [get_name(line) for line in data]
    return files


def create_object(files):
    for f in files:
        hash_f = hash_sha1(f)
        direc, file = split_dir_file(hash_f)
        path = join('.lgit/objects', direc)
        if not exists(path):
            mkdir(path)
        file = join(path, file)
        if not exists(file):
            write_file(data=read_file(f), file=file)


def add_git(files):
    mapping_files = map_index(files)
    update_index(files, mode='add', mapping=mapping_files)
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
            if item.is_dir() and "/." not in item.path:
                dir_src.append(item.path)
    return file_src


def print_status():
    pass


def get_unstaged_staged(files):
    all_files = get_files_src()
    unstaged_file = [f for f in all_files if f not in files]
    staged_file = []
    data_index = read_file()
    for line in data_index:
        data = line.split(' ')
        if data[1] != data[2]:
            unstaged_file.append(get_name(line))
        if data[2] != data[3]:
            staged_file.append(get_name(line))
    return staged_file, unstaged_file


def status_git():
    files = get_all_name()
    update_index(files, mode='status')
    staged_file, unstaged_file = get_unstaged_staged(files)


def commit_git(message):
    files = get_all_name()
    update_index(files, mode='commit')
    time_ns = format_time(time(), second=False)
    create_commit(message, time_ns, join('.lgit/commits', time_ns))
    create_snapshots(files, join('.lgit/snapshots', time_ns))
    

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
    try:
        data_index = read_file()
        for i, file in enumerate(files):
            current = hash_sha1(file)
            if mode == 'add':
                # get index from mapping index of file
                # hash add equal hash of file right now
                # commit maybe nothing or have before
                index = mapping.get(file, -1)
                add = current
                commit = commit = data_index[index].split(
                    ' ')[3] if index != -1 else ''
            else:
                # index equal enunumerate coz run all name file in index file
                # hash add equal last time add of file
                # commit equal hash add if commit else still be same in last time
                index = i
                add = data_index[index].split(' ')[2]
                if mode == 'status':
                    commit = data_index[index].split(' ')[3]
                elif mode == 'commit':
                    commit = add
            # only git add maybe have file so need add new one in index file
            # else override on that line of that name file
            if index != -1:
                data_index[index] = format_index(format_time(
                    getmtime(file)), current, add, commit, file)
            else:
                data_index.append(format_index(format_time(
                    getmtime(file)), current, add, commit, file))
        write_file(data_index)
    except FileNotFoundError:
        print('error not is a git directory')


# TODO: haven't completed yet, need time to handle error and refactor code 
def init_git(top='.lgit'):
    init_git = {'dir': ('objects', 'commits', 'snapshots'),
                'file': ('index', 'config')}
    try:
        mkdir(top)
        for dir in init_git['dir']:
            mkdir(join(top, dir))
        for file in init_git['file']:
            with open(join(top, file), 'x') as f:
                if file == 'config':
                    # get name of env
                    # env | grep LOGNAME
                    f.write(environ.get('LOGNAME'))
        return 'Initialized empty Git repository'
    except FileExistsError:
        return 'Reinitialized existing Git repository'


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
    args = get_args()
    if args.command == 'init':
        init_git()
    elif args.command == 'add':
        add_git(args.files)
    elif args.command == 'status':
        status_git()
    elif args.command == 'commit':
        commit_git(args.message)
    elif args.command == 'config':
        write_file([args.author], file='.lgit/config')
    else:
        print("Git: '" + args.command + "' is not a git command.")


if __name__ == '__main__':
    main()
