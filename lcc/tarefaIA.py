import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cv2 import imread
from skimage.exposure import equalize_adapthist
from skimage.filters import gaussian, sobel
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import time
from sklearn.model_selection import StratifiedKFold


def my_subplots(shape, data):
    rows, cols = shape
    
    fig, axs = plt.subplots(rows, cols, constrained_layout=True)

    if rows == 1:
        for i, (title, image) in enumerate(data):
            axs[i % cols].set_title(title)
            axs[i % cols].imshow(image)
    else:
        for i, (title, image) in enumerate(data):
            axs[i // cols, i % cols].set_title(title)
            axs[i // cols, i % cols].imshow(image)

    for ax in axs.flat:
        ax.label_outer()

    plt.show()


original = imread('images/gfrp.tiff', 0)

data = [
    ('original', original),
    ('equalized', equalize_adapthist(original)),
    ('gaussian 5', gaussian(original, sigma=5)),
    ('sobel', sobel(original)),
    ('labeled', imread('images/labeled_gfrp.tiff', 0))
]

my_subplots((1, 5), data)

df = pd.DataFrame()

for title, image in data:
    df[title] = image.reshape(-1)

X = df.drop(labels='labeled', axis=1)
Y = df['labeled']

# X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)
skf = StratifiedKFold(n_splits=10)
skf.get_n_splits(X, Y)
accuracy = []
times = []

for train_index, test_index in skf.split(X,Y):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    Y_train, Y_test = np.ravel(pd.DataFrame(Y).iloc[train_index]), np.ravel(pd.DataFrame(Y).iloc[test_index])

    classifier = RandomForestClassifier(n_estimators=10)
    
    start = time.time()
    classifier.fit(X_train, Y_train)
    Y_pred = classifier.predict(X_test)
    score = accuracy_score(Y_pred, Y_test)
    accuracy.append(score)
    times.append(time.time() - start)

print("RFC: ")
print("    Accuracy = ", np.array(accuracy).mean())
print("    Average Time = ", np.array(times).mean())

# Y_pred = classifier.predict(X_test)

# score = accuracy_score(Y_test, Y_pred)
# print(f'Accuracy: {score*100:.2f}%')

feature_imp = pd.Series(classifier.feature_importances_).sort_values(ascending=False)
print(feature_imp)

output = classifier.predict(X)

data = [
    data[0],
    data[-1],
    ('output', output.reshape(original.shape))
]

my_subplots((1, 3), data)
