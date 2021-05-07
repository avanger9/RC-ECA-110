#!../../python3.9/bin/python

import numpy as np
import matplotlib.pyplot as plt
import time
from multiprocessing import Pool

import sys; sys.path.append('../')
from eca110 import elementaryCellularAutomataMnist as eca

class mnist():
    def __init__(self, images, labels, tri, M):
        self.rule = self._get_rule(110)
        self.M = M
        self.images = images
        self.tri = tri
        self.labels = labels
        self.rows = []


        self._vars()
        self.Ws = []

    def _vars(self):
        nimages, x, y, bytes = self.images.shape
        self.num_images = nimages
        self.x = x
        self.y = y
        self.bytes = bytes

    def _get_rule(self,idx):
        """ Retorna la regla del eca amb al valor corresponent al conjunt
            dels 3 bits corresponents """
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


    def createReservoir(self, image, bit):
        """Retorna la matriu corresponent al bit de la imatge seleccionada """
        eachrc = []
        for i in range(self.x):
            eachbit = []
            for j in range(self.y):
                eachbit.append(image[i][j][bit])
            eachrc.append(eachbit)
        return eachrc

    def _iterateAutomata(self, board):
        """Retorna la nova fila després d'aplicar la regla 110 """
        new_board = np.zeros_like(board)
        for i in range(1, board.shape[0]-1):
            """
            Per cada iteracio agafa 3 bits i mira a la regla quin valor li correspon
            Per la posició 0 i la posició final no es miren perquè ho fem amb
            posicions fixades
            """
            new_board[i] = self.rule[tuple(board[i-1:i+2])]
        return new_board

    def evolveReservoir(self, imageb):
        """ La funcio rep el bit d'una imatge de 28x28. Executa un pas de la
            regla 110 per cada fila i per cada columna. Cal fer la transposada
            per la matriu de la columna. Executa bit a bit el bit de la filaij
            pel corresponent bit de la colij i retorna la matriu XOR"""
        automat = []
        automatar, automatac = [], []
        for i in range(self.x):
            automatar.append(self._iterateAutomata(imageb[i,:]))
            automatac.append(self._iterateAutomata(imageb[:,i]))

        automatac = np.array(automatac)
        automatac = np.matrix.transpose(automatac)
        automata = []
        for i in range(self.x):
            aux = []
            for j in range(self.y):
                 r = automatar[i][j]
                 c = automatac[i][j]
                 aux.append(r^c)
            automata.append(aux)

        return automata

    def reintegrateBits(self, aut):
        """ La funció rep una imatge de 28x28x8 bits i la reintegra. Ens Retorna
            la imatge 28x28 bytes
        """
        matBytes = []
        for i in range(self.x):
            aux = []
            for j in range(self.y):
                binary = ''
                for bit in range(self.bytes):
                    """ al posar-ho de nou en binari ho fem pensant en l'ordre
                        u7 u6 u5 u4 u3 u2 u1 u0"""
                    binary += str(aut[7-bit][i][j])
                aux.append(int(binary,2))
            matBytes.append(aux)
        return np.array(matBytes)

    def maxpolling(self,image):
        """ la funció rep una imatge i li fa un max pool per redimensionar-la
            per cada 2x2 bytes escull el maxim. Retorna una imatge de 14x14 bytes
        """
        start, step2, end = 0, 2, self.x
        # print(image)
        bytesMax = []
        for i in range(start, end, step2):
            auxM = []
            for j in range(start, end, step2):
                aux = image[i:i+step2, j:j+step2]
                aux = np.array(aux)
                # print('h', aux)
                max_4bytes = aux.max()
                auxM.append(max_4bytes)
            bytesMax.append(auxM)

        # visualize_board(bytesMax, '14x14')
        return np.array(bytesMax)



    def start(self):
        """ Funció principal per dur a terme tots els passos per extreure les
            les dades d'entrada de cada imatge del mnist
        """
        f = open('errors_en_imatges.txt', 'w+')
        for k in range(self.num_images):
            try:
                rowsb = []
                # visualize_board(self.tri[k], str(self.labels[k]))
                for bit in range(self.bytes):
                    """ recordem en el bit = 0 está el bit de menys mes i al
                        bit = 7 está el bit de més pes """
                    rowsb.append(self.createReservoir(self.images[k], bit))  # 8 matrius de 28x28
                self.rows.append(rowsb); rowsb = np.array(rowsb)
                print('Imatge' ,k, 'contruida correctament amb 8 matrius de 28x28', rowsb.shape)
                """
                En aquest punt ja tenim guardats per cada imatge els bits de mes a
                menys pes en vectors
                """
                # try:
                #     p = Pool(8)     # 8 procesadors
                #     a = p.starmap(evolveReservoir, [(rowsb[bit], x) for bit in range(bytes)])
                # finally:
                #     p.close()
                #     p.join()

                automat = np.ndarray((self.M, 8, 28, 28), dtype=int)
                W       = np.ndarray((self.M, 14*14),     dtype=int)
                for i in range(self.M):
                    automat_aux = []
                    for bit in range(self.bytes):
                        if i:
                            print('entras al pas que utilitzem lanterior automat pel pas:', i, 'amb el bit:', bit)
                            automat_aux.append(self.evolveReservoir(automat[i-1][bit]))
                        else:
                            print('entres al pas inicial utilitzant el vector original i el bit', bit)
                            automat_aux.append(self.evolveReservoir(rowsb[bit]))    # evolucio de l'automat pels 8 bits
                    automat[i] = automat_aux
                    print(automat.shape)

                    """ Ara que ja tenim l'automat, reintegrem a decimal de nou
                        Passant de tenir 8 matrius a 1 matriu de 28*28"""
                    imageR = self.reintegrateBits(automat_aux)
                    # visualize_board(imageR, 'imatge reintegrada')
                    """ Apliquem maxpolling per redimensionar a 14*14 """
                    aux = self.maxpolling(imageR)
                    """ Per cada imatge redimensionada convertim el vector de 2D a 1D"""
                    W[i] = aux.flatten()
                X = np.array(W.flatten())
                self.Ws.append(X)
                print('Matriu Xu de dimensió 196*M', X.shape)
                print('Imatge', k, 'procesada correctament')
            except:
                f.write('Error en la imatge %d\r\n' % k)
        self.Ws = np.array(self.Ws)
        np.save('wsfile', self.Ws)
        f.close()
        """
        Arribats a aquest punt, el processament de l'entrada d'una imatge k
        HA FINALITZAT amb la variable Xu de 196*M components

        El seguent pas
        """



def visualize_board(board, title):
    """ Funcio per visualitzar la imatge"""
    plt.figure()
    plt.imshow(board, cmap="Greys")
    plt.axis("off")
    plt.title(title, fontsize=14)
    plt.show()
    plt.close()

def test(u, tri):
    pass

if __name__ == '__main__':

    start_time = time.time()

    # parser = argparse.ArgumentParser(prog = 'mnistProblem.py')
    # parser.add_argument('-M', required=True, type=int)
    # args = parser.parse_args()
    # M = args.M

    tri = np.load('../../mnist/array/train_images_array.npy')
    lab = np.load('../../mnist/array/train_labels_array.npy')
    for i in range(10):
        print(lab[i])
    u = np.load('train_images_layers_array.npy')

    """
    vector u generat amb les 8 capes
    Per les proves inicials es treballarà amb un vector més petit
    """
    lim = 100
    tri = tri[:lim]
    # visualize_board(tri, 'hola')
    u = u[:lim]

    """
    Per cada imatge treballarem amb els bits del mateix pes per cada fila i
    cada columna iterant sobre un parametre M
    """

    M = 10
    mnist(u, lab, tri, M).start()


    print('--- %s seconds ---', '%.3f' % (time.time() - start_time))
