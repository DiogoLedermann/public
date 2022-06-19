from skimage import io, img_as_float
from skimage.filters import gaussian
from matplotlib import pyplot as plt

# unsharpened = original + k * (original - blured)
original = img_as_float(io.imread('0576.tiff', as_gray=True))
blured = gaussian(original, sigma=2, mode='constant', cval=0)
k = 2
unsharpened = original + k * (original - blured)

plt.imshow(unsharpened, cmap='gray')
plt.show()
print('done')
