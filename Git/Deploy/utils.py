from git import read_file, write_file, split_dir_file, join, listdir

def checkout_git(timecommit):
    commits = get_commits()
    if timecommit in commits:
        snapshot = read_file(join('.lgit/snapshots', timecommit))
        for line in snapshot:
            hash_f, file = get_info_snap(line)
            content = read_object(hash_f)
            write_file(content, file)


def read_object(hash_commit):
    direc, file = split_dir_file(hash_commit)
    return read_file(join(join('.lgit/objects', direc), file))


def get_info_snap(line):
    line = line.strip()
    # format hash commit file, path of file
    return line[:40], line[41:]


def get_commits():
    return listdir('.lig/commits')