def almostIncreasingSequence(sequence):
    for value in sequence:
        if sequence.remove(value) == sorted(sequence.remove(value)):
            return True
    return False


print(almostIncreasingSequence([1, 3, 2]))
