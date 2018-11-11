def get_steps():
    global nums_sort, steps
    command = steps.pop(0)
    print(command)
    if command[0] == 'compare':
        show_compare(command)
    else:
        if swap_num:
            swap_num.completed()
        handle_swap_temp(command)
    if command[0] == 'finish' and deck_sort.algo == "insert":
        highlight_numbers(command[1])
    flag = False


def handle_swap_temp(command):
    global nums_sort, stored
    if len(command) > 1:
        if command[0] == 'start':
            show_temp(command[1])
        if stored and command[0] == 'clean':
            clean_insert()
        swap_num = Swap(nums_sort[command[1]],
                        nums_sort[command[2]],
                        mode=command[0],
                        move='cross')
        # swap_num = Swap(nums_sort[command[1]],
        #                 nums_sort[command[2]],
        #                 mode=command[0])
    else:
        highlight_numbers(len(nums_sort))

def show_compare(command):
    global idea
    if command[2] != command[3]:
        if command[2] > command[3]:
            compare = " > "
        elif command[2] < command[3]:
            compare = " < "
        else:
            compare = " = "
        text = str(command[2]) + compare + str(command[3]) + " -->" + command[1]
    else:
        text = str(command[2]) + " finish --> next element"
    idea = Number(text, "", thoughbubble,
                        200, 600, 0.5, True)