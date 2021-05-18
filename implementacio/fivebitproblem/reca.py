#!../../python3.9/bin/python

import numpy as np

from sklearn import linear_model

from generadorFiveBitProblem import fivebit
from encoder import Encoder
from eca110 import elementaryCellularAutomata as eca
# from visualitzador.visualitzador import visualizer


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
        l'últim autòmata ho fem tot en un mateix gran bucle
        """

        first_inp = True
        eca_i = None
        for i in range(size):
            """
            args:
            -----
            input_encoded: array auxiliar amb l'input codificat pels parametres R, C i l'automat anterior
            encoder: array per emmagatzemar cada encoder
            aux_reservoi: array auxiliar amb totes les iteracions I de la regla 110
            reservoir: array er emmagatzemar cada iteració de l'automat
            eca_i: array amb l'últim autòmat
            """
            input_encoded = Encoder(self.R, self.C, self.input[i]).encode_input(first_inp, eca_i)
            self.encoder.append(input_encoded)
            aux_reservoir = eca(self.I, input_encoded).generate_automata()
            for k in range(self.I):
                self.reservoir.append(aux_reservoir[k])
            eca_i = self.reservoir[-1]
            first_inp = False
        reservoir_size = len(self.input)

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
        return x, self.reservoir


def visualizer_5bit(automat, i, I, R, C):

    plt.figure
    plt.imshow(automat, cmap='Greys', interpolation='nearest')
    plt.title('Automata cellular elemental del 5 bit')
    # plt.show()
    plt.savefig('automats_fivebit/automata%d_I%d_R%d_C%d.png' % (i, I, R, C))

def start(I, R, C,bucle, distractor):

    fbp = fivebit(distractor)
    input, output = fbp.generateProblem()

    iterations = I     # -I
    random_map = R     # -R
    size_of_v  = C     # -C

    """ No tenen utilitat per ara, però en algun codi els he vist i estan per si de cas"""
    diffuse, pad = 0, 0

    r = 0
    pred = np.zeros(32, dtype=int)
    fail = np.zeros(32, dtype=int)
    f = open('dades_fivebit/fivebit_I%d_R%d_C%d_bucle%d_distractor%d'
                        % (I, R, C, bucle, distractor), 'w+')
    while r < bucle:

        print('bucle:', r)
        r += 1
        for i in range(32):
            pc = ProblemClassification(iterations, random_map, size_of_v,
                                            input[i], output[i])
            predictor, automata = pc.generatingProblem()

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


    # visualitzar l'automat

    # for i in range(32):
    #     pc = ProblemClassification(iterations, random_map, size_of_v,
    #                                          input[i], output[i])
    #     x, automata = pc.generatingProblem()
    #     visualizer_5bit(automata, i, I, R, C)
