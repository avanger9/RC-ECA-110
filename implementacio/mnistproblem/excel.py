import numpy as np
# from openpyxl import Workbook
import xlwt
from training import training

#
# ws = []

trainLabels = np.load('arrays/train_labels_array.npy')
testLabels = np.load('arrays/test_labels_array.npy')
# wstest = np.load('train_ws_array_I0/ws_test_arrayfile.npy')
# wstrain = np.load('train_ws_array_I0/ws_train_arrayfile.npy')

bucle = [0, 10, 13, 16]
for l in bucle:
    for i in range(6):
        aux = np.load('train_ws_array_I%d/ws_train_arrayfile%d.npy' % (l, i+1))
        for k in range(10000):
            t = aux[k]
            ws.append(t)
    wstrain = np.array(ws)
    wstest = np.load('train_ws_array_I%d/ws_test_arrayfile.npy' % (l))

    book = xlwt.Workbook()
    sheet = book.add_sheet('I%d' % i)

    cols = ['C','D','E','F','G','H','I','J','K']
    batch = [5,10,20,50,100,200,500,1000,2000]

    row_start = 3

    optimizers = ['Adam', 'Nadam', 'RMS', 'SGD', 'Adamax']

    for i in range(len(optimizers)):
        opt = optimizers[i]
        row = sheet.row(row_start)
        row.write(1, opt)
        for index, col in enumerate(cols):
            value = batch[index]
            row.write(index+2, value)
        for rows in range(10):
            new_rows = row_start+rows+1
            row = sheet.row(new_rows)
            precision = training(opt, wstrain, wstest, trainLabels, testLabels)
            for index in range(len(precision)):
                value = precision[index]
                row.write(index+2, value)
            book.save('results.xls')
        row_start += 13

    book.save('results.xls')
