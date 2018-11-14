#!/usr/bin/env python3

from os import mkdir
from os.path import join, getmtime
from datetime import datetime


def get_args():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('file', nargs="*", help=" Add file contents to the index")
    return parser.parse_args()


def hash_sha1(file):
    from hashlib import sha1
    with open(file, 'rb') as f:
        return sha1(b''.join(map(bytes, f.readlines()))).hexdigest()


def split_dir_file(text, hash=True):
    if hash:
        return text[:2], text[2:]
    return text, text.split('.')[0]


# TODO: working on
# def write_file(file, src):
#     try:
#         with open(file, 'w+') as f, open(src, 'r') as s:
#             f.writelines(s.readlines())
#     except BaseException:
#         return False
#     return True
# get string format time


def format_time(file, second=True):
    time = datetime.fromtimestamp(getmtime(file))
    if second:
        return time.strftime('%Y%m%d%H%M%S.%f')
    return time.strftime('%Y%m%d%H%M%S')


# get string format index
def format_index(timestamp, current, add, commit, path):
    return '%s %s %s %40s %s' %(timestamp,current,add,commit,path)


def main():
    file = 'readme'
    print(format_time(file, second=False))


if __name__ == '__main__':
    main()
