#!/usr/bin/env python3
import os
from argparse import ArgumentParser
from time import time
from sys import exit as exit_program
from args_lgit import handle_arguments
from utils import *
from print_message import *
import get_data_lgit as lgit_g
import create_data_lgit as lgit_c
import update_data_lgit as lgit_u
import format_data_lgit as lgit_f
import difflib


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
    handle_merge()
    last_cmit_b = lgit_g.get_commit_branch(branch_m)
    if lgit_g.get_commit_branch() != last_cmit_b:
        if is_fast_forward(branch_m):
            print('<--------------Merge Fast-Forward-------------->')
            revert_commit(branch_m)
            lgit_u.update_commit_branch(last_cmit_b)
        else:
            print('<------------------Merge Conflict----------------->')
            # conflict_f, create_f = check_merge_branch(last_cmit_b)
            # update_files_commit(create_f)
            # handle_conflict(conflict_f, branch_m)
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


def handle_merge():
    compare_origin('origin', 'master')
    compare_origin('origin', 'branch')


def set_map_line(dest_content):
    line_dest = [-1]
    for index, i in enumerate(dest_content):
        if i == '\n':
            line_dest.append(index)
    if dest_content[-1] != '\n':
        line_dest.append(len(dest_content) - 1)
    return line_dest


def compare_origin(origin, other):
    dest_content = ''.join(read_file(origin))
    source_content = ''.join(read_file(other))

    line_dest = set_map_line(dest_content)
    line_src = set_map_line(source_content)
    print(line_dest)


    match = difflib.SequenceMatcher(None, dest_content, source_content)
    direction = match.get_opcodes()

    merge_file = []
    print(direction)
    for tag, i1, i2, j1, j2 in direction:
        if tag == 'equal':
            print('%s\n%s\n%s' % (
                tag, dest_content[i1:i2], source_content[j1:j2]))
            start, end = handle_line(line_dest, i1, i2)
            merge_file.append(('equal', start, end))
        if tag == 'insert':
            print('%s\n%s\n%s' % (
                tag, dest_content[i1:i2], source_content[j1:j2]))
            start, end = handle_line(line_dest, i1, i2)
            merge_file.append(('insert', start, end))
        elif tag == 'replace':
            print('%s\n%s\n%s' % (
                tag, dest_content[i1:i2], source_content[j1:j2]))
            start, end = handle_line(line_dest, i1, i2)
            merge_file.append(('replace', start, end))
        elif tag == 'delete':
            print('%s\n%s\n%s' % (
            tag, dest_content[i1:i2], source_content[j1:j2]))
            start, end = handle_line(line_dest, i1, i2)
            merge_file.append(('delele', start, end))
    print(merge_file)
    status_file = {'equal':[], 'insert':[], 'replace': [], 'delete': []}
    for tag, start, end in merge_file:
        if  tag == 'equal' and (start, end) not in status_file['equal']:
            status_file['equal'].append((start, end))
        if  tag == 'insert' and (start, end) not in status_file['insert']:
            status_file['insert'].append((start, end))
        if  tag == 'replace' and (start, end) not in status_file['replace']:
            status_file['replace'].append((start, end))
        if  tag == 'delete' and (start, end) not in status_file['delete']:
            status_file['delete'].append((start, end))
    equal_origin = []
    for line in status_file['equal']:
        if line not in status_file['insert'] + status_file['replace'] + status_file['delete']:
            equal_origin.append(line)
    print(equal_origin)


def handle_line(line_dest, start, end):
    size = len(line_dest)
    end_l = end - 1
    start_l = start
    for i in range(1, size):
        if line_dest[i - 1] <= start_l <= line_dest[i]:
            if start_l == line_dest[i]:
                start_l = line_dest[i] + 1
            else:
                start_l = line_dest[i - 1] + 1
            j = i
            while not (line_dest[j - 1] <= end_l and end_l <= line_dest[j]):
                j = j + 1
            if start_l == line_dest[j - 1] + 1:
                end_l = j
            else:
                end_l = j - 1

            if start_l == line_dest[i]:
                start_l = i
            else:
                start_l = i - 1
            if start == end:
                end_l = start_l
            break
    return start_l, end_l


def is_fast_forward(branch_m):
    '''
    Task: checking time commit create of 2 branch
    :param branch_m: other branch merge to current branch
    :return: Boolean
    '''
    commit_create_b = lgit_g.get_cmit_create_b(branch_m)
    return commit_create_b and lgit_g.get_commit_branch() <= commit_create_b


def get_branch_commits(branch):
    '''
    Task: find all commits of branch passed and return it
    :param branch: branch want to get all of commits
    :return: list
    '''
    commit = lgit_g.get_commit_branch(branch)
    commits_branch = []
    while commit:
        commits_branch.append(commit)
        _, _, commit, _ = lgit_g.get_info_commit(commit)
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
        lgit_c.create_stash_files(modified_files)
        revert_commit(lgit_g.get_branch_now())
        print('Stash the current changes')
    else:
        print('Nothing changes at all')


def unstash_git():
    print(lgit_u.update_unstash_files(lgit_g.get_branch_now()))


def show_branch():
    branchs = os.listdir('.lgit/refs/heads/')
    b_current = lgit_g.get_branch_now()
    print('%s*%s%s' % (COLORS.GREEN, b_current, COLORS.ENDC))
    other_b = '\n'.join([b for b in branchs if b not in b_current])
    if other_b:
        print(other_b)


def branch_git(name):
    if not name:
        show_branch()
    elif is_invalid_branch(name):
        lgit_c.create_branch(name)
        lgit_c.create_info_branch(name)
        print("Create a new branch '%s'" % (name))
    else:
        print("fatal: A branch named '%s' already exists." % (name))


def checkout_git(branch):
    if is_invalid_branch(branch):
        print("error:patal '%s' not match any branchs known to git" % (branch))
    elif branch != lgit_g.get_branch_now():
        modified = check_modified_file()
        if not modified:
            revert_commit(branch)
            lgit_u.update_branch_now(branch)
            print("Switched to branch '%s'" % (branch))
        else:
            ERROR_CHECKOUT(
                [format_path(p, mode='relative') for p in modified])
    else:
        print("Already on '%s'" % (branch))


def revert_commit(branch):
    commit = lgit_g.get_commit_branch(branch=branch)
    files_hash = lgit_g.get_files_hash(commit)
    files_update = lgit_u.update_files_commit(files_hash)
    remove_untracked_commit(files_update)
    overwrite_index(files_hash)


def remove_untracked_commit(files_update):
    tracked, _ = lgit_g.get_tracked_unstracked()
    untracked_file = [f for f in tracked if f not in files_update]
    for file in untracked_file:
        os.remove(file)
        remove_empty_dirs(file)


def check_modified_file():
    '''
    return list file is modified at branch now
    '''
    tracked, _ = lgit_g.get_tracked_unstracked()
    lgit_u.update_index(tracked, mode='status')
    staged, unstaged = lgit_g.get_staged_unstaged()
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
        line = lgit_f.format_index(lgit_f.format_time(os.path.getmtime(file)),
                                   hash_f, hash_f, hash_f, file)
        data.append(line)
    write_file(data, '.lgit/index')


def is_invalid_branch(branch):
    branchs = lgit_g.get_all_branchs()
    return branch not in branchs


def config_git(author):
    write_file(['%s\n' % (author)], file='.lgit/config')


def handle_raw_input(files_user, tracked_file='', mode=''):
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

            if os.path.isdir(path):
                sub_files = get_files_direc(path, mode)
                valid_files = valid_files +\
                    handle_raw_input(sub_files, tracked_file, mode)

            elif path in tracked_file or is_valid_file(path, file):
                valid_files.append(path)

        else:
            OUTSIDE_DIRECTORY(file)
            exit_program()
    return valid_files


def is_valid_file(path, file):
    '''
    Task: Return True if file is valid
        + File do not have permission to read --> Show error
        + Path does not exist --> Show error
    '''
    if os.path.exists(path) and os.access(path, mode=os.R_OK):
        return True
    elif not os.path.exists(path):
        NOT_MATCH_FILE(file)
    elif not os.access(path, mode=os.R_OK):
        PERMISSION_DENIED_READ(file)
    else:
        return False
    exit_program()


def is_inside_lgit(path):
    return os.getcwd() in path


def add_git(files_add):
    '''
    Task:
        + Add untrack file or update unstaged file in index file
        + Store a copy of the file content in the lgit database
    '''
    files_new = handle_raw_input(files_add, mode='add')
    if files_new:
        lgit_u.update_index(files_new, mode='add')
        lgit_c.create_object(files_new)


def status_git():
    tracked, _ = lgit_g.get_tracked_unstracked()
    lgit_u.update_index(tracked, mode='status')
    show_status(get_files_deleted(tracked))


def get_files_deleted(tracked_file):
    return [file for file in tracked_file if not os.path.exists(file)]


def show_status(deleted_files=''):
    _, untracked = lgit_g.get_tracked_unstracked()
    staged, unstaged = lgit_g.get_staged_unstaged()
    staged = [f for f in staged if f not in deleted_files]
    unstaged = [f for f in unstaged if f not in deleted_files]
    BRANCH_NOW(lgit_g.get_branch_now())
    if not os.listdir('.lgit/commits'):
        NO_COMMITS_YET()
    if staged:
        READY_COMMITTED(
            [format_path(p, mode='relative') for p in staged])
    if unstaged:
        TRACKED_MODIFIED(
            [format_path(p, mode='relative') for p in unstaged])
    if deleted_files:
        TRACKED_DELETED(
            [format_path(p, mode='relative') for p in deleted_files])
    if untracked:
        UNTRACKED_FILE(
            [format_path(p, mode='relative') for p in untracked])
    if not os.listdir('.lgit/commits') and not staged and untracked:
        NO_ADDED_BUT_UNTRACKED()
    elif not staged:
        NO_ADDED_TO_COMMIT()


def commit_git(message):
    '''
    Task:
        + Update hash commit in index file
        + Create name file is time commit in commits directory
        + Create name file is time commit in snapshots directory
        + Nothing added to commit then show status
    '''
    tracked_files, _ = lgit_g.get_tracked_unstracked()
    staged_files, _ = lgit_g.get_staged_unstaged()
    if staged_files:
        lgit_u.update_index(tracked_files, mode='commit')
        time_commit = lgit_f.format_time(time(), second=False)
        lgit_c.create_commit(message, time_commit)
        lgit_c.create_snapshot('.lgit/snapshots/%s' % (time_commit))
        lgit_u.update_commit_branch(time_commit)
    else:
        show_status()


def log_git():
    commit = lgit_g.get_commit_branch()
    show_log(commit)


def show_log(commit):
    if commit:
        time_commit, author, p_commit, message = lgit_g.get_info_commit(commit)
        date = lgit_f.format_date_log(time_commit)
        print("%scommit %s%s\nAuthor: %s\nDate: %s\n\n\t%s\n\n" %
              (COLORS.RED, commit, COLORS.ENDC, author, date, message))
        show_log(p_commit)


def ls_files_git():
    tracked_file, _ = lgit_g.get_tracked_unstracked()
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
    tracked, _ = lgit_g.get_tracked_unstracked()
    files_new = handle_raw_input(files, tracked)
    if files_new:
        data_index = read_file(file='.lgit/index')
        location = lgit_g.get_pos_track(files_new)
        for file in files_new:
            line = location.get(file, -1)
            if os.path.exists(file):
                os.remove(file)
                remove_empty_dirs(file)
            data_index[line] = ""
        write_file(data_index, file='.lgit/index')


def handle_init_dest(dest):
    if dest:
        if os.path.exists(dest):
            print('fatal: cannot mkdir %s: File exists' % (dest))
            exit_program()
        else:
            os.makedirs(dest)
            os.chdir(dest)


def init_git():
    direcs, files = check_strucsture_lgit()
    lgit_c.create_structure_lgit(direcs, files)
    setup_lgit()
    if len(direcs) + len(files) < 10:
        print('Lgit repository already initialized.')
    else:
        print('Initialized empty Lgit repository in %s/.lgit/' % (os.getcwd()))


def check_strucsture_lgit():
    direcs = ('.lgit/objects', '.lgit/commits', '.lgit/info',
              '.lgit/stash/heads/master/objects',
              '.lgit/snapshots', '.lgit/refs/heads')
    files = ('.lgit/index', '.lgit/config', '.lgit/info/master',
             '.lgit/refs/heads/master', '.lgit/HEAD')
    init_d = [d for d in direcs if not os.path.isdir(d)]
    init_f = [f for f in files if not os.path.isfile(f)]
    return init_d, init_f


def setup_lgit():
    if not read_file('.lgit/config'):
        config_git(author=os.environ.get('LOGNAME'))
    if not read_file('.lgit/HEAD'):
        write_file(['ref: refs/heads/master'], '.lgit/HEAD')
    if not read_file('.lgit/info/master'):
        write_file(['%s\n' % (lgit_f.format_time(time(), second=False))],
                   '.lgit/info/master')


def find_parent_git():
    global cwd_path
    cwd_path = os.getcwd()
    while os.getcwd() != "/":
        if os.path.exists('.lgit/'):
            return True
        os.chdir('../')
    return False


def format_path(path, mode):
    if mode == 'absolute':
        return os.path.abspath('%s/%s' % (cwd_path, path))
    elif mode == 'relative':
        return os.path.relpath('%s/%s' % (os.getcwd(), path), start=cwd_path)


def main():
    args = handle_arguments()
    try:
        if args.command == 'init':
            handle_init_dest(args.dest)
            init_git()
        elif find_parent_git():
            if args.command == 'add':
                add_git(args.file)
            elif args.command == 'status':
                status_git()
            elif args.command == 'commit':
                commit_git(args.message)
            elif args.command == 'config':
                config_git(args.author)
            elif args.command == 'ls-files':
                ls_files_git()
            elif args.command == 'log':
                log_git()
            elif args.command == 'rm':
                rm_git(args.file)
            elif args.command == 'checkout':
                checkout_git(args.branch)
            elif args.command == 'branch':
                branch_git(args.name)
            elif args.command == 'stash':
                stash_git()
            elif args.command == 'unstash':
                unstash_git()
            elif args.command == 'merge':
                merge_git(args.branch)
        else:
            print('fatal: not a git repository (or any \
of the parent directories)')
    except FileNotFoundError:
        print('fatal: not a git repository (or any of the parent directories)')
    except IsADirectoryError:
        pass


if __name__ == '__main__':
    main()
