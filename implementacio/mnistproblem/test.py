#!../../python3.9/bin/python

import numpy as np
import matplotlib.pyplot as plt
import time
from multiprocessing import Pool

import sys; sys.path.append('../')
from eca110 import elementaryCellularAutomataMnist as eca

def get_rule(idx):
    """Return the rule with the name and the result of each combination of 3 bits"""
    input_patterns = [
        (1,1,1),
        (1,1,0),
        (1,0,1),
        (1,0,0),
        (0,1,1),
        (0,1,0),
        (0,0,1),
        (0,0,0)
    ]
    outputs = list(map(int,format(idx, "#010b")[2:]))
    mapping = dict(zip(input_patterns, outputs))
    mapping["name"] = "Rule %d" % (idx)
    return mapping

def iterateAutomata(rule, board):
    """Return the new row of the cellular automata after applying the rule"""
    new_board = np.zeros_like(board)
    # print(new_board.shape)
    for i in range(1, board.shape[0] - 1):
        """
        Per cada iteracio agafa 3 bits i mira a la regla quin valor li correspon
        Per la posició 0 i la posició final no es miren perquè no pots mirar el primer i últim bit
        """
        new_board[i] = rule[tuple(board[i-1:i+2])]
    # print(new_board.shape)
    return new_board

def visualize_board(board, title):
    """Visualize the elementary cellular automata"""
    plt.figure()
    plt.imshow(board, cmap="Greys")
    plt.axis("off")
    plt.title(title, fontsize=14)
    plt.show()
    plt.close()

tri = np.load('../../mnist/array/train_images_array.npy')
lab = np.load('../../mnist/array/train_labels_array.npy')
u = np.load('train_images_layers_array.npy')

t = tri[7]
u = u[7]


visualize_board(t, 'hola')
x, y = t.shape
for i in range(x):
    for j in range(y):
        if t[i][j] > 50:
            t[i][j] = 1
        else:
            t[i][j] = 0


r = get_rule(110)
rc = []
for k in range(10):
    if k != 0:
        t = np.array(rc)
    a, b = [], []
    for i in range(x):
        a.append(iterateAutomata(r, t[i]))
        b.append(iterateAutomata(r, t[:,i]))

    b = np.array(b)
    b = np.matrix.transpose(b)
    visualize_board(a,'a')
    visualize_board(b,'b')

    rc = []
    for i in range(x):
        aux = []
        for j in range(y):
            h,c=a[i][j],b[i][j]
            aux.append(h^c)
        rc.append(aux)
    visualize_board(rc, 'hola')
