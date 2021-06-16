#!../../python3.9/bin/python

import numpy as np

def generateMnistInput():
    trainI = np.load('mnist_array/train_images_array.npy')
    trainL = np.load('mnist_array/train_labels_array.npy')
    testI = np.load('mnist_array/test_images_array.npy')
    testL = np.load('mnist_array/test_labels_array.npy')
    return trainI, trainL, testI, testL

def generateLayers(mnist):
    images, x, y = mnist.shape
    u = np.zeros((images,x,y,8), dtype=int)
    for k in range(images):
        for i in range(x):
            for j in range(y):
                num_byte = mnist[k][i][j]
                num_byte = format(num_byte, '08b')
                for m in range(8):
                    u[k][i][j][7-m] = int(num_byte[m])
    return u


if __name__ == '__main__':
    ti, tl, tti, ttl = generateMnistInput()
    print('----------- ENTRADA DEL MNIST -------------')
    print('mida dels train:', ti.shape, ',', tl.shape,
          'i mida dels test:', tti.shape, ',', ttl.shape,
          '\n-----------------------------------------')


    train_layers = generateLayers(ti)
    test_layers = generateLayers(tti)
    import os
    os.system('mkdir images_layers_generated')
    np.save('images_layers_generated/train_images_layers_array.npy', train_layers)
    np.save('images_layers_generated/test_images_layers_array.npy', test_layers)
