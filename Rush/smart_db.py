#!/usr/bin/env python3
# set interpreter
from argparse import ArgumentParser
from json import load
from class_smartdb import Finder
from sys import stdin


'''
# TODO: format data
first_name,last_name,username,age,gender,city
'''


def read_pattern(js_file):
    with open(js_file, "r") as f:
        queries = load(f)
    return Finder(queries)


def read_database():
    data = []
    for line in stdin:
        line = line.strip().split(',')
        line[3] = int(line[3])
        data.append(line)
    return data


def main():
    args = handle_wel_args()
    process = read_pattern(args.json)
    process.find(read_database())
    process.show()


def handle_wel_args():
    parser = ArgumentParser()
    parser.add_argument('json',  help="set requirement to show data on terminal")
    return parser.parse_args()


if __name__ == '__main__':
    main()
