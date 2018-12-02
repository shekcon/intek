from os import environ
from shlex import split as split_args
from subprocess import run


def handle_logic_op(string):
    '''
    Tasks: + First get step need to do from parse command operator
           + Run command and if exit status isn't 0 and operator is 'and' then skip
           + else exit status is 0 and operator is 'or' then skip
    '''
    steps_exec = _parse_command_operator(string)
    operator = ''
    for i, step in enumerate(steps_exec):
        command = step[0]
        op = step[1]
        if _is_skip_command(i, operator) and _is_boolean_command(command[0]):

            # run command with arguments
            result = run(command)
            environ['?'] = str(result.returncode)
        operator = op


def _is_skip_command(index, operator):
    if operator == '&&':
        return index == 0 or environ['?'] == '0'
    return index == 0 or environ['?'] != '0'


def _is_boolean_command(command):
    if command == 'false':
        environ['?'] = '1'
    elif command == 'true':
        environ['?'] = '0'
    else:
        return True
    return False


def _parse_command_operator(string):
    '''
    Tasks: + Split command and logical operator into list of tuple
           + Inside tuple is command + args and logical operators after that command
           + Return list of step need to do logical operators
    '''
    commands = _split_nested_op(split_args(string))
    steps = []

    start = 0
    for i, com in enumerate(commands):
        if com == '||' or com == "&&":
            steps.append((commands[start: i], commands[i]))
            start = i + 1
        if i == len(commands) - 1:
            steps.append((commands[start:], ''))

    return steps


def _split_nested_op(commands):
    '''
    Tasks: + That will help split some nested operator into command and logical operators
           + Then return this
    '''
    new_commands = []

    for com in commands:
        if _is_nested_op(com):
            new_commands = new_commands + _handle_nested_op(com)
        else:
            new_commands.append(com)

    return new_commands


def _handle_nested_op(text):
    '''
    Tasks: + From text passed then separate into list of command or args and operators
           + Have order from text passed
    '''
    commands = []
    start = 0
    i = 0

    while i < len(text):
        if text[i] == "|" or text[i] == "&":
            if i != 0:
                commands.append(text[start: i])
                commands.append(text[i] * 2)
            else:
                commands.append(text[i] * 2)
            i = i + 1
            start = i + 1
        elif i == len(text) - 1:
            commands.append(text[start:])
        i = i + 1
    return commands


def _is_nested_op(txt):
    return txt != "||" and txt != "&&" and ("||" in txt or "&&" in txt)


handle_logic_op('false || echo "hhaha" && ls -la && echo How i this shit')
# print(_parse_command_operator("fasle || echo 'hhaha'"))
# print(handle_logic_op('ls &&ls&&ls&&ls||echo "dawdaw"'))
# handle_logic_op('ls ||ls&&ls||ls&&echo "dawdaw"')
# handle_logic_op('ls ||ls&&ls||ls&&echo "dawdaw"||   echo "dawdawdawdaw" && echo "shekcon"')