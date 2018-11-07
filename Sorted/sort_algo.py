def show(nums):
    print(" ".join([str(num) for num in nums]))


def bubble(nums):
    size = len(nums)
    for i in range(size):
        unsorted = False
        for j in range(size - i - 1):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
                unsorted = True
                show(nums)
        # is list of integer sorted
        if not unsorted:
            break


def insert(nums):
    size = len(nums)
    for i in range(1, size):
        left = i - 1
        key = nums[i]
        # find positon of key
        while left >= 0 and key < nums[left]:
            # assign front of left equal left
            nums[left + 1] = nums[left]
            left -= 1
        # assign key
        nums[left + 1] = key
        # take time find position of key
        if left + 1 != i:
            show(nums)


def quick(nums, start, end):
    if (start < end):
        # find position of pivot
        pivot_pos = partition(nums, start, end)
        # show value pivot
        print("P: %s" % (nums[pivot_pos]))
        # show list of number
        show(nums)
        # quick sort on left of pivot not include pivot
        quick(nums, start, pivot_pos - 1)
        # quick sort on right of pivot not include pivot
        quick(nums, pivot_pos + 1, end)


def partition(nums, start, end):
    # get middle between start and end
    index = (end - start) // 2 + start
    # swap end and middle
    nums[index], nums[end] = nums[end], nums[index]
    # take pivot
    pivot = nums[end]
    # define leftmark, rightmark
    left, right = start, end - 1
    # run only left is still smaller than right
    while left <= right:
        # if number at left bigger pivot and number at right smaller pivot
        # then swap left and right
        # increase left
        if nums[left] > pivot and nums[right] <= pivot:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
        # if left smaller pivot then
        # increase left
        elif nums[left] <= pivot:
            left += 1
        # default decrease right
        else:
            right -= 1
    # swap pivot value with number at left
    nums[end], nums[left] = nums[left], nums[end]
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
        show(nums)
