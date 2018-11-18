from utils import read_file, write_file, hash_sha1
from get_data_lgit import get_info_index, get_info_config
from get_data_lgit import get_data_object, get_info_snap
from get_data_lgit import get_staged_unstaged, get_tracked_commit
from get_data_lgit import get_pos_track, get_files_hash
from format_data_lgit import format_index, format_time
from os.path import getmtime, exists, join
from os import remove


def update_index(files_update, mode):
    '''
    Task: Update information of tracked file or untracked file in index file
        + With add command:
            - Update hash add and timestamp of file
            - Or add new line infomation file added in index file
        + With status command:
            - Update hash current and timestamp of file in index file
        + With commit command:
            - Update hash commit of file in index file
    '''
    data_index = read_file('.lgit/index')
    location = get_pos_track(files_update)
    for file in files_update:
        h_current = hash_sha1(file)
        line = location.get(file, -1)
        if mode == 'add':
            h_add = h_current
            if line != -1:
                _, _, _, h_commit, _ = get_info_index(data_index[line])
            else:
                h_commit = ''
        else:
            _, _, h_add, h_commit, _ = get_info_index(data_index[line])
            if mode == 'commit':
                h_commit = h_add
        if line != -1:
            data_index[line] = format_index(format_time(
                getmtime(file)), h_current, h_add, h_commit, file)
        else:
            data_index.append(format_index(format_time(
                getmtime(file)), h_current, h_add, h_commit, file))
    write_file(data_index, file='.lgit/index')  


def update_head_branch(time_commit):
    _, branch, _ = get_info_config()
    write_file(['%s\n' % (time_commit)], join('.lgit/refs/HEAD', branch))


def update_files_commit(timecommit):
    files_commit = get_files_hash(timecommit)
    files_update = []
    for file in files_commit.keys():
        content = get_data_object(files_commit[file])
        write_file(content, file, mode='wb')
        files_update.append(file)
    return files_update


def rm_untrack_commit(files_update):
    _, _, commit = get_info_config()
    tracked_files = get_tracked_commit(commit)
    unstrack_rm = [f for f in tracked_files if f not in files_update]
    for file in unstrack_rm:
        remove(file)