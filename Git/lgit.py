#!/usr/bin/env python3

from subprocess import Popen, check_output
from subprocess import PIPE
from os import mkdir
from os.path import join
from argparse import Argpa



def get_cofg_name():
    ps = Popen(('env'), stdout=PIPE)
    output = check_output(('grep', 'LOGNAME'), stdin=ps.stdout)
    ps.wait()
    return output.decode().strip('LOGNAME=')


def init_git():
    global top
    init_git = {'dir': ('objects', 'commits', 'snapshots'),
                'file': ('index', 'config')}
    try:
        mkdir(top)
        for dir in init_git['dir']:
            mkdir(join(top, dir))
        for file in init_git['file']:
            with open(join(top, file), 'x') as f:
                if file == 'config':
                    f.write(get_cofg_name())
        return 'Initialized empty Git repository'
    except FileExistsError:
        return 'Reinitialized existing Git repository'

def get_status():
    global top
    try:
        with open(join(top, 'index')) as f:
            pass
    except FileNotFoundError:
        return "fatal: not a git repository (or any of the parent directories)"

def main():
    global top
    top = '.lgit/'
    # print(init_git())
    print(get_status())



if __name__ == '__main__':
    main()
