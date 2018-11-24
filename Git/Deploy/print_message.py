class COLORS:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    UNDERLINE = '\033[4m'
    RED = "\033[1;31m"
    BLUE = "\033[1;34m"
    CYAN = "\033[1;36m"
    GREEN = "\033[3;32m"
    RESET = "\033[0;0m"
    BOLD = "\033[;1m"
    REVERSE = "\033[;7m"


def READY_COMMITTED(paths):
    print("Changes to be committed:\n\
(use \"./lgit.py reset HEAD ...\" to unstage)\n")
    print("\t %smodified: %s%s" %
          (COLORS.GREEN,
           '\n\t modified: '.join(paths), COLORS.ENDC), end='\n\n')


def TRACKED_MODIFIED(modified, deleted):
    print("Changes not staged for commit:\n\
(use \"./lgit.py add ...\" to update what will be committed)\n\
(use \"./lgit.py checkout -- ...\" to discard changes \
in working directory)\n")
    if modified:
        print("\t %smodified: %s%s" %
              (COLORS.FAIL,
               '\n\t modified: '.join(modified), COLORS.ENDC),
              end='\n')
    if deleted:
        print("\t %sdeleted: %s%s" %
              (COLORS.RED,
               '\n\t deleted: '.join(deleted),
               COLORS.ENDC), end='\n')
    print()


def UNTRACKED_FILE(paths):
    print("Untracked files:\n\
(use \"./lgit.py add <file>...\" to include in what will be committed)\n")
    print("\t%s%s%s" %
          (COLORS.FAIL, '\n\t'.join(paths), COLORS.ENDC), end='\n\n')


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
    print("error: Your local changes to the following files would \
be overwritten by checkout:\n\t%s\nPlease commit your changes or \
stash them before you switch branches.\nAborting"
          % ('\n\t'.join(paths)))


def PERMISSION_DENIED_STASH(f):
    print("error: open(\"%s\"): Permission denied\n"
          "fatal: Unable to process path %s\n"
          "Cannot save the current worktree state" % (f, f))


def NOFILE_ADDED():
    print("Nothing specified, nothing added.\n"
          "Maybe you wanted to say 'git add .'?")


def MISSING_AUTHOR():
    print('Please config author before ./lgit.py commit ...\n')
