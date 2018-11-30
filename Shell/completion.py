import os


def show_suggest(txt):
    print('\n'.join(get_suggest(txt)))


def get_suggest(txt):
    commands = []
    for path in os.environ['PATH'].split(':'):
        if os.path.exists(path):
            commands += os.listdir(path)
    auto = []
    for com in commands:
        if com.startswith(txt):
            auto.append(com)
    return auto


def handle_completion(txt):
    list_suggest = get_suggest(txt)
    if not list_suggest:
        return txt
    elif len(list_suggest) is 1:
        return list_suggest[0]
    min_command = min(list_suggest, key=lambda o: len(o))
    if min_command != len(txt):
        index = len(txt)
        max_command = max(list_suggest)
        while True:
            for e in list_suggest:
                if not e.startswith(max_command[:index + 1]):
                    return max_command[: index]
            index += 1
    return txt




if __name__ == '__main__':
    print(handle_completion('e'))