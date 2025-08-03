# the first 2 algorithms can be used to find target, if the sorted list has only unique targets
# [_], [_, ], [ ,_, ], [ ,_, , ]
# if the searching range len is 1 or 2 -> the next loop might not decrease the search range


# narrow down the search range


# first 5
def findfirst(input, target):
    if len(input) == 0:
        return -1  # does not exist

    left = 0
    right = len(input) - 1
    while right - left > 1:
        mid = (left + right) // 2
        if input[mid] < target:
            left = mid + 1
        elif input[mid] > target:
            right = mid - 1
        else:
            right = (
                mid  # found the target, but the solution could be in the [LEFT...MID]
            )

    if input[left] == target:
        return left
    if input[right] == target:
        return right
    return -1  # target not found


# last 5
def findlast(input, target):
    if len(input) == 0:
        return -1  # does not exist

    left = 0
    right = len(input) - 1
    while right - left > 1:
        mid = (left + right) // 2
        if input[mid] < target:
            left = mid + 1
        elif input[mid] > target:
            right = mid - 1
        else:
            left = mid  # [MID...RIGHT] could contain the solution

    if input[right] == target:
        return right
    if input[left] == target:
        return left

    return -1  # target not found


# unless target is smaller than 1st element, otherwise there's always a solution
# target itself doesn't need to be in the input
def findfirstbefore(input, target):
    if len(input) == 0:
        return -1  # does not exist

    left = 0
    right = len(input) - 1
    while right - left > 1:
        mid = (left + right) // 2
        if input[mid] < target:
            left = mid  # mid could be a solution [MID...RIGHT]
        elif input[mid] > target:
            right = mid - 1
        else:
            right = mid - 1

    if input[right] < target:
        return right
    if input[left] < target:
        return left

    return -1  # target not found


# 8
def findfirstafter(input, target):
    if len(input) == 0:
        return -1  # does not exist

    left = 0
    right = len(input) - 1
    while right - left > 1:
        mid = (left + right) // 2
        if input[mid] < target:
            left = mid + 1
        elif input[mid] > target:
            right = mid
        else:
            left = mid + 1

    if input[left] > target:
        return left
    if input[right] > target:
        return right

    return -1  # target not found
