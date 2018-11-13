from class_gui import Action


def bubble(nums):
    steps = []
    size = len(nums)
    for i in range(size):
        unsorted = False
        for j in range(size - i - 1):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
                unsorted = True
                # steps.append(('compare','swap',j, j+1))
                steps.append(Action('swap', [j, j+1]))
            else:
                # steps.append(('compare','noswap',j, j+1))
                steps.append(Action('noswap', [j, j+1]))
                pass
        # is list of integer sorted
        # steps.append(('compare','finish', size - i - 1, size - i - 1))
        steps.append(Action('finish', [size - i - 1]))
        if not unsorted:
            steps.append(Action('completed'))
            break
    return steps


def insert(nums):
    steps = []
    size = len(nums)
    steps.append(Action('noswap', [0]))
    steps.append(Action('temp', [0]))
    steps.append(Action('noswap', [0]))
    steps.append(Action('clean', [0]))
    for i in range(1, size):
        left = i - 1
        key = nums[i]
        steps.append(Action('noswap', [i]))
        steps.append(Action('temp', [i]))
        # find positon of key
        while left >= 0 and key < nums[left]:
            # assign right of left equal left
            nums[left + 1] = nums[left]
            steps.append(Action('noswap', [left + 1, left]))
            steps.append(Action('swap', [left + 1, left]))
            left -= 1
        # assign key
        nums[left + 1] = key
        # take time find position of key
        if left + 1 == i:
            steps.append(Action('noswap', [i]))
            steps.append(Action('noswap', [i]))
        elif left >= 0 and key > nums[left]:
            steps.append(Action('noswap', [left]))
        steps.append(Action('clean', [left + 1]))
        steps.append(Action('finish', [i]))
    steps.append(Action('completed'))
    return steps


def quick(nums, start, end, steps):
    if (start < end):
        # find position of pivot
        pivot_pos = partition(nums, start, end, steps)
        # show value pivot
        steps.append(Action('finish', [pivot_pos]))
        # show list of number
        # quick sort on left of pivot not include pivot
        quick(nums, start, pivot_pos - 1, steps)
        # quick sort on right of pivot not include pivot
        quick(nums, pivot_pos + 1, end, steps)
        return steps
    else:
        steps.append(Action('finish', [start]))


def partition(nums, start, end, steps):
    # get middle between start and end
    index = (end - start) // 2 + start
    # swap end and middle
    steps.append(Action('noswap', [index]))
    nums[index], nums[end] = nums[end], nums[index]
    steps.append(Action('swap', [index, end]))
    steps.append(Action('noswap', [end]))
    steps.append(Action('temp', [end]))
    # take pivot
    pivot = nums[end]
    # define leftmark, rightmark
    left, right = start, end - 1
    steps.append(Action('noswap', [left, right]))
    # run only left is still smaller than right
    while left <= right:
        # if number at left bigger pivot and number at right smaller pivot
        # then swap left and right
        # increase left
        if nums[left] > pivot and nums[right] <= pivot:
            nums[left], nums[right] = nums[right], nums[left]
            if left != right:
                steps.append(Action('swap', [left, right]))
            left += 1
        # if left smaller pivot then
        # increase left
        elif nums[left] <= pivot:
            steps.append(Action('noswap', [left, right]))
            left += 1
        # default decrease right
        else:
            steps.append(Action('noswap', [left, right]))
            right -= 1
    # swap pivot value with number at left
    steps.append(Action('clean', [end]))
    steps.append(Action('noswap', [end]))
    nums[end], nums[left] = nums[left], nums[end]
    if left != end:
        steps.append(Action('swap', [left, end]))
    # return position of pivot
    return left


def merge(nums):
    if len(nums) > 1:
        mid = len(nums) // 2  # Finding the mid of the array
        left_half = nums[: mid]  # Dividing the array elements
        right_half = nums[mid:]  # into 2 halves
        merge(left_half)  # Sorting the first half
        merge(right_half)  # Sorting the second half
        left = right = index = 0
        # Copy data to temp arrays left_half[] and right_half[]
        while left < len(left_half) and right < len(right_half):
            if left_half[left] < right_half[right]:
                nums[index] = left_half[left]
                left += 1
            else:
                nums[index] = right_half[right]
                right += 1
            index += 1
        # Checking if any element was left
        while left < len(left_half):
            nums[index] = left_half[left]
            left += 1
            index += 1
        while right < len(right_half):
            nums[index] = right_half[right]
            right += 1
            index += 1
