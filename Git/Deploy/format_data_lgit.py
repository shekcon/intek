from datetime import datetime
from time import strftime, mktime, localtime
from get_data_lgit import get_branch_now


def format_date_log(timestamp):
    year = int(timestamp[0: 4])
    moth = int(timestamp[4: 6])
    day = int(timestamp[6: 8])
    hour = int(timestamp[8: 10])
    minute = int(timestamp[10: 12])
    second = int(timestamp[12: 14])
    # create Epoch time
    date = mktime((year, moth, day, hour, minute, second, 0, 0, 0))
    return strftime("%a %b %d %H:%M:%S %Y", localtime(date))


def format_time(timestamp, second=True):
    timestamp = datetime.fromtimestamp(timestamp)
    if second:
        return timestamp.strftime('%Y%m%d%H%M%S')
    return timestamp.strftime('%Y%m%d%H%M%S.%f')


# get string format index
def format_index(timestamp, current, add, commit, path):
    return '%s %s %s %40s %s\n' % (timestamp, current, add, commit, path)


def format_conflict(data_rec, data_mer, branch_m):
    return '<<<<<<<< %s\n%s======== %s\n%s' % (get_branch_now(), data_rec,
                                               branch_m, data_mer)
