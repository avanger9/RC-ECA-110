#!../../python3.9/bin/python

import numpy as np

def generateMnistInput():
    trainI = np.load('../../mnist/array/train_images_array.npy')
    trainL = np.load('../../mnist/array/train_labels_array.npy')
    testI = np.load('../../mnist/array/test_images_array.npy')
    testL = np.load('../../mnist/array/test_labels_array.npy')
    return trainI, trainL, testI, testL
