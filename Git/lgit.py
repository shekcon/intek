#!/usr/bin/env python3

from subprocess import Popen, check_output
from subprocess import PIPE
from os import mkdir
from os import environ, getcwd
from os.path import join
from argparse import ArgumentParser


# git init
# init directory lgit
def init_git(top):
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


# working on
def get_status(top):
    try:
        with open(join(top, 'index')) as f:
            pass
    except FileNotFoundError:
        return "fatal: not a git repository (or any of the parent directories)"


# get command and option
def get_args():
        parser = ArgumentParser(prog="lgit", description=None)
        parser.add_argument('command',  metavar="command", choices=["init", 'add',
        'status', 'commit', 'checkout', 'rm', 'config'],
                           help="command options")
        parser.add_argument('file', nargs="*", help=" Add file contents to the index")
        parser.add_argument('-m', '--message',
                           help="description about what you do",
                           action="store_true")
        return rsync.parse_args()


# testing
def main():
    top = join(getcwd(), '.lgit/')
    args = get_args()
    # test git init
    if args.command == 'init':
        print(init_git(top))
    elif args.command == 'status':
        pass
    elif args.command == 'add':
        pass
    elif args.command == 'commit':
        pass
    elif args.command == 'rm':
        pass
    elif args.command == 'config':
        pass
    else:
        pass
    # test git status when don't have git directory
    # print(get_status(top))



if __name__ == '__main__':
    main()
