def rotateImage(a):
    return list(zip(*reversed(a)))


a = [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]

print(rotateImage(a))
