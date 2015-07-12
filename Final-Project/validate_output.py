author = 'ppatel'

import re
from math import *
import numpy as np
import csv

def test(in_data):
    allX = []
    allY = []
    for i in range(len(in_data)):
        # print in_data[i][0]
        allX.append(in_data[i][0])
        allY.append(in_data[i][1])
    Ncount = len(in_data)
    Xcount = len(allX)
    Ycount = len(allY)
    badX = sum(n < 240 or n > 1696 for n in allX)
    badY = sum(n < 105 or n > 974 for n in allY)

    if Ncount == 60 and Xcount == 60 and Ycount == 60 and badX == 0 and badY == 0:
        print "Success: no negative and sixty eneries"
    else:
        print "FAIL: something went wrong"
        print "Number of data points: ", Ncount
        print "Number of data points: ", Ncount
        print "Number of X points: ", Xcount
        print "Number of Y points: ", Ycount
        print "Number of out of range X points: ", badX
        print "Number of out of range Y points: ", badY

    return Ncount, Xcount, Ycount, badX, badY

input_file = 'Inputs/training_data.txt'

input_array =  np.genfromtxt(input_file, delimiter=',', dtype=int)

test(input_array[0:60])
test(input_array)

