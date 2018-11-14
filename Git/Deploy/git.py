#!/usr/bin/env python3

from os import mkdir, environ
from os.path import join, getmtime
from datetime import datetime
from argparse import ArgumentParser



def hash_sha1(file):
    from hashlib import sha1
    with open(file, 'rb') as f:
        return sha1(b''.join(map(bytes, f.readlines()))).hexdigest()


def split_dir_file(text, hash=True):
    if hash:
        return text[:2], text[2:]
    return text, text.split('.')[0]


def get_name(data):
    return list(filter(None,(data.strip().split(' ')[4:])))[0]


def get_commit(data):
    return data.strip().split(' ')[3]


def map_index(files):
    '''
    return dictionary of mapping index of each file
    '''
    file_map = {}
    for i, line in enumerate(read_file_index()):
        for f in files:
            if get_name(line) == f:
                file_map[f] = i
    return file_map
    

def read_file_index():
    with open('.lgit/index', 'r') as f:
        return f.readlines()


def write_file_index(data):
    # data is a list of string element
    with open('.lgit/index', 'w') as f:
        f.write("\n".join(map(str, data)))

def get_all_name():
    data = read_file_index()
    files = [get_name(line) for line in data]
    return files


def add_git(files):
    mapping_files = map_index(files)
    update_index(files, mode='add', mapping=mapping_files)


def status_git():
    files = get_all_name()
    update_index(files, mode='status')


def commit_git():
    files = get_all_name()
    update_index(files, mode='commit')


def update_index(files, mode, mapping=''):
    try:
        data_index = read_file_index()
        for i, file in enumerate(files):
            current = hash_sha1(file)
            if mode == 'add':
                # get index from mapping index of file
                # hash add equal hash of file right now
                # commit maybe nothing or have before
                index = mapping.get(file, -1)
                add = current
                commit = commit = data_index[index].split(' ')[3] if index != -1 else ''
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
                data_index[index] = format_index(format_time(file), current, add, commit, file)
            else:
                data_index.append(format_index(format_time(file), current, add, commit, file))
        write_file_index(data_index)
    except FileNotFoundError:
        print('error not is a git directory')


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

# TODO: working on
# def write_file(file, src):
#     try:
#         with open(file, 'w+') as f, open(src, 'r') as s:
#             f.writelines(s.readlines())
#     except BaseException:
#         return False
#     return True
# get string format timestamp


def format_time(file, second=True):
    time = datetime.fromtimestamp(getmtime(file))
    if second:
        return time.strftime('%Y%m%d%H%M%S')
    return time.strftime('%Y%m%d%H%M%S.%f')


# get string format index
def format_index(timestamp, current, add, commit, path):
    return '%s %s %s %40s %s' %(timestamp,current,add,commit,path)


def get_args():
    parser = ArgumentParser(prog="lgit")
    parser.add_argument('command',  metavar="command",
                        help="command options")
    parser.add_argument('files', nargs="*", help=" Add file contents to the index")
    parser.add_argument('-m', '--message',
                        help="description about what you do",
                        action="store_true")
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
        commit_git()
    else:
        print("Git: '" + args.command + "' is not a git command. See 'git --help'.")



if __name__ == '__main__':
    main()
