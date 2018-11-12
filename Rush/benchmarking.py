#!/usr/bin/env python3
import argparse
import subprocess
import resource
import cProfile
import pstats


# import pstats

def memory_allocation():
    '''
    ru_maxrss: maximum resident set size
    '''
    memory_usage = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    print('Memory usage: ' + str(memory_usage) + ' KB')


def run_time():
    '''
    ru_utime: time in user mode (float)
    '''

    run_time = resource.getrusage(resource.RUSAGE_CHILDREN).ru_utime
    print('Execution time: ' + str(run_time) + 's')


def num_function_calls(file):
    '''
    compile(source, filename, mode) -> return a code object
    The mode argument specifies what kind of code must be compiled:
    - ‘exec’: source consists of a sequence of statements
    - ‘eval’: source consists of a single expression
    - ‘single’: source consists of a single interactive statement

    ex: file: ./smart_db.py
    -> file[2:]: smart_db.py
    '''

    compile_target_file = compile(open(file, "r").read(), file, 'exec')
    pr = cProfile.Profile()
    pr.enable()
    pr.run(compile_target_file)
    pr.disable()
    ps = pstats.Stats(pr).strip_dirs().sort_stats('calls')
    ps.print_stats()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', help='output the memory allocation of the target\
                        program', action='store_true',)
    parser.add_argument('-t', help='output the execution time (run-time) of\
                        the target program', action='store_true')
    parser.add_argument('-n', help='output the number of function\
                        calls of the target program',
                        action='store_true')
    parser.add_argument('program', help='target program', type=str, nargs='+')
    args = parser.parse_args()
    program = args.program
    subprocess.run(program)
    if args.m:
        memory_allocation()
    if args.t:
        run_time()
    if args.n:
        num_function_calls(program[0])
    # run with -t if no option is passed
    if not args.m and not args.t and not args.n:
        run_time()


if __name__ == '__main__':
    main()
