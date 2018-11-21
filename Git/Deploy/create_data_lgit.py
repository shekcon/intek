from get_data_lgit import get_info_index, get_branch_now, get_commit_branch
from get_data_lgit import get_author
from os.path import join, exists, isdir, isfile, split
from os import makedirs, getcwd, access, R_OK
from utils import write_file, read_file, hash_sha1, split_dir_file
from sys import exit as exit_program
import print_message


def create_branch(name):
    makedirs('.lgit/stash/heads/%s/objects' % (name))
    write_file(['%s\n' % (get_commit_branch())],
               '.lgit/refs/heads/%s' % (name))


def create_commit(message, time_ns):
    # save commit message and author
    author = get_author()
    t_commit = time_ns.split('.')[0]
    p_commit = get_commit_branch()
    write_file(["%s\n%s\n%s\n\n%s\n" %
                (author, t_commit, p_commit, message)],
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
            makedirs(direc_obj)
        file_obj = join(direc_obj, file_obj)
        if not exists(file_obj):
            write_file(read_file(path, mode='rb'), file_obj, mode='wb')


def create_info_branch(branch):
    write_file(['%s\n' % (get_commit_branch())],
               join('.lgit/info', branch))


def create_structure_lgit(direcs, files):
    if not exists('.lgit'):
        makedirs('.lgit')
    elif isfile('.lgit'):
        print('fatal: Invalid gitfile format: .lgit')
        exit_program()
    for d in direcs:
        if isfile(d):
            print("%s: Not a directory" % (join(getcwd(), d)))
        else:
            makedirs(d)
    for f in files:
        if not isdir(f):
            open(f, 'w').close()
        else:
            print("error: unable to mmap '%s' Is a directory" %
                  (join(getcwd(), f)))


def create_stash_files(modified_file):
    if _is_valid_stash(modified_file):
        branch_now = get_branch_now()
        path = '.lgit/stash/heads/%s/index' % (branch_now)
        write_file(read_file('.lgit/index'), path)
        for file in modified_file:
            content = read_file(file, mode='rb')
            path = join('.lgit/stash/heads/%s/objects' % (branch_now), file)
            write_file(content, path, mode='wb')


def _is_valid_stash(files):
    for f in files:
        if access(f, R_OK):
            print_message.PERMISSION_DENIED_STASH(f)
            exit_program()
    return True
