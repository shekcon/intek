from argparse import ArgumentParser, _SubParsersAction
from sys import argv, exit


def handle_arguments():
    if len(argv) > 1 and is_invalid_command():
        print("lgit: '%s' is not a lgit command. See './lgit.py --help'." %
              (argv[1]))
        exit()
    else:
        # declare information what command is used
        # and description summary each purpose's command
        parser = ArgumentParser(
            prog='lgit', usage='./lgit.py <command> [optional] [<arg>]',
            description="Lgit is a lightweight version of git")
        commands = parser.add_subparsers(title='There are common '
                                         'Git commands used',
                                         dest='command', metavar="command")

        init = commands.add_parser('init',
                                   usage='usage: ./lgit.py init [<directory>]',
                                   help='Create an empty Git repository'
                                   ' or reinitialize an existing one')
        init.add_argument('dest', metavar='directory', nargs='?',
                          help="Destination to create directories's lgit")

        add = commands.add_parser('add',
                                  usage='./lgit.py add <file> ...',
                                  help='Add file contents to the index')
        add.add_argument('file', nargs='*',
                         help="file will be added to the index")

        commands.add_parser('status', usage='./lgit status',
                            help='Show the working tree status')

        commit = commands.add_parser('commit',
                                     usage='./lgit.py commit -m <message>',
                                     help='Record changes to the repository')
        commit.add_argument('-m', dest='message', help='commit message')

        remove = commands.add_parser('rm',
                                     usage='./lgit.py rm <file > ...',
                                     help='Remove files from the '
                                     'working tree and from the index')
        remove.add_argument('file', nargs='*',
                            help="file will be removed")

        config = commands.add_parser('config',
                                     usage='./lgit.py config --author <name>',
                                     help='Setting config lgit')

        config.add_argument('--author', help='store information author')

        commands.add_parser('ls-files', usage='./lgit.py ls-files',
                            help='Show index file at current directory'
                            ' or subdirectory')

        commands.add_parser('log', usage='./lgit.py log',
                            help='Show commit logs')
        branch = commands.add_parser('branch',
                                     usage='./lgit.py branch [<name>]',
                                     help='List or create branches')
        branch.add_argument('name', nargs='?', help="create a new branch")

        checkout = commands.add_parser('checkout',
                                       usage='./lgit.py checkout <branch>',
                                       help='Switch branches or restore '
                                       'working tree files')
        checkout.add_argument('branch', help="switched to branch")

        merge = commands.add_parser('merge',
                                    usage='./lgit.py merge <branch>',
                                    help='Join two or more development'
                                    ' histories together')
        merge.add_argument('branch', help="join branch into current branch")

        commands.add_parser('stash',
                            usage='./lgit.py stash',
                            help='Stash the current changes of current '
                            'working directories')
        commands.add_parser('unstash',
                            usage='./lgit.py unstash',
                            help='Unstash the current changes of current '
                            'working directories')
        # get arguments from sys.argv
        args = parser.parse_args()

        # check valid argument or not
        # invalid --> show help
        if not args.command:
            parser.print_help()
        if args.command == 'commit' and not args.message:
            show_help_subcommand(parser, 'commit')
        elif args.command == 'config' and not args.author:
            show_help_subcommand(parser, 'config')
        elif args.command == 'add' and not args.file:
            print("Nothing specified, nothing added.\n\
Maybe you wanted to say 'git add .'?")
        elif args.command == 'rm' and not args.file:
            show_help_subcommand(parser, 'rm')
        elif args.command == 'merge' and not args.branch:
            print("fatal: No remote for the current branch.")
        else:
            return args
    exit()


def show_help_subcommand(parser, command):
    # retrieve subparsers from parser
    subparsers_actions = [
        action for action in parser._actions
        if isinstance(action, _SubParsersAction)]
    # there will probably only be one subparser_action
    for subparsers_action in subparsers_actions:
        # get all subparsers and print help
        for choice, subparser in subparsers_action.choices.items():
            if choice == command:
                print(subparser.format_help())


def is_invalid_command():
    return argv[1] not in ('init', 'add', 'status', 'commit', 'rm',
                           'config', 'ls-files', 'log', 'branch',
                           'checkout', 'merge', 'stash', 'unstash')
