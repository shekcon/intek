#!/usr/bin/env python3
from os import chdir, environ, listdir
from os.path import exists
from subprocess import check_output, CalledProcessError


def cd_sh(args):
    if args:
        try:
            chdir(args[0])
        except FileNotFoundError:
            print("intek-sh: cd: '%s': No such file or directory" % (args[0]))
    elif environ.get('HOME', ''):
        chdir(environ['HOME'])
    else:
        print("intek-sh: cd: HOME not set")


def handle_args(args):
    if len(args) > 1:
        return args[0], args[1:]
    if not args:
        return '', ''
    return args[0], []


def export_sh(args):
    name_key, value_key = args[0].split('=')
    environ[name_key] = value_key


def unset_sh(args):
    if environ.get(args[0], ''):
        del environ[args[0]]


def printenv_sh(args):
    if environ.get(args[0], ''):
        print(environ[args[0]])


def exc_program(command, args, origin_command):
    try:
        output = check_output(["%s" % (command)] + args)
        print(output.decode(), end='')
    except CalledProcessError:
        pass
    except PermissionError:
        print("intek-sh: %s: Permission denied" % (origin_command))


def handle_check_command(command, args):
    if environ.get('PATH', ""):
        if exists(command) and (command.startswith('./') or
                                command.startswith('../')):
            exc_program(command, args, command)
            return True
        for path in environ['PATH'].split(':'):
            if exists(path):
                bin_commands = listdir(path)
                if command in bin_commands:
                    exc_program("%s/%s" % (path, command), args, command)
                    return True
    return False


def main():
    command_built = {'cd', 'printenv', 'export', 'unset'}
    try:
        while True:
            input_user = input('intek-sh$ ').strip()
            command, args = handle_args(list(filter(None,
                                                    input_user.split(' '))))
            if command in command_built:
                exec('%s(%s)' % (command + '_sh', args))
            elif command == 'exit':
                print('exit')
                break
            elif command and not handle_check_command(command, args):
                print("intek-sh: %s: command not found" % (command))
    except EOFError:
        pass


if __name__ == '__main__':
    main()
