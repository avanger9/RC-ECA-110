import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv
import skimage.filters.thresholding as th

#.......... CARREGA DE FITXERS NUMPY ............

trlb = np.load('array/train_labels_array.npy')
trim = np.load('array/train_images_array.npy')
telb = np.load('array/test_labels_array.npy')
teim = np.load('array/test_images_array.npy')
print("Training Set Labels shape ::",trlb.shape)
print("Training Set Image shape ::",trim.shape)
print("Test Set Labels shape ::",telb.shape)
print("Test Set Image shape ::",teim.shape)

#................... BINARITZACIÓ PER OTSU ...............
im = trim[0]
x, y = im.shape

plt.figure()
plt.imshow(im, cmap='gray'), plt.title('Imatge sense binaritzar')
plt.show()

#ret1, th1 = cv.threshold(im, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
th = th.threshold_otsu(im)
print(th)

binary = np.zeros((x,y), dtype=int)

for i in range(x):
    for j in range(y):
        if im[i][j] >= th:
            binary[i][j] = 1


plt.figure()
plt.imshow(binary, cmap='gray'), plt.title('Imatge binaritzada amb 0 i 1')
plt.show()


""" Hauria de funcionar, pero no es veu be
plt.figure()

plt.imshow(im, cmap='gray')
plt.subplot(1,2,1)

plt.imshow(binary, cmap='gray')
plt.subplot(1,2,2)

plt.show()
"""
