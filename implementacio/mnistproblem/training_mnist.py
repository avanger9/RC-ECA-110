#!../../python3.9/bin/python

import time
import numpy as np

def loadWs():
    ws = []
    for i in range(6):
        aux = np.load('train_ws_array/ws_train_arrayfile%d.npy' % (i+1))
        for k in range(10000):
            t = aux[k]
            ws.append(t)
    wstest = np.load('train_ws_array/ws_test_arrayfile.npy')
    return np.array(ws), wstest

def loadMnist():
    ti  = np.load('mnist_array/test_images_array.npy')
    tl  = np.load('mnist_array/test_labels_array.npy')
    tri = np.load('mnist_array/train_images_array.npy')
    trl = np.load('mnist_array/train_labels_array.npy')
    return tri, trl, ti, tl

def training():
    pass

def visualitzar(images, labels):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(20,4))
    for index, (image, label) in enumerate(zip(images[0:5], labels[0:5])):
        plt.subplot(1, 5, index + 1)
        plt.imshow(image, cmap=plt.cm.gray)
        plt.title('Training: %i\n' % label, fontsize = 20)
    plt.show()


if __name__ == '__main__':

    start_time = time.time()

    wstrain, wstest = loadWs()
    trainImages, trainLabels, testImages, testLabels = loadMnist()

    visualitzar(trainImages, trainLabels)
    training()

    print('--- %s seconds ---', '%.3f' % (time.time() - start_time))
