#!/usr/bin/env python3

from argparse import  ArgumentParser


def getArgs():
    parser = ArgumentParser(prog='lgit', usage='./lgit.py <command> [optional] [<arg>]')
    sub_parsers = parser.add_subparsers(title='There are common Git commands used',
                                        dest='command', metavar="command")

    init = sub_parsers.add_parser('init', usage='usage: ./lgit.py init [<directory>]',
                                  help='Create an empty Git repository or reinitialize an existing one')
    init.add_argument('directory', nargs='?', help="Destination to create directories's lgit")

    add = sub_parsers.add_parser('add',
                                 usage='./lgit.py add <file> ...',
                                 help='Add file contents to the index')
    add.add_argument('file', nargs='+',
                     help="file will be added to the index")

    status = sub_parsers.add_parser('status', usage='./lgit status',
                                    help='Show the working tree status')

    commit = sub_parsers.add_parser('commit', usage='./lgit.py commit -m <message>',
                                    help='Record changes to the repository')
    option_commit = commit.add_mutually_exclusive_group(required=True)

    option_commit.add_argument('-m', dest='message', help='commit message')

    remove = sub_parsers.add_parser('rm',
                                    usage='./lgit.py rm <file > ...',
                                    help='Remove files from the working tree and from the index')
    remove.add_argument('file', nargs='*',
                        help="file will be removed")

    config = sub_parsers.add_parser('config', usage='./lgit.py config --author <name>',
                                    help='Setting config lgit')

    option_config = config.add_mutually_exclusive_group(required=True)
    option_config.add_argument('--author', help='store information author')

    ls_files = sub_parsers.add_parser('ls-files', usage='./lgit.py ls-files',
                                      help='Show index file at current directory or subdirectory')

    log = sub_parsers.add_parser('log', usage='./lgit.py log',
                                 help='Show commit logs')
    branch = sub_parsers.add_parser('branch',
                                 usage='./lgit.py branch [<name>]',
                                 help='List or create branches')
    branch.add_argument('name', nargs='?', help="create a new branch")

    checkout = sub_parsers.add_parser('checkout',
                                    usage='./lgit.py checkout <branch>',
                                    help='Switch branches or restore working tree files')
    checkout.add_argument('branch', help="switched to branch")

    merge = sub_parsers.add_parser('merge',
                                      usage='./lgit.py merge <branch>',
                                      help='Join two or more development histories together')
    merge.add_argument('branch', help="join branch into current branch")

    stash = sub_parsers.add_parser('stash',
                                   usage='./lgit.py stash',
                                   help='Stash the current changes of current working directories')
    unstash = sub_parsers.add_parser('unstash',
                                   usage='./lgit.py unstash',
                                   help='Unstash the current changes of current working directories')
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
    return args

args = getArgs()
