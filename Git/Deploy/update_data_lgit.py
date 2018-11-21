from utils import read_file, write_file, hash_sha1
from get_data_lgit import get_info_index, get_branch_now
from get_data_lgit import get_data_object, get_info_snap
from get_data_lgit import get_pos_track, get_files_hash, get_commit_branch
from format_data_lgit import format_index, format_time
from os.path import getmtime, join, split, exists
from os import makedirs, listdir, remove, access, W_OK, R_OK


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
        # commit command then ignore about file doesn't exist
        # or haven't permission to read else skip this file
        # if there is valid file then get location file
        if mode != 'commit' and (not exists(file) or
                                 not access(file, R_OK)):
            continue
        line = location.get(file, -1)

        # add command need hash sha1 file
        # hash add equal hash file
        # hash commit get from index file or empty
        if mode == 'add':
            h_current = hash_sha1(file)
            h_add = h_current
            if line != -1:
                _, _, _, h_commit, _ = get_info_index(data_index[line])

        # commit command only read inside index file
        # read hash current, hash add
        # then now hash commit equal hash add
        elif mode == 'commit':
            _, h_current, h_add, _, _ = get_info_index(data_index[line])
            h_commit = h_add

        # status command update timestamp and hash file now
        # get hash sha1 file then read index file get hash add and commit
        elif mode == 'status':
            h_current = hash_sha1(file)
            _, _, h_add, h_commit, _ = get_info_index(data_index[line])

        if line != -1:
            data_index[line] = format_index(format_time(
                getmtime(file)), h_current, h_add, h_commit, file)

        # when add command if file not in index file then append it into list
        else:
            data_index.append(format_index(format_time(
                getmtime(file)), h_current, h_add, '', file))

    # hash information changes is diffent with origin index file
    # if different then update information changes into index file
    if hash_sha1('.lgit/index') != hash_sha1(data_index, mode='list'):
        write_file(data_index, file='.lgit/index')


def update_files_commit(files_hash):
    '''
    Task:
        + Get dictionary of commit passed: file is key, hash of file is value
        + Loop all file in commit if different hash then
                    get content of file in database object
        + If file exists but not have permission write then remove it
        + Create file or overwrite content of file
    :param files_hash: a dictionary key is file, value is hash of file
    :return: list files is changed content from commit passed
    '''
    files_update = []
    for file in files_hash.keys():
        if exists(file) and not access(file, W_OK):
            remove(file)
        if not exists(file) or files_hash[file] != hash_sha1(file):
            update_content_file(file, files_hash[file])
        files_update.append(file)
    return files_update


def update_content_file(file, hash_file):
    content = get_data_object(hash_file)
    head, _ = split(file)
    if head and not exists(head):
        makedirs(head)
    write_file(content, file, mode='wb')


def update_commit_branch(commit):
    '''
    Task: update information last commit for branch
    :param commit: last commit of branch now
    :return:
    '''
    branch = get_branch_now()
    write_file(['%s\n' % (commit)], join('.lgit/refs/heads', branch))


def update_branch_now(branch):
    '''
    Task: update information of branch is working now
    :param branch: branch is switch
    :return: nothing
    '''
    write_file(['ref: refs/heads/%s\n' % (branch)], '.lgit/HEAD')


def update_unstash_files(branch):
    path = '.lgit/stash/heads/%s/index' % (branch)
    if exists(path):
        write_file(read_file(path), '.lgit/index')
        for file in listdir('.lgit/stash/heads/%s/objects' % (branch)):
            # get content of file
            file_object = '.lgit/stash/heads/%s/objects/%s' % (branch, file)
            content = read_file(file_object, mode='rb')

            # if file exists and not have permission to write then remove
            if exists(file) and not access(file, W_OK):
                remove(file)
            write_file(content, file, mode='wb')

            remove(file_object)
        remove(path)
        return 'Unstaged completed'
    else:
        return "Nothing to unstaged at all"
