#!../../python3.9/bin/python

import os
import numpy as np
import tensorflow

from tensorflow.keras.datasets import mnist

(X_train, y_train), (X_test, y_test) = mnist.load_data()

os.system('mkdir mnist_array')

np.save('mnist_array/train_images_array.npy', X_train)
np.save('mnist_array/train_labels_array.npy', y_train)
np.save('mnist_array/test_images_array.npy', X_test)
np.save('mnist_array/test_labels_array.npy', y_test)

print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)
