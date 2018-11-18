def READY_COMMITTED():
    print("Changes to be committed:\n\
(use \"./lgit.py reset HEAD ...\" to unstage)\n")


def TRACKED_MODIFIED():
    print("Changes not staged for commit:\n\
(use \"./lgit.py add ...\" to update what will be committed)\n\
(use \"./lgit.py checkout -- ...\" to discard changes \
in working directory)\n")


def UNTRACKED_FILE():
    print("Untracked files:\n\
(use \"./lgit.py add <file>...\" to include in what will be committed)\n")


def NO_ADDED_BUT_UNTRACKED():
    print("nothing added to commit but untracked files\
present (use \"./lgit.py add\" to track)")


def NO_ADDED_TO_COMMIT():
    print('no changes added to commit')


def BRANCH_NOW(branch):
    print('On branch %s\n' % (branch))


def NO_COMMITS_YET():
    print("No commits yet\n")
