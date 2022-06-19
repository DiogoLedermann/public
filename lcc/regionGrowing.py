from skimage import io, img_as_float
from skimage.filters import gaussian
from matplotlib import pyplot as plt
import numpy as np
np.set_printoptions(precision=2, linewidth=np.inf)

input = np.array(img_as_float(io.imread('images/ex.tiff', as_gray=True)))
print(input)
print()

h, w = len(input), len(input[0])

output = np.zeros((len(input[0]), len(input)))

min = input.min()
max = input.max()

threshold = (max - min) / 2

seeds = [
    (5 , 5 ),
    (10, 14),
    (14, 7 ),
]

regions = []

for i, seed in enumerate(seeds):
    r, c = seed
    output[r, c] = i + 1

    top = (r - 1, c)
    right = (r, c + 1)
    bottom = (r + 1, c)
    left = (r, c - 1)

    neighbours = [
        top,
        right,
        bottom,
        left
    ]
    
    regions.append(neighbours)
        

while True:
    print(output)
    print()

    for i, region in enumerate(regions):
        new_neighbours = []

        for j, neighbour in enumerate(region):
            sR, sC = seeds[i]
            nR, nC = neighbour

            if input[sR, sC] - input[nR, nC] < threshold:
                output[nR, nC] = i + 1

                top = (nR - 1, nC)
                right = (nR, nC + 1)
                bottom = (nR + 1, nC)
                left = (nR, nC - 1)

                neighbours = [
                    top,
                    right,
                    bottom,
                    left
                ]

                for neighbour in neighbours:
                    r, c = neighbour
                
                    if 0 < r < h and 0 < c < w:
                        if output[r, c] == 0:
                            if (r, c) not in new_neighbours:
                                new_neighbours.append((r, c))
        
        regions[i] = new_neighbours
    
    if sum([len(region) for region in regions]) == 0:
        break
