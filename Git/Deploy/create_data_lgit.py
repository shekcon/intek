from get_data_lgit import get_info_config, get_info_index
from os.path import split, join, exists
from os import mkdir
from utils import write_file, read_file, hash_sha1, split_dir_file
from get_data_lgit import get_head_commit


def create_branch(name):
    _, branch, _ = get_info_config()
    write_file(['%s\n' % (get_head_commit(branch))],
               '.lgit/refs/HEAD/%s' % (name))


def create_commit(message, time_ns):
    # save commit message and author
    author, _, _ = get_info_config()
    time_commit = time_ns.split('.')[0]
    write_file(["%s\n%s\n\n%s\n" % (author, time_commit, message)],
               join('.lgit/commits', time_ns))


def create_snapshot(path):
    # save all of hash commit and path in index file
    # into timestamp of commit file at snapshot directory
    data_snap = []
    for line in read_file('.lgit/index'):
        _, _, _, h_commit, name = get_info_index(line)
        data_snap.append(h_commit + " " + name + '\n')
    write_file(data_snap, file=path)


def create_object(files_add):
    '''
    Task:
        + Store a copy of the file content in the lgit database
        + Each file will be stocked in the following way:
            - first two characters of the SHA1 will be the directory name
            - last 38 characters will be the file name
    '''
    for path in files_add:
        hash_f = hash_sha1(path)
        direc_obj, file_obj = split_dir_file(hash_f)
        direc_obj = join('.lgit/objects', direc_obj)
        if not exists(direc_obj):
            mkdir(direc_obj)
        file_obj = join(direc_obj, file_obj)
        if not exists(file_obj):
            write_file(read_file(path, mode='rb'), file_obj, mode='wb')