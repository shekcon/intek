#!/usr/bin/env python3
from os.path import join
import os

def format_path(path, mode):
    cwd_path = '/home/shekcon/Intek/Git/Deploy/test/f1' + path 
    # os.chdir(cwd_path)
    lgit = '/home/shekcon/Intek/Git/Deploy'
    # cwd = cwd_path
    if mode == 'add':
        path = os.path.abspath(cwd_path)
        print(path)
        path = path.replace(lgit + "/", "")
        if lgit not in path:
            print('dawdaw')
        print(path)
    elif mode == 'status':
        return relpath(join(getcwd(), path), start=cwd_path)


format_path('/*', 'add')


# def checkout_git(branch):
#     time_commit = is_valid_commit(branch)
#     if is_invalid_branch(branch):
#         print("error '%s' not match any branchs known to git" % (branch))
#     elif branch != get_branch_now() or time_commit:
#         tracked, _ = get_tracked_unstracked()
#         update_index(tracked, mode='status')
#         staged, unstaged = get_staged_unstaged()
#         # modified_file = get_modified_branch()
#         if not (staged or unstaged):
#             if time_commit:
#                 files_hash = get_files_hash(time_commit)
#             else:
#                 files_hash = get_files_hash(get_commit_branch(branch=branch))
#             files_modified = update_files_commit(files_hash)
#             rm_git([file for file in tracked
#                     if file not in files_modified], mode='checkout')
#             overwrite_index(files_hash)
#             if time_commit:
#                 print("HEAD now is '%s'" % (time_commit))
#             else:
#                 update_branch_now(branch)
#                 print("Switched to branch '%s'" % (branch))
#         else:
#             print_message.ERROR_CHECKOUT(
#                 [format_path(p, mode='relative') for p in staged + unstaged])
#     else:
#         print("Already on '%s'" % (branch))


# def is_valid_commit(commit):
#     branch_commits = get_branch_commits(get_branch_now())
#     if commit in branch_commits:
#         return commit
#     return ''