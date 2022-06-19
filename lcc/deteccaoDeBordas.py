import numpy as np
import matplotlib.pyplot as plt
from skimage import io, img_as_float

original = img_as_float(io.imread('images/0576.tiff', as_gray=True))

vertical_filter = [
    [-1, -2, -1],
    [ 0,  0,  0],
    [ 1,  2,  1],
]
horizontal_filter = [
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1],
]

n, m = original.shape

edges_img = np.zeros_like(original)
for r in range(3, n-2):
    for c in range(3, m-2):
        local_pixels = original[r-1:r+2, c-1:c+2]

        vertical_trasformed_pixels = vertical_filter * local_pixels
        vertical_score = vertical_trasformed_pixels.sum()/4

        horizontal_trasformed_pixels = horizontal_filter * local_pixels
        horizontal_score = horizontal_trasformed_pixels.sum()/4

        edge_score = (vertical_score**2 + horizontal_score**2)**0.5
        edges_img[r, c] = edge_score*3
edges_img = edges_img / edges_img.max()

plt.imshow(edges_img, cmap='grey')
plt.show()
