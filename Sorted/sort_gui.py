#!/usr/bin/env python3

from pic_gui import Number, Swap
import pyglet
from pyglet.window import key, mouse
from argparse import ArgumentParser
import sort_algo


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
window = pyglet.window.Window(1920,1080)
circle = pyglet.image.load('./Resources/rectangle_s.png')
# circle.width = 50
# circle.height = 50
# num_circle = pyglet.sprite.Sprite(circle, x=100, y=100)

num_circle = []
size = len(deck_sort.nums)
x = (1920 - (size * 100)) // 2
y = 500
for i in deck_sort.nums:
    num_circle.append(Number(str(i), circle, x, y))
    x += 100
# num_circle[0].num.color = (255, 255, 255, 255)
# num_circle2 = Number('-30', circle, 200, 100)
background = pyglet.image.load('./Resources/background.jpg')
backg = pyglet.sprite.Sprite(background, x=0, y=0)
swap_num = Swap(num_circle[0], num_circle[1])
index = 0


@window.event
def on_draw():
    window.clear()
    backg.draw()
    for num in num_circle:
        num.draw()


def bubble_sort(dt):
    global swap_num, index
    swap_num.swap_pos()
    if swap_num.finish:
        print(index)
        index += 1
        if index > len(num_circle) - 1:
            swap_num = Swap(num_circle[index], num_circle[0])
        else:
            swap_num = Swap(num_circle[index], num_circle[index+1])



# def swap_pos(num1, num2):
#     default_pos = num1.default_pos
#     pos_now = num1.get_pos()
#     if pos_now[1] <= default_pos[1] + 200:
#         num1.update(0, 20)
#     elif pos_now[0] <= num2.default_pos[0] - 5:
#         num1.update(10, 0)
    # elif num1.
if deck_sort.gui:
    pyglet.clock.schedule_interval(bubble_sort, 1/60)
    pyglet.app.run()
