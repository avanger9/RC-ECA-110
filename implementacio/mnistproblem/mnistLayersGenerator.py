#!../../python3.9/bin/python

import numpy as np

def generateMnistInput():
    trainI = np.load('../../mnist/array/train_images_array.npy')
    trainL = np.load('../../mnist/array/train_labels_array.npy')
    testI = np.load('../../mnist/array/test_images_array.npy')
    testL = np.load('../../mnist/array/test_labels_array.npy')
    return trainI, trainL, testI, testL

def generateLayers(mnist):
    images, x, y = mnist.shape
    u = np.zeros((images,x,y,8), dtype=int)
    print(u.shape)
    import time
    for k in range(images):
        start_time = time.time()
        for i in range(x):
            for j in range(y):
                num_byte = mnist[k][i][j]
                num_byte = format(num_byte, '08b')
                for m in range(8):
                    u[k][i][j][7-m] = int(num_byte[m])
        print('--- %s seconds ---', '%.3f' % (time.time() - start_time), 'num bucle:', k)
    return u


if __name__ == '__main__':
    ti, tl, tti, ttl = generateMnistInput()
    print('----------- ENTRADA DEL MNIST -------------')
    print('mida dels train:', ti.shape, ',', tl.shape,
          'i mida dels test:', tti.shape, ',', ttl.shape,
          '\n-----------------------------------------')

    test2 = ti[0][10][12]
    test = ti[0][0][0]
    print(test)
    """
    vector u on guardarem els bits de més a menys pes de les 8 capes
    """
    bit = format(test, '08b')
    print('Prova per passar un número decimal a binari:', bit)
    print(bit[1])

    # u = generateLayers(ti)
    # np.save('train_images_layers_array.npy', u)
