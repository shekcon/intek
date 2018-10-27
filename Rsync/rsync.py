#!/usr/bin/env python3
# set interpreter

import hashlib
import os
from argparse import ArgumentParser


def handle_wel_args():
    global rsync, path, name_src
    rsync = ArgumentParser(prog="rsync",
                           usage='./rsync.py [OPTIONS] SOURCE DESTINATION [...]')
    rsync.add_argument('src')
    rsync.add_argument('dests', metavar="dest", nargs="+")
    rsync.add_argument('-u', '--update',
                       help="update",
                       action="store_true")
    rsync.add_argument('-c', '--checksum',
                       help="check sum no check time & size",
                       action="store_true")
    rsync = rsync.parse_args()
    path = os.getcwd()
    name_src = rsync.src.split("/")[-1]


def set_per_md5_src():
    global per, md5_src
    per = os.stat(rsync.src).st_mode
    data = open(rsync.src, 'rb').readlines()
    result = [item.decode() for item in data]
    md5_src = hashlib.md5("".join(result).encode()).hexdigest()


def set_atime_mtime_src():
    global atime, mtime
    atime = os.stat(rsync.src).st_atime
    mtime = os.stat(rsync.src).st_mtime


def change_per_atime_mtime(file):
    global per, atime, mtime
    os.chmod(file, per)
    os.utime(file, (atime, mtime))


def handle_path(directory):
    # handle create path
    top = directory.split('/')
    top = top[:len(top)-1]
    path = os.getcwd()
    count = 0
    while count < len(top):
        path += "/" + top[count]
        try:
            os.mkdir(path)
        except BaseException:
            pass
        finally:
            count += 1


def check_sum(des):
    global md5_src
    data = open(des, 'rb').readlines()
    result = [item.decode() for item in data]
    md5_des = hashlib.md5("".join(result).encode()).hexdigest()
    return md5_src == md5_des


def copy_same_content_src(file):
    """
    parameter: + file or directory
    not file: create name's file as source
    copy content of source paste into destination
    return path_file
    """
    global name_src, path
    # handle get path file if file is folder
    if os.path.isdir(file) or file[-1] == "/":
        if file[-1] == "/":
            file = file + name_src
        else:
            file = file + "/" + name_src
    # open file
    src = os.open(rsync.src, os.O_RDONLY)
    des = os.open(file, os.O_CREAT | os.O_RDWR)
    # read file
    result = os.read(src, 100)
    while result != b"":
        os.write(des, result)
        result = os.read(src, 100)
    return file


if __name__ == "__main__":
    handle_wel_args()
    # check path
    # dont have create path
    for des in rsync.dests:
        if not os.path.isfile(des) or not os.path.isdir(des):
            handle_path(des)
    if os.path.isdir(rsync.src):
        print("skipping directory .")
    elif not os.path.isfile(rsync.src):
        print("rsync: \"" + path + "/" + rsync.src +
              "\" failed: No such file or directory")
    else:
        for des in rsync.dests:
            if not os.path.isfile(des):
                des = copy_same_content_src(des)
            else:
                set_per_md5_src()
                if not check_sum(des):
                    copy_same_content_src(des)
            set_atime_mtime_src()
            change_per_atime_mtime(des)
