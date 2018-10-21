#!/usr/bin/env  python3
from sys import stdin, stdout, stderr
from random import choice
from string import ascii_uppercase
from collections import deque
from parent import Track
from time import sleep
from os import system


resources = []
maze = []
player = ()
path = deque()
enemy = {}
other_player = ""
# track_maze = []
path_enemy = []
# define direction vertor of move
direction = {
    (-1, 0): "MOVE UP",  # up
    (1, 0): "MOVE DOWN",  # down
    (0, -1): "MOVE LEFT",  # left
    (0, 1): "MOVE RIGHT"   # rightif path:
}


def save_debug(data):
    system("echo \"%s\" >> debug.txt" % (data))


def get_value(pos):
    # return value at that direction
    return maze[pos[0]][pos[1]]


def get_pos(location, direc):
    # return position at that direction
    return (location[0] + direc[0], location[1] + direc[1])


def valid_move(location):
    global track_maze
    child = []
    destination = []
    flag = False
    for move in direction.keys():
        pos = get_pos(location, move)
        value = get_value(pos)
        # found wall then next another direction
        if value == "#" or track_maze.is_mark(pos):
            continue
        elif value == "o" or value == "!":
            # found destination
            flag = True
            child.append(pos)
            track_maze.mark(pos)
            destination = pos
            break
        # valid direction
        else:
            # mark used
            track_maze.mark(pos)
            # add it into list of valid move
            child.append(pos)
    return child, flag, destination


def mark_parent(valids, parent, child_parent):
    for child in valids:
        # add mapping between child and parent
        child_parent[child] = parent
    return child_parent


def location_player(letter):
    global maze
    return all_location_in_maze(letter)[0]


def back_track_path(destination, parents, player_pos):
    path = [destination]
    pos = parents[destination]
    # found path from destination to start
    while pos != player_pos:
        path.append(pos)
        pos = parents[pos]
    # reverse path coz found end to start
    return path[::-1]


def get_direction(location):
    global player
    return (location[0] - player[0], location[1] - player[1])


def update_maze():
    global maze
    # reset maze
    maze.clear()
    data = stdin.readline().strip()
    while data != "":
        maze.append(list(data))
        data = stdin.readline().strip()


def return_maze(data):
    stdout.write("%s\n\n" % (data))


def wait_maze():
    """ get infomation maze want """
    return stdin.readline()


def breadth_first_search(player, path=[], enemy=[]):
    global track_maze
    global resources
    track_maze.empty_track()
    track_maze.mark(player)
    child_parent = {}
    top_parent = deque([[player]])
    count_time = 0
    while not path:
        parent = top_parent.popleft()
        for top in parent:
            # find valid move of top
            valids, flag, destination = valid_move(top)
            # store infomation top of valid move
            child_parent = mark_parent(valids, top, child_parent)
            # add valid move into queue
            top_parent.append(valids)
            # flag == True then found destination
            if flag:
                path = deque(back_track_path(destination,
                                             child_parent,
                                             player))
                count_time += 1
                # check is best path and if not have good path
                # run at that path search at next time
                if (enemy and check_smart_path(path, enemy)
                   and len(resources) != count_time):
                    path.clear()
    return path


def check_smart_path(path, enemy):
    path = list(path)
    # check is best path
    for player in enemy:
        if player[-1] == path[-1] and len(player) < len(path):
            return True
    return False


def is_other_player(pos):
    global maze
    global other_player
    value = get_value(pos)
    return value in other_player


def debug(data):
    # show infomation with red text on terminal
    stderr.write("%s\n\n" % (data))


def found_enemy(player_mine):
    # found pos of other player
    global enemy
    global other_player
    global ascii_uppercase
    other_player = ""
    index = ascii_uppercase.index(player_mine)
    letter_enemy = ascii_uppercase[:index] + ascii_uppercase[index+1:]
    location_enemy = all_location_in_maze(letter_enemy)
    # get letter of enemy
    for pos in location_enemy:
        other_player += get_value(pos)
    return location_enemy


def check_resources():
    global resources
    global maze
    global path
    flag = False
    # have resources check is different
    if resources:
        for pos in resources:
            value = get_value(pos)
            if not (value in "o!"):
                flag = True
                break
    update_resources()
    # if have different reset path find path again
    if flag:
        path.clear()


def all_location_in_maze(pattern):
    # found all location of pattern in maze
    global maze
    locations = []
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            result = get_value((row, col))
            if result in pattern:
                locations.append((row, col))
    return locations


def update_resources():
    # find all location of resource after maze update
    global maze
    global resources
    resources.clear()
    resources = all_location_in_maze("o!")


def get_path_enemy(all_other_player):
    enemy_path = []
    if not path:
        enemy_path.clear()
        # found path each enemy
        for letter_player in all_other_player:
            enemy_path.append(breadth_first_search(letter_player))
    return enemy_path


def is_valid_move(move_player):
    global track_maze
    global path
    if is_other_player(move_player):
        # delete pathing move
        path.clear()
        track_maze.empty_track()
        # found again valid move at player
        player_choices, _, _ = valid_move(player)
        # random choice from valid move not have another player
        move_player = choice(player_choices)
        while is_other_player(move_player) or len(player_choices) == 1:
            move_player = choice(player_choices)
    return move_player


def main():
    # define variable global use
    global maze
    global path
    global player
    global track_maze
    command = wait_maze()
    # use communication with virtual machine
    while command != "":
        if "HELLO" in command:
            return_maze("I AM Sang")
        elif "YOU ARE" in command:
            """ store letter is playing"""
            player_character = command[-2]
            return_maze("OK")
        elif "MAZE" in command:
            # store maze
            update_maze()
            # create object tracking map
            track_maze = Track(maze)
            player = location_player(player_character)
            all_other_player = found_enemy(player_character)
            # resource changed clear path find path again
            check_resources()
            # found path enemy
            enemy_path = get_path_enemy(all_other_player)
            # found path if dont have ?
            path = breadth_first_search(player, path, enemy_path)
            # get location move
            move_player = path.popleft()
            # direction move is another player
            move_player = is_valid_move(move_player)
            # return direction move
            return_maze(direction[get_direction(move_player)])
        command = wait_maze()


if __name__ == "__main__":
    main()
