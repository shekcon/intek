#!/usr/bin/env python3
# set interpreter

import hashlib
import os
from argparse import ArgumentParser


def handle_wel_args():
    global rsync, path
    rsync = ArgumentParser(prog="rsync",
                           usage='./rsync.py [OPTIONS] SRC [SRC...] DES')
    rsync.add_argument('srcs',  nargs="+", help="source files")
    rsync.add_argument('dest', help="destination to copy file or multi files")
    rsync.add_argument('-u', '--update',
                       help="update",
                       action="store_true")
    rsync.add_argument('-c', '--checksum',
                       help="check sum no check time & size",
                       action="store_true")
    rsync.add_argument('-r', '--recursive',
                       help="resure into directory",
                       action="store_true")
    rsync = rsync.parse_args()
    path = os.getcwd()


def get_per_size_src(src):
    size_src = os.stat(src).st_size
    per = os.stat(src).st_mode
    return per, size_src


def get_atime_mtime_src(src):
    atime = os.stat(src).st_atime
    mtime = os.stat(src).st_mtime
    return atime, mtime


def change_per_atime_mtime(file, per, atime, mtime):
    os.chmod(file, per)
    os.utime(file, (atime, mtime))


def handle_path(directory, mode=1):
    """
    param: directory path of file or directory
    param: mode: - 1 is only create head of path
                 - 0 create all path
    """
    # handle get path
    if mode:
        top = os.path.split(directory)[0]
    else:
        top = directory
    if top and not os.path.exists(top):
        top = top.split('/')[::-1]
        path = ""
        # create directory from top ==> bottom
        while top:
            path = os.path.join(path, top.pop())
            if path and not os.path.exists(path):
                os.mkdir(path)


def check_sum(dest, src, size_src):
    try:
        des = os.open(dest, os.O_RDONLY)
    except PermissionError:
        os.unlink(dest)
        rewrite_content_des(dest, src)
    else:
        size_des = os.stat(dest).st_size
        md5_des = hashlib.md5(os.read(des, size_des)).hexdigest()
        src = os.open(src, os.O_RDONLY)
        md5_src = hashlib.md5(os.read(src, size_src)).hexdigest()
        os.close(des)
        os.close(src)
        return md5_src == md5_des
    return True


def get_valid_name(des, name_src):
    """
    parameter: file or directory
    if dir:
        join dir + name of source
    return path
    """
    if os.path.isdir(des) or des[-1] == "/":
        des = os.path.join(des, name_src)
    return des


def is_diff_mtime_size(des, mtime, size_src):
    mtime_des = os.stat(des).st_mtime
    size_des = os.stat(des).st_size
    return mtime != mtime_des or size_des != size_src


def is_des_newer_src(des, mtime):
    mtime_des = os.stat(des).st_mtime
    return mtime < mtime_des


def is_more_size_src(des, size_src):
    size_des = os.stat(des).st_size
    return size_des > size_src


def rewrite_content_des(file, src):
    """
    parameter: path_file
    write all content of source into destination
    return True if error
    """
    # open file
    src = os.open(src, os.O_RDONLY)
    # if des not exist, will create new one
    des = os.open(file, os.O_CREAT | os.O_RDWR)
    # read file
    result = os.read(src, 100)
    while result != b"":
        os.write(des, result)
        result = os.read(src, 100)
    os.close(src)
    os.close(des)


def write_diff_des(des, pos, content):
    """
    parameter: + des: file descriptor
               + pos: location write
               + content: data write
    """
    os.lseek(des, pos, 0)
    os.write(des, str.encode(content))


def update_diff_des(dest, src, size_src):
    """
    find different if size destination < source else rewrite des
    send different to destination
    append data missing from source
    """
    # handle size destination biggest than source
    # pass --> rewrite destination
    if is_more_size_src(dest, size_src):
        os.unlink(dest)
        rewrite_content_des(dest, src)
    else:
        # handle define
        miss_text = ""
        size_des = os.stat(dest).st_size
        # handle destination dont have permission readly or write
        try:
            des = os.open(dest, os.O_RDWR)
        except PermissionError:
            os.unlink(dest)
            rewrite_content_des(dest, src)
        else:
            src = os.open(src, os.O_RDONLY)
            # handle get data
            data_des = os.read(des, size_des).decode()
            data_src = os.read(src, size_src).decode()
            os.close(src)
            # handle find diff destination from source
            diff = {i: data_src[i] for i in range(
                len(data_des)) if data_des[i] != data_src[i]}
            # override write destination at posistion different
            for key in diff.keys():
                write_diff_des(des, key, diff[key])
            # find text missing of destination
            if len(data_src) > len(data_des):
                miss_text = data_src[len(data_des):]
            os.close(des)
            # write miss text at the end destination
            des = os.open(dest, os.O_RDWR | os.O_APPEND)
            if miss_text:
                os.write(des, str.encode(miss_text))
            os.close(des)


def is_diff_des(des, src, mtime, size_src):
    # handle option checksum
    if rsync.checksum:
        return not check_sum(des, src, size_src)
    # handle option check newer and check different
    # run option check newer:
    #       + pass --> skip check modified time & size
    #       + not pass --> check different normal
    # check different normal:
    #       + is different modified time ?
    #       + is different size ?
    # if diff: return True
    return (not (rsync.update and is_des_newer_src(des, mtime))
            and is_diff_mtime_size(des, mtime, size_src))


def handle_sym_hard(des, src):
    # create link need file not exits
    if os.path.exists(des):
        os.unlink(des)
    try:
        if os.stat(src).st_nlink > 1:
            # create hardlink
            os.link(src, des)
        else:
            link_src = os.readlink(src)
            # handle path directly of link source and destination
            os.symlink(os.path.join(os.getcwd(), link_src),
                       os.path.join(os.getcwd(), des))
    except PermissionError:
        pass


def main(des, src):
    # source is destination then skip rsync
    if des != src:
        try:
            # get information source
            per, size_src = get_per_size_src(src)
            atime, mtime = get_atime_mtime_src(src)
            # get name of source
            name_src = os.path.split(src)[1]
            des = get_valid_name(des, name_src)
            # handle source have symlink or hardlink
            if (os.path.islink(src) or os.stat(src).st_nlink > 1):
                handle_sym_hard(des, src)
            # handle file not exist
            elif not os.path.exists(des):
                rewrite_content_des(des, src)
            # handle file exist and different on destination
            elif is_diff_des(des, src, mtime, size_src):
                update_diff_des(des, src, size_src)
            # handle change permission, access time and modification time
            if os.path.exists(des):
                change_per_atime_mtime(des, per, atime, mtime)
        except PermissionError:
            print("rsync: send_files failed to open \"" + os.path.join(path, src) + "\": Permission denied (13)")


def get_files_dirs_src(src):
    dir_src = [src]
    file_src = []
    dirs_src = []
    # find all path of file in src
    while dir_src:
        # take directory from src
        data_dir = os.scandir(dir_src.pop())
        for item in data_dir:
            # store file in data_dir
            if item.is_file():
                file_src.append(item.path)
            # store directory in data_dir
            if item.is_dir():
                dir_src.append(item.path)
                dirs_src.append(item.path)
    return file_src, dirs_src


def handle_recursive(dest, src):
    files_src, dirs_src = get_files_dirs_src(src)
    # copy directory from source
    for direc in dirs_src:
        if src[-1] == '/':
            # remove directory top of path
            direc = direc[direc.index("/") + 1:]
        handle_path(os.path.join(dest, direc), mode=0)
    # rsync all files in source
    for file in files_src:
        # if the end of src is "/" then only copy content of directory
        if src[-1] == '/':
            content_src = file[file.index("/") + 1:]
            des_new = os.path.join(dest, content_src)
        else:
            des_new = os.path.join(dest, file)
        # rsync destination
        main(des_new, file)


if __name__ == "__main__":
    handle_wel_args()
    # handle destination and source
    dest = rsync.dest
    # path destination invalid --> create path
    if not os.path.exists(dest):
        # handle with many source
        # if destination not exits --> make it directory
        if len(rsync.srcs) > 1 and dest[-1] != "/":
            handle_path(dest + "/")
        else:
            handle_path(dest)
    # handle source more than 1 file or directory
    # destination need to be directory
    # if not specific --> create destination is directory
    if (len(rsync.srcs) > 1 or rsync.recursive) and os.path.isfile(dest):
        print("ERROR: destination must be a directory when copying more than 1 file")
    else:
        for src in rsync.srcs:
            if not rsync.recursive and os.path.isdir(src):
                print("skipping directory .")
            elif not os.path.exists(src):
                print("rsync: link_stat \"" + path + "/" + src + "\" failed: No such file or directory (2)")
            elif rsync.recursive and os.path.isdir(src):
                handle_recursive(dest, src)
            else:
                main(dest, src)
