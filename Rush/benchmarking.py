#!/usr/bin/env python3
# set interpreter
from argparse import ArgumentParser
import sys
import subprocess
import resource
import tracemalloc
import os
import cProfile


def read_resource(usage):
    RESOURCES = [
        ('ru_utime', 'User time'),
        ('ru_stime', 'System time'),
        ('ru_maxrss', 'Max. Resident Set Size'),
    ]

    usage = resource.getrusage(usage)

    for name, desc in RESOURCES:
        print('{:<25} ({:<10}) = {}'.format(
            desc, name, getattr(usage, name)))


def display_trace():
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    for stat in top_stats:
        print(stat)

def read_stdin():
    data = []
    for line in sys.stdin:
        line = line.strip()
        line = line.split(',')
        line[3] = int(line[3])
        data.append(line)
    return data



def handle_wel_args():
    parser = ArgumentParser(usage='./benchmarking.py [option] program *arguments',
                            description='benchmarking calculate the memory allocation, run-time performance and number of function calls of the program')
    parser.add_argument('programs', nargs="+")
    parser.add_argument('-m', '--memory',
                        help="outputs the memory allocation of the target program",
                        action="store_true")
    parser.add_argument('-t', '--time',
                        help="outputs the execution time (run-time) of the target program",
                        action="store_true")
    parser.add_argument('-n', '--number',
                        help="outputs the number of function calls of the target program",
                        action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    
    args = handle_wel_args()
    # read_stdin()
    # pr = cProfile.Profile()
    # pr.enable()
    tracemalloc.start(25)
    subprocess.run(args.programs)
    # pr.disable()
    # pr.print_stats()
    display_trace()
    read_resource(resource.RUSAGE_CHILDREN)
