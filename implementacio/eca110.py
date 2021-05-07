#!../python3.9/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt

# rule 110 - 0110 1110
# time I - número d'iteracions de la regla
# start_pattern - patro inicial, es pot començar amb un unic 1 central o aleatori

class elementaryCellularAutomata():
    def __init__(self, iterations, input):
        self.r = self._get_rule(110)
        self.I = iterations
        self.input = input

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

    def generate_automata(self):
        board = np.array(self.input)
        rows = []
        for _ in range(self.I):
            board = self.iterate(board)
            rows.append(board)

        rows = np.array(rows)
        return rows

    def iterate(self, board):
        """Return the new row of the cellular automata after applying the rule"""

        new_board = np.zeros_like(board)
        for i in range(0, board.shape[0]):
            """
            Per cada iteracio agafa 3 bits i mira a la regla quin valor li correspon
            Per la posició 0 i la posició final no es miren perquè no pots mirar el primer i últim bit
            """
            if i == 0:
                new_board[i] = self.r[(board[board.shape[0]-1], board[i], board[i+1])]
            elif i == board.shape[0]-1:
                new_board[i] = self.r[(board[i-1], board[i], board[0])]
            else:
                new_board[i] = self.r[tuple(board[i-1:i+2])]
        return new_board

        def visualize_board(self, board, title):
            """Visualize the elementary cellular automata"""
            plt.figure()
            plt.imshow(board, cmap="Greys")
            plt.axis("off")
            plt.title(title, fontsize=14)
            plt.show()
            plt.close()


class elementaryCellularAutomataMnist():
    """
    Class eca per testejar diferentes funcionalitats, no
    s'utilitza per les funcions principals
    """

    def __init__(self, iterations, start_pattern):
        self.r = self._get_rule(110)
        self.I = iterations
        self.input = start_pattern

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

    def generate_automata(self):
        board = np.array(self.input)
        rows = []
        for _ in range(self.I):
            board = self.iterate(board)
            rows.append(board)

        rows = np.array(rows)
        return rows

    def iterate(self, board):
        """Return the new row of the cellular automata after applying the rule"""
        new_board = np.zeros_like(board)
        for i in range(1, board.shape[0] - 1):
            """
            Per cada iteracio agafa 3 bits i mira a la regla quin valor li correspon
            Per la posició 0 i la posició final no es miren perquè no pots mirar el primer i últim bit
            """
            new_board[i] = self.r[tuple(board[i-1:i+2])]
        return new_board

class elementaryCellularAutomataTest():
    """
    Class eca per testejar diferentes funcionalitats, no
    s'utilitza per les funcions principals
    """

    def __init__(self, iterations, start_pattern):
        self.r = self._get_rule(110)
        self.i = iterations
        self.p = start_pattern

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

    def generate_map(self):
        """Return the rows of the cellular automata"""
        board = np.array(self.p)
        board = np.pad(board, (self.i, self.i), 'constant', constant_values=(0,0))
        rows = [board]
        """
        Cada iteracio apliquem la regla de l'automata al patro i treien una nova
        fila de 0 i 1. Es segueix aplicant segons les iteracions que decidim
        """
        for _ in range(self.i):
            board = self.iterate(board)
            rows.append(board)

        rows = np.array(rows)
        return rows

    def iterate(self, board):
        """Return the new row of the cellular automata after applying the rule"""
        board = np.pad(board, (1, 1), 'constant', constant_values=(0,0))
        print(board, board.shape[0])
        new_board = np.zeros_like(board)
        for i in range(1, board.shape[0] - 1):
            """
            Per cada iteracio agafa 3 bits i mira a la regla quin valor li correspon
            Per la posició 0 i la posició final no es miren perquè no pots mirar el primer i últim bit
            """
            new_board[i] = self.r[tuple(board[i-1:i+2])]
        return new_board[1:-1]

    def visualize_board(self, board, title):
        """Visualize the elementary cellular automata"""
        plt.figure()
        plt.imshow(board, cmap="Greys")
        plt.axis("off")
        plt.title(title, fontsize=14)
        plt.show()
        plt.close()

if __name__ == "__main__":


    #start_pattern = list('000000000010000000000'
    # reservoir = elementaryCellularAutomataTest(i, start_pattern)
    # board = reservoir.generate_map()
    # reservoir.visualize_board(board, '110')

    # Per testejar l'eca110
    a = np.array((0,1,0))
    i = 15
    reservoir = elementaryCellularAutomataTest(i, a)
    board = reservoir.generate_map()
    reservoir.visualize_board(board, '110')
