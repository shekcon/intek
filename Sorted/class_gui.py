import pyglet


class List_Number():
    rectangle = pyglet.image.load('./Resources/rectangle_s.png')
    numbers = []

    def __init__(self, list_integers, y=300, x=0):
        x = (1920 - (len(list_integers) * 100)) // 2
        for i, num in enumerate(list_integers):
            self.numbers.append(Number(str(num), i,
                                       self.rectangle,
                                       i * 100 + x,
                                       y))
        self.size = len(self.numbers)

    def __str__(self):
        return str(self.numbers)

    def __repr__(self):
        return str(self.numbers)

    def draw(self):
        for num in self.numbers:
            num.draw()

    def swap_index(self, pos):
        self.numbers[pos[1]].id = pos[0]
        self.numbers[pos[0]].id = pos[1]
        self.numbers[pos[0]], self.numbers[pos[1]
                                           ] = self.numbers[pos[1]], self.numbers[pos[0]]

    def sort_highlight(self, end=-1, mode='all', color='yellow'):
        if mode == 'all':
            for e in self.numbers:
                e.change_color(color=color)
        else:
            for i in range(end):
                self.numbers[i].change_color(color=color)

    def get(self, index_number):
        return self.numbers[index_number]


class Number():
    """
    Tasks: display for number on screen
    param: number inside image
    param: index is index of number in list_unsort
    param: image want show
    param: x in window
    param: y in window
    """
    red = (255, 0, 0, 255)
    white = (255, 255, 255, 255)
    yellow = (255, 255, 0, 255)

    def __init__(self, number, index, image, x, y, scale=1, compare=False, color=white):
        # declare attribute
        self.text = number
        self.isdraw = True
        self.id = index
        self.default_pos = (x, y)
        self.image = pyglet.sprite.Sprite(image, x=x, y=y)
        self.image.scale = scale
        # set fexible size for label
        if not compare:
            y += 30
            if len(number) == 2:
                x += 20
            elif len(number) >= 3:
                x += 12
            elif len(number) <= 1:
                x += 30
        else:
            x += 20
            y += 50
            color = self.red
        self.num = pyglet.text.Label(number, font_size=24, y=y,
                                     x=x, color=color)

    def draw(self):
        if self.isdraw:
            self.image.draw()
            self.num.draw()

    def change_color(self, color='red'):
        '''
        color: - red: compare
               - yellow: completed
               - white: queue
        '''
        if color == 'red':
            self.num.color = self.red
        elif color == 'yellow':
            self.num.color = self.yellow
        else:
            self.num.color = self.white

    def move(self, x, y):
        self.image.x += x
        self.image.y += y
        self.num.x += x
        self.num.y += y

    def __repr__(self):
        return "id:%s v:%s pos:(%s,%s)" % (self.id, self.num.text,
                                           self.default_pos[0],
                                           self.default_pos[1])

    def get_pos(self):
        return (self.image.x, self.image.y)

    def update_new_pos(self):
        self.default_pos = (self.image.x, self.image.y)


class Action():
    def __init__(self, action, data=[]):
        self.action = action
        if data and len(data) > 1 and data[0] != data[1]:
            if data[0] < data[1]:
                id1 = data[0]
                id2 = data[1]
            else:
                id1 = data[1]
                id2 = data[0]
            self.id1 = id1
            self.id2 = id2
            self.size = True
        else:
            self.size = False
            self.id = tuple(data)

    def __repr__(self):
        if self.size:
            return "%s (%s,%s)" % (self.action, self.id1, self.id2)
        else:
            return "%s  %s" % (self.action, self.id if self.id else "")

    def get_index(self):
        if self.size:
            return (self.id1, self.id2)
        return self.id


class HighLight():
    def __init__(self, list_numbers, algo):
        self.algo = algo
        self.numbers = list_numbers
        self.ishighlight = False
        self.isnothing = True

    def get_data(self, indexs, mode='compare'):
        self.mode = mode
        self.indexs = indexs
        if self.mode == 'compare':
            color = 'red'
        else:
            color = 'yellow'
        if self.algo == 'insert' and self.mode == 'finish':
            self.numbers.sort_highlight(indexs[0] + 1, mode='insert')
        else:
            for index in self.indexs:
                self.numbers.get(index).change_color(color=color)
        self.count = 0
        self.ishighlight = True
        self.isnothing = False

    def set_normal(self):
        if not self.isnothing and self.mode == 'compare':
            for index in self.indexs:
                self.numbers.get(index).change_color(color='white')

    def highlighting(self):
        if self.count <= 50:
            self.count += 1
        else:
            self.ishighlight = False


class Swap(object):
    '''
    Task: swap positon 2 number
    + init:
    - param: list of object Number
    - param: move  - normal  : 2 number move different way
                   - cross   : 2 number move cross each other
    + get_data: take information of 2 index need swap
    + swapping: swap 2 number in slow way

    '''

    def __init__(self, numbers, move='normal'):
        self.numbers = numbers
        self.how_move = move
        self.is_swap = False

    def get_data(self, id1, id2):
        self.swap = [self.numbers.get(id1), self.numbers.get(id2)]
        self.default_pos = self.swap[1].default_pos
        self.default = 5
        self.up = 0
        self.down = 0
        self.right = False
        self.finish = False
        self.switch = False
        self.is_swap = True

    def get_id(self):
        return (self.swap[0].id, self.swap[1].id)

    def swapping(self):
        if self.how_move == 'normal':
            self.move()
        else:
            self.move_cross()

    def completed(self):
        self.numbers.swap_index(self.get_id())
        self.is_swap = False
        self.swap[0].move(-5, 0)
        self.swap[1].move(5, 0)
        self.swap[0].update_new_pos()
        self.swap[1].update_new_pos()

    def move(self):
        if self.up <= self.default:
            self.swap[0].move(0, 15)
            self.swap[1].move(0, -15)
            self.up += 1
        elif self.swap[0].image.x <= self.default_pos[0]:
            self.swap[0].move(5, 0)
            self.swap[1].move(-5, 0)
        elif self.down <= self.default:
            self.swap[0].move(0, -15)
            self.swap[1].move(0, 15)
            self.down += 1
        else:
            self.completed()

    def move_cross(self):
        if self.swap[0].image.x <= self.default_pos[0]:
            self.swap[0].move(5, 0)
            self.swap[1].move(-5, 0)
        else:
            self.completed()
