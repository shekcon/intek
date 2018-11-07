#!/usr/bin/env python3
# set interpreter

from argparse import ArgumentParser
import sort_algo

def handle_wel_args():
    global deck_sort
    parser = ArgumentParser()
    parser.add_argument('nums',  metavar='N',nargs="+", type=int,
                        help="an integer for the list to sort")
    parser.add_argument('--algo', metavar='ALGO', type=str, default="bubble",
                        choices=["bubble", 'insert', 'quick', 'merge'],
                        help="specify which algorithm to use for sorting among\
 [bubble | insert | quick | merge], default bubble")
    parser.add_argument('--gui',
                        help="visualise the algorithm in GUI mode",
                        action="store_true")
    deck_sort = parser.parse_args()


if __name__ == "__main__":
    handle_wel_args()
    if len(deck_sort.nums) > 15 and deck_sort.gui:
        print('Input too large')
    elif deck_sort.gui:
        # TODO: gui for sort algorithms
        pass
    else:
        if deck_sort.algo == "bubble":
            sort_algo.bubble(deck_sort.nums)
        elif deck_sort.algo == "insert":
            sort_algo.insert(deck_sort.nums)
        elif deck_sort.algo == "quick":
            sort_algo.quick(deck_sort.nums, 0, len(deck_sort.nums) - 1)
            # TODO: quick algorithms
        else:
            sort_algo.merge(deck_sort.nums)
            # TODO: merge algorithms