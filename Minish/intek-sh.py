#!/usr/bin/env python3
from os import chdir, environ, listdir
from os.path import exists, join
from subprocess import check_output, CalledProcessError
from sys import exit as sys_exit


def cd_sh(args):
    '''
    Task:
        + Change directory to home if no argument passed
        + If HOME not set yet then --> Show message
        + Have argument passed then change directory to that
        + If not found that directory then rasie FileNotFoundError
    :param args: list
    :return:
    '''
    if args:
        chdir(args[0])
    elif environ.get('HOME', ''):
        chdir(environ['HOME'])
    else:
        print("intek-sh: cd: HOME not set")


def export_sh(args):
    '''
    Task:
        + If not argument passed then print all environment
        + Else take environment want change and value change
        + Run check long string to get right value
        + Set value for environment
    :param args: argument change environment
    :return: None
    '''
    if not args:
        print_all_env()
    else:
        name_key, value_key = args[0].split('=')
        value_key = check_long_str(args, value_key)
        environ[name_key] = value_key


def check_long_str(args, value_key):
    '''
    Testcase:   bash$ export TEST='dawdaw'
                bash$ printenv TEST
                bash$ dawdaw
                bash$ export TEST="hello wrold"
                bash$ printenv TEST
                bash$ hello world
    '''
    if ((value_key.startswith("'") and value_key.endswith("'"))
       or (value_key.startswith("\"") and value_key.endswith("\""))):
        return value_key[1:-1:]
    elif ((value_key.startswith("'"))
          or (value_key.startswith("\""))):
        match = value_key[0]
        for i in range(1, len(args)):
            if args[i].endswith(match):
                end = i
        return ' '.join([value_key[1:]] + args[1:end] + args[:-1:])
    return value_key


def unset_sh(args):
    if not args:
        print("intek-sh$ unset: not enough arguments")
    elif environ.get(args[0], ''):
        del environ[args[0]]


def print_all_env():
    for env, content in environ.items():
        print('%s=%s' % (env, content))


def printenv_sh(args):
    if not args:
        print_all_env()
    elif environ.get(args[0], ''):
        print(environ[args[0]])


def exc_program(command, args):
    output = check_output([command] + args)
    print(output.decode(), end='')


def exit_sh(args):
    print('exit')
    if args and not args[0].isdigit():
        print("intek-sh$ exit:")
    sys_exit()


def handle_args(args):
    args = list(filter(None, args.split(' ')))
    if len(args) > 1:
        return args[0], args[1:]
    if not args:
        return '', []
    return args[0], []


def handle_check_command(command, args):
    '''
    Task:
        + Check is command at current or other directory
        + Find command in path of execute file
        + Found then run command and return True
        + Return False if not found command
    :param command: command line
    :param args: argument for command
    :return: Boolean
    '''
    if exists(command) and (command.startswith('./') or
                            command.startswith('../')):
        exc_program(command, args)
        return True
    if environ.get('PATH', ""):
        for path in environ['PATH'].split(':'):
            if exists(path) and command in listdir(path):
                exc_program(join(path, command), args)
                return True
    return False


def main():
    command_built = {'cd', 'printenv', 'export', 'unset', 'exit'}
    try:
        while True:
            input_user = input('intek-sh$ ').strip()
            command, args = handle_args(input_user)
            try:
                if command in command_built:
                    exec('%s(%s)' % (command + '_sh', args))
                elif command and not handle_check_command(command, args):
                    print("intek-sh: %s: command not found" %
                          (command))
            except PermissionError:
                print("intek-sh: %s: Permission denied" %
                      (command))
            except FileNotFoundError:
                print("intek-sh: cd: '%s': No such file or directory" %
                      (args[0]))
            except CalledProcessError:
                pass
    except EOFError:
        return


if __name__ == '__main__':
    main()
