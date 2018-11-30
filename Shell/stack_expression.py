import shlex





def main():
    st = "echo 'hello world'||echo 'leu leu'"
    lexer = shlex.shlex(st, posix=True)
    lexer.escapedquotes = "'\"`"
    print(list(lexer))
    s = shlex.shlex('~/a && b-c --color=auto || d *.py?',punctuation_chars = True)
    # print(list(shlex.shlex(st, punctuation_chars=True)))







if __name__ == '__main__':
    main()


