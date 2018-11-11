#!/usr/bin/env python3
# set interpreter
from argparse import ArgumentParser
import json
from class_smartdb import Smart_DB
import sys
import tracemalloc
import cProfile
import resource
'''
# TODO: format data
first_name,last_name,username,age,gender,city
'''


def read_pattern(js_file):
    with open(js_file, "r") as f:
        patterns = json.load(f)
    # print(patterns)
    # print(len(patterns))
    return Smart_DB(patterns)


def read_database():
    data = []
    for line in sys.stdin:
        line = line.strip()
        line = line.split(',')
        line[3] = int(line[3])
        data.append(line)
    return data

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

def main():
    tracemalloc.start(25)
    args = handle_wel_args()
    pr = cProfile.Profile()
    pr.enable()
    process = read_pattern(args.json)
    print("-Select: %s\n-Where: %s\n-Result:" % (
        process.select, process.compare))
    process.find(read_database())
    process.show()
    pr.disable()
    pr.print_stats()
    read_resource(resource.RUSAGE_SELF)
    


def handle_wel_args():
    
    parser = ArgumentParser()
    parser.add_argument(
        'json',  help="set requirement to show data on terminal")
    return parser.parse_args()


if __name__ == '__main__':
    main()
