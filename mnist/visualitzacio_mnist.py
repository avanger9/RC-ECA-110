#!../python3.9/bin/python

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

#%matplotlib inline

trlb = np.load('array/train_labels_array.npy')
trim = np.load('array/train_images_array.npy')
telb = np.load('array/test_labels_array.npy')
teim = np.load('array/test_images_array.npy')

im = trim[0]
x, y = im.shape

fig = plt.figure()
plt.imshow(im, cmap='gray')
plt.show()
plt.imshow(trim[2], cmap='gray')
plt.show()
plt.imshow(trim[1], cmap='gray')
plt.show()
plt.imshow(trim[3], cmap='gray')
plt.show()
