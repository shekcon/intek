#!/usr/bin/env python3

from class_gui import List_Number, Swap, HighLight
import pyglet
from pyglet.window import key
from argparse import ArgumentParser
# import sort_algo
import sort_step
import time




# thoughbubble = pyglet.image.load('./Resources/idea.png')
# idea = ""  # Number("", "", thoughbubble, 200, 600, 0.5)
window = pyglet.window.Window(1920, 1080)
background = pyglet.image.load('./Resources/background.jpg')
backg = pyglet.sprite.Sprite(background, x=0, y=0)


@window.event
def on_draw():
    window.clear()
    backg.draw()
    list_numbers.draw()
    time.sleep(0.02)


@window.event
def on_key_press(symbol, modifiers):
    global flag, auto
    if symbol == key.RIGHT:
        flag = True
    if symbol == key.UP:
        if auto:
            auto = False
        else:
            auto = True


def set_step():
    global list_numbers, steps, swap_gui, move, flag, compare, args
    compare.set_normal()
    act = steps.pop(0)
    print(act)
    if act.action == "swap":
        compare.get_data(act.get_index())
        swap_gui.get_data(act.id1, act.id2)
    elif act.action == 'noswap':
        compare.get_data(act.get_index())
    elif act.action == 'finish':
        compare.get_data(act.get_index(), act.action)
    elif act.action == 'completed':
        list_numbers.sort_highlight()
    flag = False


def sorting_algo(dt):
    global swap_gui, steps, flag, auto, list_numbers, compare
    if swap_gui.is_swap:
        swap_gui.swapping()
    if compare.ishighlight:
        compare.highlighting()
    if (not swap_gui.is_swap and not compare.ishighlight and
            (flag or auto) and steps):
        set_step()


# def show_temp(command):
    # global stored, list_numbers, temp
    # list_numbers[command].isdraw = False
    # temp = Number(list_numbers[command].text, -1, circle, 1920 // 2 - 50, 500)
    # stored = list_numbers[command]


# def clean_temp():
#     global stored, temp
#     stored.isdraw = True
#     temp = ""
#     stored = ""


def handle_welcome_args():
    parser = ArgumentParser()
    parser.add_argument('nums',  metavar='N', nargs="+", type=int,
                        help="an integer for the list to sort")
    parser.add_argument('--algo', metavar='ALGO', type=str, default="bubble",
                        choices=["bubble", 'insert', 'quick', 'merge'],
                        help="specify which algorithm to use for sorting among\
    [bubble | insert | quick | merge], default bubble")
    parser.add_argument('--gui',
                        help="visualise the algorithm in GUI mode",
                        action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    global steps, list_numbers, args, compare, flag, auto
    args = handle_welcome_args()
    if args.gui:
        flag = False
        auto = False
        list_numbers = List_Number(args.nums)
        move = 'normal'
        if args.algo == 'bubble':
            steps = sort_step.bubble(args.nums)
        elif args.algo == 'insert':
            move = 'cross'
            steps = sort_step.insert(args.nums)
        elif args.algo == 'quick':
            steps = sort_step.quick(args.nums, 0,
                                    len(args.nums) - 1, [])
        compare = HighLight(list_numbers, args.algo)
        swap_gui = Swap(list_numbers, move=move)
        pyglet.clock.schedule_interval(sorting_algo, 1/60)
        pyglet.app.run()
