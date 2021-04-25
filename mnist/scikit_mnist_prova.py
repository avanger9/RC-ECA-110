#!../python3.9/bin/python

import matplotlib as mpl
import matplotlib.pyplot as plt

import numpy as np # linear algebra

def displayData(X,Y):
    # set up array
    fig, ax = plt.subplots(nrows=10, ncols=10, figsize=(15,15))
    fig.suptitle( "Display randomly images of the training data set")
    # loop over randomly drawn numbers
    for i in range(10):
        for j in range(10):
            ind = np.random.randint(X.shape[0])
            tmp = X[ind,:].reshape(28,28)
            ax[i,j].set_title("Label: {}".format(Y[ind]))
            ax[i,j].imshow(tmp, cmap='gray_r') # display it as gray colors.
            plt.setp(ax[i,j].get_xticklabels(), visible=False)
            plt.setp(ax[i,j].get_yticklabels(), visible=False)

    fig.subplots_adjust(hspace=0.5, wspace=0.5)

from sklearn.model_selection import train_test_split
x_train,x_dev, y_train,  y_dev = train_test_split(x,y,random_state=42)

displayData(x_train,y_train)
