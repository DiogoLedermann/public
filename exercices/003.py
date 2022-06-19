x = [1, 2, 3, 4, 5]
y = [6, 7, 8, 9, 0]
target = 1

def pair_adds_to_target(a, b, v):
    for i in a:
        for j in b:
            if i + j == v:
                return True
    return False


print(pair_adds_to_target(x, y, target))
