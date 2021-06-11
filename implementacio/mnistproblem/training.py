import numpy as np
import tensorflow

from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras import optimizers


def training(opt, wstrain, wstest, trainLabels, testLabels):


    trainLabels = to_categorical(trainLabels)
    testLabels = to_categorical(testLabels)

    print(wstrain.shape)
    print(wstest.shape)

    wstrain = wstrain.astype('float32')
    wstest = wstest.astype('float32')

    wstrain /= 255
    wstest /= 255

    input_shape1 = wstrain.shape[0]
    input_shape2 = wstrain.shape[1]

    lr = 0.008
    if opt == 'Adam':
        opt = optimizers.Adam(learning_rate=lr)
    elif opt == 'Nadam':
        opt = optimizers.Nadam(learning_rate=lr)
    elif opt == 'RMS':
        opt = optimizers.RMSprop(learning_rate=lr)
    elif opt == 'SGD':
        opt = optimizers.SGD(learning_rate=lr)
    else:
        opt = optimizers.Adamax(learning_rate=lr)

    bucle = [5,10,20,50,100,200,500,1000,2000]
    precision = []


    for batch in bucle:
        model = Sequential()
        model.add(Dense(10, activation='softmax', input_shape=(input_shape2,)))  # output layer
        model.build(wstrain.shape)
        epochs = 40
        model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
        model.fit(wstrain, trainLabels, batch_size=batch, epochs=40)
        test_loss, test_acc = model.evaluate(wstest, testLabels)
        test_acc = float("{:.4f}".format(test_acc))
        test_acc *= 100

        print("Test accuracy: ", test_acc)
        precision.append(test_acc)
    return precision
