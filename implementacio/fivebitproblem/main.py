#!../../python3.9/bin/python

import sys
import argparse
import time
import numpy as np
import matplotlib.pyplot as plt

from generadorFiveBitProblem import fivebit
from reca import ProblemClassification

def visualizer_5bit(automat, i, I, R, C):

    plt.figure
    plt.imshow(automat, cmap='Greys', interpolation='nearest')
    plt.title('Automata cellular elemental del 5 bit')
    # plt.show()
    plt.savefig('automats_fivebit/automata%d_I%d_R%d_C%d.png' % (i, I, R, C))

if __name__ == '__main__':

    """
    Arguments
    ----------
    argument -I: required
        number of iterations of elemental cellular automata
    argument -R: required
        number of random mapping
    argument -C: not required
        number to multiply the size of input
    argument -b: NOT required
        number of iterations of whole program
    argument -t: NOT required
        number of distractors of 5-bit

    example:
    ./main.py -I 10 -R 4 -C 4 -b 100 -t 20
    """

    parser = argparse.ArgumentParser(prog = 'main.py')
    parser.add_argument('-I', required=True, type=int)
    parser.add_argument('-R', required=True, type=int)
    parser.add_argument('-C', required=True, type=int)
    parser.add_argument('-b', required=True, type=int)
    parser.add_argument('-t', required=True, type=int)
    args = parser.parse_args()

    I = args.I
    R = args.R
    C = args.C
    bucle = args.b
    distractor = args.t
    print(I,R,C)

    start_time = time.time()

    input, output = fivebit(distractor).generateProblem()

    r = 0
    pred = np.zeros(32, dtype=int)
    fail = np.zeros(32, dtype=int)
    f = open('dades_fivebit/fivebit_I%d_R%d_C%d_bucle%d_distractor%d'
                        % (I, R, C, bucle, distractor), 'w+')
    while r < bucle:

        print('bucle:', r)
        r += 1
        for i in range(32):
            pc = ProblemClassification(I, R, C, input[i], output[i])
            predictor, automata = pc.generatingProblem()

            # visualizer_5bit(automata, i, I, R, C)

            success = True
            for a,b in zip(predictor,output[i]):
                if not np.array_equal(a, b):
                    fail[i] += 1
                    success = False
                    break
            if success:
                pred[i] += 1
    for i in range(32):
        print('nombre dencerts:', pred[i], "nombre d'errors:", fail[i], "per l'input:", i+1)
        f.write("nombre encerts: %d, nombre d'errors: %d per l'input: %d\n" % (pred[i], fail[i], i+1))
    f.close()

    print('--- %s seconds ---', '%.3f' % (time.time() - start_time))
