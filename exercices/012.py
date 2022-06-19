def search(array, target):
    left = 0
    right = len(array) - 1
    while left <= right:
        middle = (left + right) // 2
        if array[middle] == target:
            return middle
        else:
            if array[middle] < target:
                left = middle + 1
            else:
                right = middle - 1
    return -1

 


arr = [-2, 3, 4, 7, 8, 9, 11, 13]
t = 1

print(search(arr, t))
