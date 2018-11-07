import pyglet
import time
class Number():
    """display for number on window.
    param: number inside image
    param: image want show
    param: x in window
    param: y in window
    """
    def __init__(self, number, image, x, y):
        self.default_pos = (x, y)
        self.image = pyglet.sprite.Sprite(image, x=x, y=y)
        if len(number) == 2:
            self.num = pyglet.text.Label(number, font_size=24, y=y+30,
                                         x=x+20, color = (255, 255, 255, 255))
        elif len(number) == 3:
            self.num = pyglet.text.Label(number, font_size=24, y=y+30,
                                         x=x+12, color = (255, 255, 255, 255))
        elif len(number) == 1:
            self.num = pyglet.text.Label(number, font_size=24, y=y+30,
                                         x=x+30, color = (255, 255, 255, 255))
    def draw(self):
        self.image.draw()
        self.num.draw()

    def update(self, x, y):
        self.image.x += x
        self.image.y += y
        self.num.x += x
        self.num.y += y

    def get_pos(self):
        return (self.image.x, self.image.y)

class Swap(object):
    """docstring for Swap."""
    def __init__(self, num1, num2):
        self.default_pos = num2.default_pos
        # self.default_pos2 = num2.default_pos
        self.swap = [num1, num2]
        self.default = 0
        self.up = 0
        self.down = 0
        self.right = False
        self.finish = False

    def swap_pos(self):
        if not self.finish:
            if self.swap[0].image.x <= self.default_pos[0]:
                 self.right = True
            else:
                 self.right = False
            self.move()

    def move(self):
        if self.up <= 5:
            self.swap[0].update(0, 15)
            self.swap[1].update(0, -15)
            self.up += 1
            print('up')
        elif self.right:
            self.swap[0].update(5, 0)
            self.swap[1].update(-5, 0)
            print('right')
        elif self.down <= 5:
            self.swap[0].update(0, -15)
            self.swap[1].update(0, 15)
            self.down += 1
            print('down')
        else:
            self.finish = True
