#!/usr/bin/env python3

from argparse import  ArgumentParser


def getArgs():
    parser = ArgumentParser(prog='lgit.py', description=None)
    sub_parsers = parser.add_subparsers(dest='command', metavar="Subcommand" )

    init = sub_parsers.add_parser('init', usage='usage: ./lgit.py init [<directory>]',
                                  help='Create an empty Git repository or reinitialize an existing one')
    init.add_argument('directory', nargs='?', help="Destination to create directories's lgit")

    status = sub_parsers.add_parser('status', usage='./lgit status',
                                    help='Show the working tree status')

    add = sub_parsers.add_parser('add',
                                 usage='./lgit.py add <file> ...',
                                 help='Add file contents to the index')
    add.add_argument('file', nargs='*',
                     help="file will be added to the index")

    remove = sub_parsers.add_parser('rm',
                                    usage='./lgit.py rm <file > ...',
                                    help='Remove files from the working tree and from the index')
    remove.add_argument('file', nargs='*',
                        help="file will be removed")

    commit = sub_parsers.add_parser('commit', usage='./lgit.py commit -m <message>',
                                    help='Record changes to the repository')
    commit.add_argument('-m', dest='commit message')

    config = sub_parsers.add_parser('config', usage='./lgit.py config [<options>]',
                                    help='Setting config lgit')
    config.add_argument('--author', help='store information author')

    ls_files = sub_parsers.add_parser('ls-files', usage='./lgit.py ls-files',
                                      help='Show index file at current directory or subdirectory')

    log = sub_parsers.add_parser('log', usage='./lgit.py log',
                                 help='Show commit logs')
    # List or create branches
    args = parser.parse_args()
    return args

args = getArgs()
print(args)