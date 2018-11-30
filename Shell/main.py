import curses
from completion import handle_completion



def handle_cursor(y_max, y_input):
    y_input += 10
    x = y_input // y_max
    y = y_input % y_max
    return x, y


def main():
    shell = curses.initscr()
    x, y = 0, 0
    shell.keypad(True)
    shell.addstr(x, y, "intek-sh$ ")
    x_max, y_max = shell.getmaxyx()
    key = chr(shell.getch())
    input_user = []
    y_input = 0
    while key != 'q':
        if key == 'ć':
            if input_user and y_input > 0:
                y_input -= 1
                input_user.pop(y_input)
                shell.addstr(x, y, "intek-sh$ " + ''.join(input_user) + ' ')
            x_now, y_now = handle_cursor(y_max, y_input)
            shell.move(x + x_now, y_now)
        elif key == 'Ą': # move left
            if y_input > 0:
                y_input -= 1
            x_now, y_now = handle_cursor(y_max, y_input)
            shell.move(x + x_now, y_now)
        elif key == 'ą': # move right
            if y_input < len(input_user):
                y_input += 1
            x_now, y_now = handle_cursor(y_max, y_input)
            shell.move(x + x_now, y_now)

        elif key == '\n':
            y_input = 0
            x += 1
            shell.addstr(x, y, ''.join(input_user))
            x += 1
            input_user.clear()
            shell.addstr(x, y, "intek-sh$ ")
        elif key == 'ă': # move up
            pass
        elif key == 'Ă': # move down
            pass
        elif ord(key) == 9: # tab
            auto = handle_completion(''.join(input_user))
            input_user = [i for i in auto]
            shell.addstr(x, y, "intek-sh$ " + ''.join(input_user))
            y_input = len(auto)
        elif key != '\n':
            if y_input == len(input_user):
                input_user.append(key)
            else:
                input_user.insert(y_input, key)
                shell.addstr(x, y, "intek-sh$ " + ''.join(input_user))
            y_input += 1
            x_now, y_now = handle_cursor(y_max, y_input)
            shell.move(x + x_now, y_now)
        key = chr(shell.getch())
        shell.refresh()

    curses.endwin()

if __name__ == '__main__':
    main()