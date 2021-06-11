#!../../python3.9/bin/python

import numpy as np
import random

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
        self.r = self._get_rule(110)
        self.input  = inp
        self.output = out
        self.encoder = []
        self.cellular_automat = []
        self.reservoir = []

    def _get_rule(self,idx):
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

    def generate_automata(self, input_encoded):
        size_input = len(input_encoded)
        rows = np.ndarray((self.I, size_input), dtype=int)
        for i in range(self.I):
            input_encoded = self.iterate(input_encoded)
            rows[i] = input_encoded
        return rows

    def iterate(self, board):
        """Return the new row of the cellular automata after applying the rule"""

        new_board = np.zeros_like(board)
        for i in range(0, board.shape[0]):
            """
            Per cada iteracio agafa 3 bits i mira a la regla quin valor li correspon
            Per la posició 0 es conecta l'últim bit amb el 1r i 2n
            Per la posició final s'agafa el penúltim i últim bit i el 1r
            """
            if i == 0:
                new_board[i] = self.r[(board[board.shape[0]-1], board[i], board[i+1])]
            elif i == board.shape[0]-1:
                new_board[i] = self.r[(board[i-1], board[i], board[0])]
            else:
                new_board[i] = self.r[tuple(board[i-1:i+2])]
        return new_board

    def encode_next_imput(self, mapping_input, last_eca):
        """
        Tant el yilmaz com altrs pdf's indiquen que a partir del 2n input
        s'utilitza la informació de l'ultim automat cel·lular i despres de
        codificar-lo i mapejar-lo, bit a bit, es decideix el valor a partir
        de la configuració següent
            · 1 si la suma dels 2 bits és 2
            · 0 si la suma dels 2 bits és 0
            · 0 o 1 de manera aleatoria si la suma dels 2 bits és 1
        """

        for i in range(len(mapping_input)):
            n1 = mapping_input[i]
            n2 = last_eca[i]
            if n1+n2 == 2:
                mapping_input[i] = 1
            elif n1+n2 == 0:
                mapping_input[i] = 0
            else:
                mapping_input[i] = random.randint(0,1)
        return mapping_input

    def encode_input(self, input, first_inp, last_eca):
        """
        Codifiquem l'input afegint 0's per tenir un
        array de mida C*size i el randomitzem R vegades
        """

        size = len(input)
        mapping_input = np.ndarray((self.R, size), dtype=int)
        for i in range(self.R):
            # new_size = size*self.C
            # offs = np.zeros(new_size-size, dtype=int)
            # nwp = np.concatenate((input, offs))
            aux_input = input
            random.shuffle(aux_input)
            mapping_input[i] = aux_input
        mapping_input = mapping_input.flatten()

        if not first_inp:
            mapping_input = self.encode_next_imput(mapping_input, last_eca)
        return mapping_input


    def training_5bit(self):
        """ Funció per dur a terme l'entrenament del 5 bit """
        from sklearn.linear_model import LinearRegression

        classifier = LinearRegression()
        classifier.fit(self.reservoir, self.output)
        output_predicted = classifier.predict(self.reservoir)
        # print(x.shape)
        for i in range(len(output_predicted)):
            for j in range(len(output_predicted[0])):

                if output_predicted[i][j] >= 0.5:
                    output_predicted[i][j] = 1
                else:
                    output_predicted[i][j] = 0

        return output_predicted

    def generatingProblem(self):
        size, jsize = len(self.input), len(self.input[0])

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
            encoder: array per emmagatzemar cada encoder, no es necessari realment
            aux_reservoir: array auxiliar amb totes les iteracions I de la regla 110
            reservoir: array per emmagatzemar cada iteració de l'automat
            eca_i: array amb l'últim autòmat
            first_inp: ens indica si es el 1r input o no
            """
            input_encoded     = self.encode_input(self.input[i], first_inp, eca_i)
            automat_reservoir = self.generate_automata(input_encoded)
            self.cellular_automat.append(automat_reservoir)
            eca_i = automat_reservoir[-1]
            self.reservoir.append(automat_reservoir.flatten())
            self.encoder.append(input_encoded)
            first_inp = False

        self.reservoir = np.array(self.reservoir)

        """
        Per a que el classificador funcioni ha d'haver-hi el mateix nº de
        samples a la funció fit. Per dur a terme això cada 'Time step' serà
        un vector concatenat de A_0 a A_I
        """

        output_predicted = self.training_5bit()

        # print(x)
        return output_predicted, self.cellular_automat
