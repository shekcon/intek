def show(nums):
    print(" ".join([str(num) for num in nums]))


def bubble(nums):
    size = len(nums)
    for i in range(size):
        for j in range(size - i - 1):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
                show(nums)


def insert(nums):
    size = len(nums)
    for i in range(1, size):
        j = i - 1
        key = nums[i]
        while j >= 0 and key < nums[j]:
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = key
        if j + 1 != i:
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
        L = nums[: mid]  # Dividing the array elements
        R = nums[mid:]  # into 2 halves
        merge(L)  # Sorting the first half
        merge(R)  # Sorting the second half
        i = j = k = 0
        # Copy data to temp arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                nums[k] = L[i]
                i += 1
            else:
                nums[k] = R[j]
                j += 1
            k += 1
        # Checking if any element was left
        while i < len(L):
            nums[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            nums[k] = R[j]
            j += 1
            k += 1
        show(nums)
