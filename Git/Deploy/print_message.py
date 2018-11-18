def READY_COMMITTED(paths):
    print("Changes to be committed:\n\
(use \"./lgit.py reset HEAD ...\" to unstage)\n")
    print("\t modified:", '\n\t modified: '.join(paths), end='\n\n')


def TRACKED_MODIFIED(paths):
    print("Changes not staged for commit:\n\
(use \"./lgit.py add ...\" to update what will be committed)\n\
(use \"./lgit.py checkout -- ...\" to discard changes \
in working directory)\n")
    print("\t modified:", '\n\t modified: '.join(paths), end='\n\n')


def UNTRACKED_FILE(paths):
    print("Untracked files:\n\
(use \"./lgit.py add <file>...\" to include in what will be committed)\n")
    print("\t", '\n\t'.join(paths), sep='', end='\n\n')


def NO_ADDED_BUT_UNTRACKED():
    print("nothing added to commit but untracked files\
present (use \"./lgit.py add\" to track)")


def NO_ADDED_TO_COMMIT():
    print('no changes added to commit')


def BRANCH_NOW(branch):
    print('On branch %s\n' % (branch))


def NO_COMMITS_YET():
    print("No commits yet\n")


def OUTSIDE_DIRECTORY(f):
    print("fatal: %s '%s' is outside repository" % (f, f))


def PERMISSION_DENIED_READ(f):
    print("error: open(\"%s\"): Permission denied\n\
error: unable to index file %s\nfatal: adding files failed" % (f, f))


def NOT_MATCH_FILE(f):
    print("fatal: pathspec '%s' did not match any files" % (f))


def NOTHING_TO_ADDED():
    print("Nothing specified, nothing added.\n\
Maybe you wanted to say 'git add .'?")


def ERROR_CHECKOUT(paths):
    print("error: Your local changes to the following files would be overwritten by checkout:\
\n\t%s\nPlease commit your changes or stash them before you switch branches.\nAborting"
          % ('\n\t'.join(paths)))
