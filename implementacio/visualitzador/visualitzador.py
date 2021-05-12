#!../../python3.9/bin/python

import numpy as np
import matplotlib.pyplot as plt

def visualizer(automat, i, I, R, C):

    plt.figure
    plt.imshow(automat, cmap='Greys', interpolation='nearest')
    plt.title('Automata cellular elemental del 5 bit')
    # plt.show()
    plt.savefig('fivebitproblem/automats_fivebit/automata%d_I%d_R%d_C%d.png' % (i, I, R, C))
