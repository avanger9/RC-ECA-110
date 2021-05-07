#!../python3.9/bin/python

import sys
import argparse
import time
from reca import start

if __name__ == '__main__':

    """
    Arguments
    ----------
    argument -I: required
        iterations of elemental cellular automata
    argument -R: required
        number of random mapping
    argument -C: required
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
    parser.add_argument('-b', type=int)
    parser.add_argument('-t', type=int)
    args = parser.parse_args()

    I = args.I
    R = args.R
    C = args.C

    if args.b == None:
        b = 100
    else:
        b = args.b

    if args.t == None:
        t = 20
    else:
        t = args.t
    print(I,R,C)

    start_time = time.time()
    start(I, R, C, b, t)

    print('--- %s seconds ---', '%.3f' % (time.time() - start_time))
