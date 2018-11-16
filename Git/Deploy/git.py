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
    return line[0], line[1], line[2], line[3], line[-1]


def get_name(line):
    return line.strip().split(' ')[-1]


def map_index(files):
    '''
    return dictionary of mapping line of file if have in index file
    '''
    file_mapping = {}
    for index, line in enumerate(read_file('.lgit/index')):
        name = get_name(line)
        if name in files:
            file_mapping[name] = index
    return file_mapping


def read_file(file):
    with open(file, 'r') as f:
        return f.readlines()


def write_file(data, file):
    # data is a list of string element
    # default write index file
    with open(file, 'w') as f:
        f.writelines(data)


def get_names_index():
    data = read_file('.lgit/index')
    names = [get_name(line) for line in data]
    return names


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


def handle_input(files):
    files_new = []
    for f in files:
        if isdir(f):
            sub_file = get_files_direc(f)
            files_new = files_new + sub_file
        else:
            files_new.append(f)
    return files_new


def add_git(files):
    files_new = handle_input(files)
    update_index(files, mode='add', mapping=map_index(files_new))
    create_object(files_new)


def get_files_direc(direc='.'):
    dir_direc = [direc]
    file_direc = []
    # find all path of file in src
    while dir_direc:
        # take directory from src
        entry_direc = scandir(dir_direc.pop())
        for e in entry_direc:
            # store file in data_dir
            if e.is_file():
                file_direc.append(e.path.strip('./'))
            # store directory in data_dir
            if e.is_dir() and ".lgit" not in e.path:
                dir_direc.append(e.path)
    return file_direc


def get_untracked(file_index):
    all_files = get_files_direc()
    return [f for f in all_files if f not in file_index]


def get_unstaged_staged():
    staged_file = []
    unstaged_file = []
    for line in read_file(file='.lgit/index'):
        _, h_current, h_add, h_commit, name = get_info_index(line)
        if h_current != h_add:
            unstaged_file.append(name)
        if h_add != h_commit:
            staged_file.append(name)
    return staged_file, unstaged_file


def status_git():
    file_index = get_names_index()
    update_index(file_index, mode='status')
    show_status(file_index)


# TODO: work on
def show_status(file_index):
    untracked = get_untracked(file_index)
    staged, unstaged = get_unstaged_staged()
    lists_show = ['On branch master\n\n']
    if not get_files_direc('.lgit/commits'):
        lists_show.append("No commits yet\n\n")
    if staged:
        lists_show.append("Changes to be committed:\n\
  (use \"./lgit.py reset HEAD ...\" to unstage)\n\n")
        for file in staged:
            lists_show.append("\t modified: " + file + '\n')
        lists_show.append('\n')
    if unstaged:
        lists_show.append("Changes not staged for commit:\n\
  (use \"./lgit.py add ...\" to update what will be committed)\n\
  (use \"./lgit.py checkout -- ...\" to discard changes \
in working directory)\n\n")
        for file in unstaged:
            lists_show.append("\t modified: " + file + '\n')
        lists_show.append('\n')
    if untracked:
        lists_show.append("Untracked files:\n\
  (use \"./lgit.py add <file>...\" to include in what will be committed)\n\n")
        for file in untracked:
            lists_show.append("\t" + file + '\n')
        lists_show.append('\n')
    if not get_files_direc('.lgit/commits'):
        lists_show.append("nothing added to commit but untracked files\
 present (use \"./lgit.py add\" to track)")
    print(''.join(map(str, lists_show)))


def commit_git(message):
    file_index = get_names_index()
    update_index(file_index, mode='commit')
    time_ns = format_time(time(), second=False)
    create_commit(message, time_ns)
    create_snapshot(join('.lgit/snapshots', time_ns))


def create_commit(message, time_ns):
    # save commit message and author
    author = read_file(file='.lgit/config')[0] + '\n'
    time_s = time_ns.split('.')[0] + '\n' + '\n'
    write_file([author, time_s, message], join('.lgit/commits', time_ns))


def create_snapshot(path):
    # save hash commit all of name into
    # timestamp of commit file
    data_snap = []
    for line in read_file('.lgit/index'):
        _, _, _, h_commit, name = get_info_index(line)
        data_snap.append(h_commit + " " + name + '\n')
    write_file(data_snap, file=path)


def update_index(files, mode, mapping=''):
    data_index = read_file('.lgit/index')
    for i, file in enumerate(files):
        h_current = hash_sha1(file)
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
                getmtime(file)), h_current, h_add, h_commit, file)
        else:
            data_index.append(format_index(format_time(
                getmtime(file)), h_current, h_add, h_commit, file))
    write_file(data_index, file='.lgit/index')


def init_git():
    dir = ('.lgit/objects', '.lgit/commits', '.lgit/snapshots')
    file = ('.lgit/index', '.lgit/config')
    reinit_d = [d for d in dir if not isdir(d)]
    reinit_f = [f for f in file if not isfile(f)]
    if not exists('.lgit'):
        mkdir('.lgit')
    elif isfile('.lgit'):
        print('fatal: Invalid gitfile format: .lgit')
        return
    for d in reinit_d:
        if isfile(d):
            print(join(getcwd(), dir) + ": Not a directory")
        else:
            mkdir(d)
    for f in reinit_f:
        if not isdir(f):
            open(f, 'w').close()
        else:
            print('error: unable to mmap ' + join(getcwd(), f)
                  + ' Is a directory')
    write_file(data=[environ.get('LOGNAME')], file='.lgit/config')
    if not (reinit_d or reinit_f):
        print('Git repository already initialized.')


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
            write_file([args.author + '\n'], file='.lgit/config')
        elif args.command == 'ls-files':
            # TODO: ltung working on
            print("working on")
        elif args.command == 'log':
            # TODO: ltung working on
            print("working on")
        elif args.command == 'rm':
            # TODO: ltung working on
            print("working on")
        else:
            print("Git: '" + args.command + "' is not a git command.")
    except FileNotFoundError:
        print('fatal: not a git repository (or any of the parent directories)')


if __name__ == '__main__':
    main()
