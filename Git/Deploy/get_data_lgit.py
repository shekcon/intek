from utils import read_file, split_dir_file, get_files_direc, hash_sha1
import os


def get_all_branchs():
    return os.listdir('.lgit/refs/heads')


def get_modified_branch():
    branch_commit = get_commit_branch()
    files_hash = get_files_hash(branch_commit)
    modified_file = []
    for file in files_hash.keys():
        if hash_sha1(file) != files_hash[file]:
            modified_file.append(file)
    return modified_file


def get_files_hash(commit):
    snapshot = read_file('.lgit/snapshots/%s' % (commit))
    files_hash = {}
    for line in snapshot:
        hash_f, file = get_info_snap(line)
        files_hash[file] = hash_f
    return files_hash


def get_staged_unstaged():
    staged_file = []
    unstaged_file = []
    for line in read_file(file='.lgit/index'):
        _, h_current, h_add, h_commit, name = get_info_index(line)
        if h_current != h_add or not os.access(name, os.R_OK):
            unstaged_file.append(name)
        if h_add != h_commit:
            staged_file.append(name)
    return staged_file, unstaged_file


def get_tracked_unstracked():
    '''
    Task: Return list tracked and untracked file in index file
    '''
    tracked = []
    for line in read_file('.lgit/index'):
        _, _, _, _, file = get_info_index(line)
        tracked.append(file)
    untracked = [file for file in get_files_direc() if file not in tracked]
    return tracked, untracked


def get_pos_track(files):
    '''
    Task: return dictionary with key is file, value is location in index file
    '''
    locations = {}
    for index, line in enumerate(read_file('.lgit/index')):
        _, _, _, _, path = get_info_index(line)
        if path in files:
            locations[path] = index
    return locations


def get_data_object(hash_commit):
    direc, file = split_dir_file(hash_commit)
    path = '.lgit/objects/%s/%s' % (direc, file)
    return read_file(path, mode='rb')


def get_tracked_commit(commit):
    files = []
    for line in read_file('.lgit/snapshots/%s' % (commit)):
        files.append(line.strip()[41:])
    return files


def get_info_index(line):
    '''
    Task: return format timestamp, hash current, hash add, hash commit, path
    '''
    line = line.strip()
    return line[0:14], line[15:55], line[56:96], line[97:137], line[138:]


def get_info_snap(line):
    line = line.strip()
    # format hash commit file, path of file
    return line[:40], line[41:]


def get_branch_now():
    data = read_file('.lgit/HEAD')[0].strip()
    return data[16:]


def get_commit_branch(branch=''):
    if not branch:
        branch = get_branch_now()
    result = read_file('.lgit/refs/heads/%s' % (branch))
    return result[0].strip() if result else ''


def get_info_commit(commit):
    data = read_file(".lgit/commits/%s" % (commit))
    # format time commit, author, point commit, message commit
    return data[1].strip(), data[0].strip(), data[2].strip(), data[4].strip()


def get_author():
    return read_file('.lgit/config')[0].strip()


def get_cmit_create_b(branch):
    return read_file('.lgit/info/%s' % (branch))[0].strip()
