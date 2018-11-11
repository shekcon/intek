#!/usr/bin/env python3
# set interpreter
from argparse import ArgumentParser
import sys
import subprocess
import resource
import tracemalloc
import os
import cProfile
import importlib
import pstats


def read_resource(usage):
    RESOURCES = [('ru_utime', 'User time'),
                 ('ru_stime', 'System time'),
                 ('ru_maxrss', 'Usage memory')
                 ]
    usage = resource.getrusage(usage)
    for name, desc in RESOURCES:
        print('{:<15} = {}'.format(
            desc, str(getattr(usage, name))
            + " s" if name != 'ru_maxrss' else str(getattr(usage,
                                                           name) // 1024)
            + " KB"))


def display_trace():
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    for stat in top_stats:
        print(stat)


def main():
    global target
    args = handle_wel_args()
    pr = cProfile.Profile()
    pr.enable()
    # pr = cProfile.Profile()
    # subprocess.run(args.programs, stdout=subprocess.PIPE)
    subprocess.run(args.programs)
    pr.disable()
    pr.print_stats()
    read_resource(resource.RUSAGE_CHILDREN)


def handle_wel_args():
    parser = ArgumentParser(usage='./benchmarking.py [option]\
 target', description='benchmarking calculate the\
 memory allocation, run-time performance and number of function\
 calls of the program')
    parser.add_argument('programs', nargs="*")
    parser.add_argument('-m', '--memory',
                        help="outputs the memory allocation \
of the target program",
                        action="store_true")
    parser.add_argument('-t', '--time',
                        help="outputs the execution time \
(run-time) of the target program",
                        action="store_true")
    parser.add_argument('-n', '--number',
                        help="outputs the number of \
function calls of the target program",
                        action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    main()
