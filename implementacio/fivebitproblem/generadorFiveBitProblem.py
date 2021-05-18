#!../../python3.9/bin/python

import numpy as np

class fivebit():
    def __init__(self, distractor):
        """
        :param distractor: valor del distractor
        """
        self.distractor = distractor
        self.ninputs = 32
        self.inputs = []
        self.outputs = []
        self.bits = 5

    def generateProblem(self):
        b     = self.bits
        distr = self.distractor
        for i in range(self.ninputs):
            """ 32 iteracions per donar cada parell d'inputs del pas 1 al pas 5 """
            input = []
            output = []
            y1, y2, y3 = 0, 0, 1
            for j in range(2*b + distr):
                if j < b:
                    bit = (i&2**j)/2**j
                    a1 = 1-bit
                    a2 = bit
                else:
                    a1, a2 = 0, 0

                if j >= b and j != b+distr-1:
                    a3 = 1
                else:
                    a3 = 0

                if j == b+distr-1:
                    a4 = 1
                else:
                    a4 = 0
                input.append(np.asarray([a1,a2,a3,a4]))

                if j >= b+distr:
                    y1 = input[j - (b+distr)][0]
                    y2 = input[j - (b+distr)][1]
                    y3 = 0
                output.append(np.asarray([y1,y2,y3]))

            self.inputs.append(input)
            self.outputs.append(output)
        return np.array(self.inputs, dtype='int'), np.array(self.outputs, dtype='int')

if __name__ == "__main__":

    "Per testejar el 5 bit"
    fbp = fivebit(10)
    inp, out = fbp.generateProblem()
    # print(inp, out)
