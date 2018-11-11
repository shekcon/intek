#!/usr/bin/env python3
# set interpreter
from argparse import ArgumentParser
import json
from class_smartdb import Smart_DB
import sys


'''
# TODO: format data
first_name,last_name,username,age,gender,city
'''


def read_pattern(js_file):
    with open(js_file, "r") as f:
        patterns = json.load(f)
    return Smart_DB(patterns)


# def read_database():
#     data = []
#     for line in sys.stdin:
#         line = line.strip()
#         line = line.split(',')
#         line[3] = int(line[3])
#         data.append(line)
#     return data


def main():
    args = handle_wel_args()
    process = read_pattern(args.json)
    for line in sys.stdin:
        line = line.strip().split(',')
        line[3] = int(line[3])
        process.find(line)
    process.show()


def handle_wel_args():
    parser = ArgumentParser()
    parser.add_argument(
        'json',  help="set requirement to show data on terminal")
    return parser.parse_args()


if __name__ == '__main__':
    main()
