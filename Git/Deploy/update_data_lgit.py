from utils import read_file, write_file, hash_sha1
from get_data_lgit import get_info_index, get_info_config
from get_data_lgit import get_data_object, get_info_snap
from format_data_lgit import format_index, format_time
from os.path import getmtime


def update_index(files, mode, location=''):
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
    for i, file in enumerate(files):
        if not exists(file):
            continue
        h_current = hash_sha1(file)
        if mode == 'add':
            # get index from mapping index of file
            # hash add equal hash of file right now
            # commit maybe nothing or have before
            line = location.get(file, -1)
            h_add = h_current
            if line != -1:
                _, _, _, h_commit, _ = get_info_index(data_index[line])
            else:
                h_commit = ''
        else:
            # index equal enunumerate coz run all name file in index file
            # hash add equal last time add of file
            # commit equal hash add if commit else still be same in last time
            line = i
            _, _, h_add, h_commit, _ = get_info_index(data_index[line])
            if mode == 'commit':
                h_commit = h_add
        # add new one in index file if first time tracking file
        # else override on location of file in index file
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
    snapshot = read_file(join('.lgit/snapshots', timecommit))
    staged, unstaged = get_staged_unstaged()
    files_update = staged + unstaged
    for line in snapshot:
        hash_f, file = get_info_snap(line)
        if file not in files_update:
            content = get_data_object(hash_f)
            write_file(content, file)
        files_update.append(file)
    return files_update


def remove_untrack_commit(files_update):
    _, _, commit = get_info_config()
    tracked_files = get_tracked_commit(commit)
    unstrack_rm = [f for f in tracked_files if f not in files_update]
    for file in unstrack_rm:
        remove(file)
