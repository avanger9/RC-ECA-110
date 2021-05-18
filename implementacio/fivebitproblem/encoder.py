#!../../python3.9/bin/python

import numpy as np
import random

class Encoder():
    def __init__(self, R, C, input):
        self.R = R
        self.C = C
        self.input = input
        self.rnd_input = []

    def encode_input(self, first_inp, last_eca):
        """
        Codifiquem l'input afegint 0's per tenir un
        array de mida C*size i el randomitzem R vegades
        """

        aux_input = []
        size = len(self.input)
        for _ in range(self.R):
            new_size = size*self.C
            offs = np.zeros(new_size-size, dtype=int)
            nwp = np.concatenate((self.input, offs))
            random.shuffle(nwp)
            aux = nwp
            aux_input.append(aux)

        for i in range(self.R):
            self.rnd_input = np.concatenate((self.rnd_input, aux_input[i]))

        """
        Tant el yilmaz com altrs pdf's indiquen que a partir del 2n input
        s'utilitza la informació de l'ultim automat cel·lular i despres de
        codificar-lo i mapejar-lo, bit a bit, es decideix el valor a partir
        de la configuració següent
            · 1 si la suma dels 2 bits és 2
            · 0 si la suma dels 2 bits és 0
            · 0 o 1 de manera aleatoria si la suma dels 2 bits és 1
        """
        if not first_inp:
            for i in range(len(self.rnd_input)):
                n1 = self.rnd_input[i]
                n2 = last_eca[i]
                if n1+n2 == 2:
                    self.rnd_input[i] = 1
                elif n1+n2 == 0:
                    self.rnd_input[i] = 0
                else:
                    self.rnd_input[i] = random.randint(0,1)

        self.rnd_input = np.array(self.rnd_input, dtype=int)

        return self.rnd_input


if __name__ == "__main__":

    # testeig del Encode
    enc = Encoder(2,2,np.array([1,0,0,0]))
    enc.encode_input()
