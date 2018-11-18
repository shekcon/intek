from utils import read_file, split_dir_file, get_files_direc
from os.path import join
from os import listdir
from get_data_lgit import get_info_index

def get_staged_unstaged():
    staged_file = []
    unstaged_file = []
    for line in read_file(file='.lgit/index'):
        _, h_current, h_add, h_commit, name = get_info_index(line)
        if h_current != h_add:
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
    unstracked = [file for file in get_files_direc() if file not in tracked]
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
    return read_file(join(join('.lgit/objects', direc), file))


def get_all_commits():
    return listdir('.lgit/commits')


def get_tracked_commit(commit):
    files = []
    for line in read_file(join('.lgit/snapshots', commit)):
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


def get_info_config():
    data = read_file('.lgit/config')
    # format author, branch, head
    if data:
        return data[0].strip(), data[1].strip()[8:], data[2].strip()[6:]
    # first time get infomation config is empty
    return '', 'master', ''


def get_info_commit(commit):
    data = read_file(join(".lgit/commits", commit))
    # format time commit, author, message commit
    return data[1].strip(), data[0].strip(), data[3].strip()


def get_head_commit(branch):
    return read_file(join('.lgit/refs/HEAD/', branch))[0].strip()
