#!/usr/bin/env python3

from os import environ, getcwd, chdir, remove
from os.path import join, exists, isfile, isdir, relpath, abspath, getmtime
from os import access, R_OK
from argparse import ArgumentParser
from time import time
# from get_data_lgit import get_data_object
from get_data_lgit import get_all_commits, get_pos_track, get_files_hash
from get_data_lgit import get_tracked_unstracked, get_staged_unstaged
from get_data_lgit import get_tracked_commit, get_cmit_create_b
from get_data_lgit import get_info_commit, get_branch_now, get_commit_branch
from get_data_lgit import get_modified_branch, get_all_branchs
from utils import read_file, write_file, get_files_direc, remove_empty_dirs
from utils import rm_head_lgit, hash_sha1
from update_data_lgit import update_index, update_commit_branch
from update_data_lgit import update_unstash_files
from update_data_lgit import update_branch_now, update_files_commit
from create_data_lgit import create_object, create_commit, create_info_branch
from create_data_lgit import create_branch, create_snapshot
from create_data_lgit import create_stash_files, create_structure_lgit
from format_data_lgit import format_index, format_time, format_date_log
import print_message


def merge_git(branch_m):
    '''
    Task: Merge other branch into current branch
        + Get last commit of branch merged
        + Check commit of current branch is different from other branch
        + Different then check what merge will do
        + Merge Fast forward: revert commit of other branch into current branch
          and update commit of current branch
    :param branch_m: branch is merge into current branch
    '''
    last_cmit_b = get_commit_branch(branch_m)
    if get_commit_branch() != last_cmit_b:
        if is_fast_forward(branch_m):
            print('<--------------Merge Fast-Forward-------------->')
            revert_commit(branch_m)
            update_commit_branch(last_cmit_b)
        else:
            print('<------------------Merge 3 way----------------->')
            conflict_f, create_f = check_merge_branch(last_cmit_b)
            update_files_commit(create_f)
            handle_conflict(conflict_f, branch_m)
    else:
        print("Already up to date")


# TODO: find conflict of 2 files
# def handle_conflict(files_hash, branch_m):
#     for file in files_hash.keys():
#         hash_rec, hash_mer = files_hash[file]
#         content_rec = get_data_object(hash_rec)
#         content_mer = get_data_object(hash_mer)
#         new_merge = []
#         while content_mer and content_rec:
#             line_mer, line_rec = content_mer.pop(0), content_rec.pop(0)
#             if line_mer != line_rec:
#                 new_merge.append(format_conflict(
#                     line_rec.decode(), line_mer.decode(), branch_m))
#             else:
#                 new_merge.append(line_rec.decode())
#         write_file(new_merge, file)
#     if files_hash.keys():
#         print("Merge conflict at files: \n\t%s" %
#               ('\n\t'.join(files_hash.keys())))
#
#
# def check_merge_branch(l_commit_b):
#     tracked_f_merge = get_files_hash(l_commit_b)
#     tracked_f = get_files_hash(get_commit_branch())
#     files_creates = {}
#     files_conflict = {}
#     for file in tracked_f_merge.keys():
#         if not exists(file):
#             files_creates[file] = tracked_f_merge[file]
#         elif tracked_f[file] != tracked_f_merge[file]:
#             files_conflict[file] = (tracked_f[file], tracked_f_merge[file])
#     return files_conflict, files_creates


def is_fast_forward(branch_m):
    '''
    Task: checking time commit create of 2 branch
    :param branch_m: other branch merge to current branch
    :return: Boolean
    '''
    commit_create_b = get_cmit_create_b(branch_m)
    return commit_create_b and get_commit_branch() <= commit_create_b


def get_branch_commits(branch):
    '''
    Task: find all commits of branch passed and return it
    :param branch: branch want to get all of commits
    :return: list
    '''
    commit = get_commit_branch(branch)
    commits_branch = []
    while commit:
        commits_branch.append(commit)
        _, _, commit, _ = get_info_commit(commit)
    return commits_branch


def stash_git():
    '''
    Task: Stash the current changes
        + Checking is any changes at current branch
        + Have changes then revert to last commit of current branch
        + Don't have change --> Show message
    :return: None
    '''
    modified_files = check_modified_file()
    if modified_files:
        create_stash_files(modified_files)
        revert_commit(get_branch_now())
        print('Stash the current changes')
    else:
        print('Nothing changes at all')


def unstash_git():
    print(update_unstash_files(get_branch_now()))


def branch_git(name):
    if is_invalid_branch(name):
        create_branch(name)
        create_info_branch(name)
        print("Create a new branch '%s'" % (name))
    else:
        print("fatal: A branch named '%s' already exists." % (name))


def checkout_git(branch):
    if is_invalid_branch(branch):
        print("error:patal '%s' not match any branchs known to git" % (branch))
    elif branch != get_branch_now():
        modified = check_modified_file()
        if not modified:
            revert_commit(branch)
            update_branch_now(branch)
            print("Switched to branch '%s'" % (branch))
        else:
            print_message.ERROR_CHECKOUT(
                [format_path(p, mode='relative') for p in modified])
    else:
        print("Already on '%s'" % (branch))


def revert_commit(branch):
    files_hash = get_files_hash(get_commit_branch(branch=branch))
    remove_untracked_commit(update_files_commit(files_hash))
    overwrite_index(files_hash)


def remove_untracked_commit(files_update):
    tracked, _ = get_tracked_unstracked()
    untracked_file = [f for f in tracked if f not in files_update]
    for file in untracked_file:
        remove(file)
        remove_empty_dirs(file)


def check_modified_file():
    '''
    return list file is modified at branch now
    '''
    tracked, _ = get_tracked_unstracked()
    update_index(tracked, mode='status')
    staged, unstaged = get_staged_unstaged()
    return staged + unstaged


def overwrite_index(files_hash):
    '''
    Task: overwrite index at time commit
    :param files_hash: a dictionary: key is file,
            value is hash of file at time commit
    :return: None
    '''
    data = []
    for file in files_hash.keys():
        hash_f = files_hash[file]
        data.append(format_index(format_time(getmtime(file)),
                                 hash_f, hash_f, hash_f, file))
    write_file(data, '.lgit/index')


def is_invalid_branch(branch):
    branchs = get_all_branchs()
    return branch not in branchs


def config_git(author):
    write_file(['%s\n' % (author)], file='.lgit/config')


def handle_raw_input(files_user, tracked_file=''):
    '''
    Task:
        + Return list valid file is relative with lgit directory
        + Directory --> find all of files in directory -->
                        handle input again to get valid file
        + File --> file is valid --> add it to valid files
        + Outside of lgit directory --> Show error
    Param: list of file or directory
    '''
    valid_files = []
    for file in files_user:
        path = format_path(file, mode='absolute')
        if is_inside_lgit(path):
            path = rm_head_lgit(path)
            if isdir(path):
                sub_files = get_files_direc(path)
                valid_files = valid_files + \
                    handle_raw_input(sub_files, tracked_file)
            elif path in tracked_file or is_valid_file(path, file):
                valid_files.append(path)
        else:
            print_message.OUTSIDE_DIRECTORY(file)
    return valid_files


def is_valid_file(path, file):
    '''
    Task: Return True if file is valid
        + File do not have permission to read --> Show error
        + Path does not exist --> Show error
    '''
    if exists(path) and access(path, mode=R_OK):
        return True
    elif not access(path, mode=R_OK):
        print_message.PERMISSION_DENIED_READ(file)
    else:
        print_message.NOT_MATCH_FILE(file)
    return False


def is_inside_lgit(path):
    return getcwd() in path


def add_git(files_add):
    '''
    Task:
        + Add untrack file or update unstaged file in index file
        + Store a copy of the file content in the lgit database
    '''
    files_new = handle_raw_input(files_add)
    if files_new:
        update_index(files_new, mode='add')
        create_object(files_new)
    elif not files_add:
        print_message.NOTHING_TO_ADDED()


def status_git():
    tracked, _ = get_tracked_unstracked()
    update_index(tracked, mode='status')
    show_status([f for f in tracked if not exists(f)])


def show_status(deleted_files=''):
    _, untracked = get_tracked_unstracked()
    staged, unstaged = get_staged_unstaged()
    staged = [f for f in staged if f not in deleted_files]
    unstaged = [f for f in unstaged if f not in deleted_files]
    print_message.BRANCH_NOW(get_branch_now())
    if not get_all_commits():
        print_message.NO_COMMITS_YET()
    if staged:
        print_message.READY_COMMITTED(
            [format_path(p, mode='relative') for p in staged])
    if unstaged:
        print_message.TRACKED_MODIFIED(
            [format_path(p, mode='relative') for p in unstaged])
    if deleted_files:
        print_message.TRACKED_DELETED(
            [format_path(p, mode='relative') for p in deleted_files])
    if untracked:
        print_message.UNTRACKED_FILE(
            [format_path(p, mode='relative') for p in untracked])
    if not get_all_commits() and not staged and untracked:
        print_message.NO_ADDED_BUT_UNTRACKED()
    elif not staged:
        print_message.NO_ADDED_TO_COMMIT()


def commit_git(message):
    '''
    Task:
        + Update hash commit in index file
        + Create name file is time commit in commits directory
        + Create name file is time commit in snapshots directory
        + Nothing added to commit then show status
    '''
    tracked_files, _ = get_tracked_unstracked()
    staged_files, _ = get_staged_unstaged()
    if staged_files:
        update_index(tracked_files, mode='commit')
        time_commit = format_time(time(), second=False)
        create_commit(message, time_commit)
        create_snapshot(join('.lgit/snapshots', time_commit))
        update_commit_branch(time_commit)
    else:
        show_status()


def log_git():
    commit = get_commit_branch()
    show_log(commit)


def show_log(commit):
    if commit:
        time_commit, author, p_commit, message = get_info_commit(commit)
        date = format_date_log(time_commit)
        print("commit %s\nAuthor: %s\nDate: %s\n\n\t%s\n\n" %
              (commit, author, date, message))
        show_log(p_commit)


def ls_files_git():
    tracked_file, _ = get_tracked_unstracked()
    files = get_trackfile_cwd(tracked_file)
    if files:
        print("\n".join(sorted(files, key=str)))


def get_trackfile_cwd(tracked_files):
    file_current = []
    for file in tracked_files:
        path = format_path(file, mode='relative')
        if not path.startswith('../'):
            file_current.append(path)
    return file_current


def rm_git(files):
    '''
    Task: Remove file at current working directories and index file
        + Handle files input first to get relative path from directory's lgit
        + Read index file and get location of file in index file
        + Remove file in index file and current working directories
                                also empty directories of path file
        + Not found file in index file --> Show error
        + Write changes into index file
    :param files: files are removed
    :return: None
    '''
    tracked, _ = get_tracked_unstracked()
    files_new = handle_raw_input(files, tracked)
    if files_new:
        data_index = read_file(file='.lgit/index')
        location = get_pos_track(files_new)
        for file in files_new:
            line = location.get(file, -1)
            if exists(file):
                remove(file)
                remove_empty_dirs(file)
            data_index[line] = ""
        write_file(data_index, file='.lgit/index')


def init_git():
    direcs, files = check_strucsture_lgit()
    create_structure_lgit(direcs, files)
    setup_lgit()
    if len(direcs) + len(files) < 10:
        print('Git repository already initialized.')


def check_strucsture_lgit():
    direcs = ('.lgit/objects', '.lgit/commits', '.lgit/info',
              '.lgit/stash/heads/master/objects',
              '.lgit/snapshots', '.lgit/refs/heads')
    files = ('.lgit/index', '.lgit/config', '.lgit/info/master',
             '.lgit/refs/heads/master', '.lgit/HEAD')
    init_d = [d for d in direcs if not isdir(d)]
    init_f = [f for f in files if not isfile(f)]
    return init_d, init_f


def setup_lgit():
    config_git(author=environ.get('LOGNAME'))
    if not read_file('.lgit/HEAD'):
        write_file(['ref: refs/heads/master'], '.lgit/HEAD')
    if not read_file('.lgit/info/master'):
        write_file(['%s\n' % (format_time(time(), second=False))],
                   '.lgit/info/master')


def find_parent_git():
    global cwd_path
    cwd_path = getcwd()
    while getcwd() != "/":
        if exists('.lgit/'):
            return True
        chdir('../')
    return False


def format_path(path, mode):
    if mode == 'absolute':
        return abspath(join(cwd_path, path))
    elif mode == 'relative':
        return relpath(join(getcwd(), path), start=cwd_path)


def get_args():
    parser = ArgumentParser(prog="lgit")
    parser.add_argument('command', help="command options")
    parser.add_argument('files', nargs="*",
                        help=" Add file contents to the index")
    parser.add_argument('-m', '--message',
                        help="description about what you do")
    parser.add_argument('--author', help="set author for commit",)
    return parser.parse_args()


def main():
    args = get_args()
    try:
        if args.command == 'init':
            init_git()
        elif find_parent_git():
            if args.command == 'add':
                add_git(args.files)
            elif args.command == 'status':
                status_git()
            elif args.command == 'commit':
                commit_git(args.message)
            elif args.command == 'config':
                config_git(author=args.author)
            elif args.command == 'ls-files':
                ls_files_git()
            elif args.command == 'log':
                log_git()
            elif args.command == 'rm':
                if args.files:
                    rm_git(args.files)
                else:
                    print('Missing file to removed')
            elif args.command == 'checkout':
                if len(args.files) == 1:
                    checkout_git(args.files[0])
                elif len(args.files) > 1:
                    print("invalid argument commit passed into checkout")
                else:
                    print("missing argument commit to checkout")
            elif args.command == 'branch':
                if not args.files:
                    print('*%s' % (get_branch_now()))
                else:
                    branch_git(args.files[0])
            elif args.command == 'stash':
                stash_git()
            elif args.command == 'unstash':
                unstash_git()
            elif args.command == 'merge':
                if not args.files:
                    print('Missing name of branch to merged')
                else:
                    merge_git(args.files[0])
            else:
                print("Git: '" + args.command + "' is not a git command.")
        else:
            print('fatal: not a git repository (or any \
of the parent directories)')
    except FileNotFoundError:
        print('fatal: not a git repository (or any of the parent directories)')
    except IsADirectoryError:
        pass


if __name__ == '__main__':
    main()
