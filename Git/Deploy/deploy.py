#!/usr/bin/env python3
from os.path import join
import os

def format_path(path, mode):
    cwd_path = '/home/shekcon/Intek/Git/Deploy/test/f1' + path 
    # os.chdir(cwd_path)
    lgit = '/home/shekcon/Intek/Git/Deploy'
    # cwd = cwd_path
    if mode == 'add':
        path = os.path.abspath(cwd_path)
        print(path)
        path = path.replace(lgit + "/", "")
        if lgit not in path:
            print('dawdaw')
        print(path)
    elif mode == 'status':
        return relpath(join(getcwd(), path), start=cwd_path)


format_path('/*', 'add')