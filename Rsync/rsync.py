#!/usr/bin/env python3
# set interpreter

import hashlib
import os
from argparse import ArgumentParser


def handle_wel_args():
    global rsync, path, name_src
    rsync = ArgumentParser(prog="rsync",
                           usage='./rsync.py [OPTIONS] SRC DES [DES...]')
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


def set_per_size_src():
    global per, size_src
    size_src = os.stat(rsync.src).st_size
    per = os.stat(rsync.src).st_mode


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
        path = os.path.join(path, top[count])
        try:
            os.mkdir(path)
        except BaseException:
            pass
        finally:
            count += 1


def check_sum(des):
    data = open(rsync.src, 'rb').readlines()
    result = [item.decode() for item in data]
    md5_src = hashlib.md5("".join(result).encode()).hexdigest()
    data = open(des, 'rb').readlines()
    result = [item.decode() for item in data]
    md5_des = hashlib.md5("".join(result).encode()).hexdigest()
    return md5_src == md5_des


def get_valid_name(des):
    """
    parameter: file or directory
    if dir:
        join dir + name of source
    return path
    """
    global name_src
    if os.path.isdir(des) or des[-1] == "/":
        des = os.path.join(des, name_src)
    return des


def is_diff_mtime_size(des):
    global mtime, size_src
    mtime_des = os.stat(des).st_mtime
    size_des = os.stat(des).st_size
    return mtime != mtime_des or size_des != size_src


def is_des_newer_src(des):
    global mtime
    mtime_des = os.stat(des).st_mtime
    return mtime < mtime_des


def is_more_size_src(des):
    global size_src
    size_des = os.stat(des).st_size
    return size_des > size_src


def rewrite_content_des(file):
    """
    parameter: path_file
    write all content of source into destination
    return True if error
    """
    # open file
    try:
        src = os.open(rsync.src, os.O_RDONLY)
        des = os.open(file, os.O_CREAT | os.O_RDWR)
        # read file
        result = os.read(src, 100)
        while result != b"":
            os.write(des, result)
            result = os.read(src, 100)
        return False
    except BaseException:
        return True


def write_diff_des(des, pos, content):
    """
    parameter: + des: file descriptor
               + pos: location write
               + content: data write
    """
    os.lseek(des, pos, 0)
    os.write(des, str.encode(content))


def update_diff_des(des):
    """
    find diff
    send diff to des
    add data missing from src
    return True if error
    """
    try:
        fd_des = os.open(des, os.O_RDWR)
        fd_app_des = os.open(des, os.O_RDWR | os.O_APPEND)
        add_more = ""
        des = open(des, 'rb').readlines()
        data_des = "".join([item.decode() for item in des])
        src = open(rsync.src, "rb").readlines()
        data_src = "".join([item.decode() for item in src])
        # found diff from des
        diff = {i:data_src[i] for i in range(len(data_des)) if data_des[i] != data_src[i]}
        # get data write more on des
        if len(data_src) > len(data_des):
            add_more = data_src[len(data_des):]
        # change diff from des
        for key in diff.keys():
            write_diff_des(fd_des, key, diff[key])
        # if have data write at the end of des file
        if add_more:
            os.write(fd_app_des, str.encode(add_more))
        return False
    except BaseException:
        return True


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
        print("rsync: link_stat \"" + path + "/" + rsync.src +
              "\" failed: No such file or directory (2)")
    else:
        set_per_size_src()
        set_atime_mtime_src()
        for des in rsync.dests:
            des = get_valid_name(des)
            # handle src have symlink or hardlink
            if (os.path.islink(rsync.src) or
                    os.stat(rsync.src).st_nlink > 1):
                # create link need file not exits
                if os.path.exists(des):
                    os.unlink(des)
                if os.path.islink(rsync.src):
                    link_src = os.readlink(rsync.src)
                    # handle path directly of link src and des
                    os.symlink(os.path.join(os.getcwd(), link_src),
                               os.path.join(os.getcwd(), des))
                else:
                    # create hardlink
                    try:
                        os.link(rsync.src, des)
                    except BaseException:
                        # path_des = os.path.split(des)[0]
                        # os.chmod(path_des, int("755", 8))
                        # os.link(rsync.src, des)
                        pass
            # handle file not exist
            elif not os.path.exists(des):
                rewrite_content_des(des)
            # handle file exist
            else:
                diff = False
                error = False
                # handle option checksum
                if rsync.checksum and not check_sum(des):
                    diff = True
                else:
                    # handle option check newer and check diff
                    # run option check newer:
                    #       + pass: skip check mtime & size
                    #       + check diff normal
                    # check diff normal:
                    #       + is diff mtime
                    #       + is diff size
                    # if diff: diff = True
                    if (not (rsync.update and is_des_newer_src(des))
                            and is_diff_mtime_size(des)):
                        diff = True
                if diff:
                    # handle size des > src
                    # then rewrite des
                    if is_more_size_src(des):
                        os.unlink(des)
                        error = rewrite_content_des(des)
                    else:
                        error = update_diff_des(des)
                # handle error when cann't read src
                if error:
                    print("rsync: send_files failed to open \"" +
                          os.path.join(path, rsync.src) + "\": Permission denied (13)")
            # handle change per atime mtime
            change_per_atime_mtime(des)
