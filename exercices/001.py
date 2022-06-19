from math import factorial
from time import perf_counter


def my_factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)


ti = perf_counter()
for i in range(1000):
    my_factorial(i)
tf = perf_counter()
print(f'my_facorial time: {tf-ti}')

ti = perf_counter()
for i in range(1000):
    factorial(i)
tf = perf_counter()
print(f'facorial time: {tf-ti}')
