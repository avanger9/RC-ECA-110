#!../python3.9/bin/python

import numpy as np

from sklearn import linear_model

from mnistproblem.mnistGenerator import generateMnistInput
from fivebitproblem.fiveBitProblem import fivebit
from encoder.encoder import Encoder
from eca110 import elementaryCellularAutomata as eca


class ProblemClassification():
    def __init__(self, iterations, random_mapping, size_of_v, inp, out):
        """
        Parameters
        ----------
        iterations: int
            number of iterations that cellular automata will do
        random_mapping: int
            number of random mapping that will encode each input
        size_of_v: int
            number to multiplicate with with size of input for the final size
        inp: array 2D
            input
        out: array 2D
            output
        """
        self.I = iterations
        self.R = random_mapping
        self.C = size_of_v
        self.input  = inp
        self.output = out
        self.encoder = []
        self.reservoir = []

    def generatingProblem(self):
        size, jsize = len(self.input), len(self.input[0])

        # Codifiquem l'entrada
        # for i in range(size):
        #     for j in range(jsize):
        #         enc = Encoder(self.R, self.C, self.input[i][j]).encode_input()
        #         self.encoder.append(enc)

        # for i in range(size):
        #     enc = Encoder(self.R, self.C, self.input[i]).encode_input()
        #     self.encoder.append(enc)
        #
        # reservoir_size = len(self.encoder)
        # # print(reservoir_size)    # mida del reservori
        #
        # """Per cada input se li passa l'automata cellular"""
        # for i in range(reservoir_size):
        #     aux_reservoir = eca(self.I, self.encoder[i]).generate_automata()
        #     for j in range(self.I):
        #         self.reservoir.append(aux_reservoir[j])
        # # print(len(self.reservoir))
        # # print(self.reservoir[0])
        # self.reservoir = np.array(self.reservoir)

        """
        Per cada input el codifiquem i ja l'enviem al reservori per a que l'autòmata
        iteri i tinguem l'A_n. Com per mapejar l'input en cal la informació de
        l'últim autòmata ho  fem tot en un mateix gran bucle
        """

        first_inp = True
        eca_i = []
        for i in range(size):
            if first_inp:
                enc = Encoder(self.R, self.C, self.input[i]).encode_input(first_inp, eca_i)
                self.encoder.append(enc)
                aux_reservoir = eca(self.I, enc).generate_automata()
                for k in range(self.I):
                    self.reservoir.append(aux_reservoir[k])
                eca_i = self.reservoir[-1]
                first_inp = False
            else:
                enc = Encoder(self.R, self.C, self.input[i]).encode_input(first_inp, eca_i)
                self.encoder.append(enc)
                aux_reservoir = eca(self.I, enc).generate_automata()
                for k in range(self.I):
                    self.reservoir.append(aux_reservoir[k])
                eca_i = self.reservoir[-1]
        reservoir_size = len(self.encoder)

        """
        Per a que el classificador funcioni ha d'haver-hi el mateix nº de
        samples a la funció fit. Per dur a terme això cada 'Time step' serà
        un vector concatenat de A_0 a A_I
        """

        a_i = []
        for i in range(reservoir_size):
            aux = []
            for j in range(self.I):
                aux.append(self.reservoir[i][j])
            a_i.append(aux)

        # print(len(aux_i))

        classifier = linear_model.LinearRegression()
        classifier.fit(a_i, self.output)
        x = classifier.predict(a_i)
        # print(x.shape)
        for i in range(len(x)):
            for j in range(len(x[0])):

                if x[i][j] >= 0.5:
                    x[i][j] = 1
                else:
                    x[i][j] = 0

        x = np.array(x, dtype=int)

        # print(x)
        return x

def start(I,R,C,bucle, distractor):



    fbp = fivebit(distractor)
    input, output = fbp.generateProblem()



    iterations = I     # -I
    random_map = R     # -R
    size_of_v  = C     # -C

    """ No tenen utilitat per ara, però en algun codi els he vist i estan per si de cas"""
    diffuse, pad = 0, 0


    r, pred, fail = 0, 0, 0
    while r < bucle:
        print('bucle:', r)
        r += 1
        pc = ProblemClassification(iterations, random_map, size_of_v, input[0], output[0])
        x = pc.generatingProblem()

        succ = True
        for a,b in zip(x,output[0]):
            # print('array a:', a, 'array b:', b)
            if not np.array_equal(a, b):
                fail += 1
                succ = False
                break
        if succ:
            pred += 1
    print('nombre dencerts:', pred, 'nombre de fallos:', fail)
