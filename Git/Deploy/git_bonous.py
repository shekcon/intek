#!/usr/bin/env python3

from os import mkdir, environ, scandir, getcwd, chdir, listdir, remove
from os.path import join, exists, isfile, isdir, relpath, abspath, split
from os import makedirs
from argparse import ArgumentParser
from time import time
from get_data_lgit import get_info_config, get_all_commits
from utils import read_file, write_file
import print_message


# TODO: fix conflict
# def checkout_git(timecommit):
#     _, branch, commit = get_info_config()
#     head_commit = get_head_commit(branch)
#     if commit == head_commit:
#         update_index(get_tracked_files(), mode='status')
#     timecommit = timecommit[0]
#     commits = get_commits()
#     if timecommit in commits:
#         rm_untracked_commit(switch_files_commit(timecommit))
#         config_git(head=timecommit)



def config_git(author='', branch='', head=''):
    aut, bra, he = get_info_config()
    if author:
        aut = author
    if branch:
        bra = branch
    if head:
        he = head
    write_file(['%s\nbranch: %s\nhead: %s\n' %
                (aut, bra, he)], file='.lgit/config')


def handle_raw_input(files):
    '''
    Task:
        + Return list valid file is relative with lgit directory
        + Outside of lgit directory --> Show error
        + Path does not exist --> Show error
    '''
    files_new = []
    for f in files:
        path = format_path(f, mode='absolute')
        if getcwd() in path:
            path = path.replace(getcwd() + "/", "")
            if isdir(path):
                sub_file = get_files_direc(path)
                files_new = files_new + sub_file
            elif exists(path):
                files_new.append(path)
            else:
                print("fatal: pathspec '" + f + "' did not match any files")
        else:
            print("fatal: %s '%s' is outside repository" % (f, f))
    return files_new


def add_git(files_add):
    '''
    Task:
        + Add untrack file or update unstaged file in index file
        + Store a copy of the file content in the lgit database
    '''
    files_new = handle_raw_input(files_add)
    if files_new:
        update_index(files_new, mode='add', location=get_pos_track(files_new))
        create_object(files_new)
    elif not files_add:
        print("Nothing specified, nothing added.\n\
Maybe you wanted to say 'git add .'?")


def status_git():
    tracked, _ = get_tracked_unstracked()
    update_index(tracked, mode='status')
    show_status()


def show_status():
    _, untracked = get_tracked_unstracked()
    staged, unstaged = get_staged_unstaged()
    _, branch, _ = get_info_config()
    print_message.BRANCH_NOW(branch)
    if not get_all_commits():
        print_message.NO_COMMITS_YET()
    if staged:
        print_message.READY_COMMITTED()
        print("\t modified:", '\n\t modified: '.join(
            [format_path(p, mode='relative') for p in staged]), end='\n\n')
    if unstaged:
        print_message.TRACKED_MODIFIED()
        print("\t modified:", '\n\t modified: '.join(
            [format_path(p, mode='relative') for p in unstaged]), end='\n\n')
    if untracked:
        print_message.UNTRACKED_FILE()
        print("\t", '\n\t'.join([format_path(p, mode='relative')
                                 for p in untracked]), sep='', end='\n\n')
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
    if staged_file:
        update_index(tracked_files, mode='commit')
        time_commit = format_time(time(), second=False)
        create_commit(message, time_commit)
        create_snapshot(join('.lgit/snapshots', time_commit))
        config_git(head=time_commit)
        update_head_branch(time_commit)
    else:
        show_status()


def log_git():
    for commit in sorted(get_all_commits(), key=str, reverse=True):
        time_commit, author, message = get_info_commit(commit)
        date = format_date_log(time_commit)
        print("commit %s\nAuthor: %s\nDate: %s\n\n\t%s\n\n" %
              (commit, author, date, message))


def ls_files_git():
    files = get_trackfile_cwd(get_tracked_files())
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
                print("fatal: pathspec '" + file + "' did not match any files")
        write_file(data_index, file='.lgit/index')
    elif not files:
        print('missing argument of file to removed')


def init_git():
    direcs = ('.lgit/objects', '.lgit/commits',
              '.lgit/snapshots', '.lgit/refs/HEAD')
    files = ('.lgit/index', '.lgit/config', '.lgit/refs/HEAD/master')
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
    config_git(author=environ.get('LOGNAME'), branch='master')
    if len(init_f) + len(init_d) < 5:
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
                checkout_git(args.files)
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
