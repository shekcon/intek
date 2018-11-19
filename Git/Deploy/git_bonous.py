#!/usr/bin/env python3

from os import mkdir, environ, scandir, getcwd, chdir, listdir, remove
from os.path import join, exists, isfile, isdir, relpath, abspath, split
from os import makedirs, access, R_OK
from argparse import ArgumentParser
from time import time
from get_data_lgit import get_info_config, get_all_commits, get_pos_track
from get_data_lgit import get_tracked_unstracked, get_staged_unstaged
from get_data_lgit import get_info_commit, get_head_commit
from get_data_lgit import get_modified_headcommit
from update_data_lgit import update_files_commit, rm_untrack_commit
from utils import read_file, write_file, get_files_direc, remove_empty_dirs
from utils import rm_head_lgit, hash_sha1
from update_data_lgit import update_index, update_head_branch
from create_data_lgit import create_object, create_commit, create_snapshot, create_branch
from format_data_lgit import format_index, format_time, format_date_log
import print_message


def branch_git(name):
    create_branch(name)
    print("create new branch %s" % (name))


def checkout_git(commit):
    modified_file = get_modified_headcommit()
    if not modified_file and is_valid_commit(commit):
        rm_untrack_commit(update_files_commit(commit))
        config_git(head=commit)
        print("head now is %s" % (commit))
    else:
        print_message.ERROR_CHECKOUT(
            [format_path(p, mode='relative') for p in modified_file])


def is_valid_commit(timecommit):
    commits = get_all_commits()
    return timecommit in commits


def config_git(author):
    write_file(['%s\n' % (author)], file='.lgit/config')


def handle_raw_input(files_user):
    '''
    Task:
        + Return list valid file is relative with lgit directory
        + Directory --> find all of files in directory --> handle input again to get valid file
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
                valid_files = valid_files + handle_raw_input(sub_files)
            elif is_valid_file(path, file):
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
    if is_last_commit():
        tracked, _ = get_tracked_unstracked()
        update_index(tracked, mode='status')
        show_status()


def is_last_commit():
    _, branch, head_commit = get_info_config()
    last_commit = get_head_commit(branch)
    return head_commit != last_commit


def show_status():
    _, untracked = get_tracked_unstracked()
    staged, unstaged = get_staged_unstaged()
    _, branch, _ = get_info_config()
    print_message.BRANCH_NOW(branch)
    if not get_all_commits():
        print_message.NO_COMMITS_YET()
    if staged:
        print_message.READY_COMMITTED(
            [format_path(p, mode='relative') for p in staged])
    if unstaged:
        print_message.TRACKED_MODIFIED(
            [format_path(p, mode='relative') for p in unstaged])
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
        config_git(head=time_commit)
        update_head_branch(time_commit)
    else:
        show_status()


def log_git():
    _, branch, _ = get_info_config()
    p_commit = get_head_commit(branch)
    while p_commit:
        time_commit, author, p_commit, message = get_info_commit(commit)
        date = format_date_log(time_commit)
        print("commit %s\nAuthor: %s\nDate: %s\n\n\t%s\n\n" %
              (commit, author, date, message))


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
    files_new = handle_raw_input(files)
    if files_new:
        data_index = read_file(file='.lgit/index')
        location = get_pos_track(files_new)
        for file in files_new:
            line = location.get(file, -1)  # get location of file
            # if not in index file print error
            if line != -1:
                if exists(file):
                    remove(file)
                    remove_empty_dirs(file)
                data_index[line] = ""
            else:
                print_message.NOT_MATCH_FILE(
                    format_path(file, mode='relative'))
        write_file(data_index, file='.lgit/index')
    elif not files:
        print('missing argument of file to removed')


def init_git():
    direcs = ('.lgit/objects', '.lgit/commits',
              '.lgit/snapshots', '.lgit/refs/heads')
    files = ('.lgit/index', '.lgit/config', '.lgit/refs/heads/master', '.lgit/HEAD')
    init_d = [d for d in direcs if not isdir(d)]
    init_f = [f for f in files if not isfile(f)]
    if not exists('.lgit'):
        mkdir('.lgit')
    elif isfile('.lgit'):
        print('fatal: Invalid gitfile format: .lgit')
        return
    for d in init_d:
        if isfile(d):
            print(join(getcwd(), dir) + ": Not a directory")
        else:
            makedirs(d)
    for f in init_f:
        if not isdir(f):
            open(f, 'w').close()
        else:
            print('error: unable to mmap ' + join(getcwd(), f)
                  + ' Is a directory')
    config_git(author=environ.get('LOGNAME'))
    if len(init_f) + len(init_d) < 8:
        print('Git repository already initialized.')


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
                rm_git(args.files)
            elif args.command == 'checkout':
                if len(args.files) == 1:
                    checkout_git(args.files[0])
                elif len(args.files) > 1:
                    print("invalid argument commit passed into checkout")
                else:
                    print("missing argument commit to checkout")
            elif args.command == 'branch':
                if not args.files:
                    _, branch, _ = get_info_config()
                    print('*%s' % (branch))
                else:
                    branch_git(args.files[0])
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
