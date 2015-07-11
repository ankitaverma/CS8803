author = 'ppatel'

import re
from math import *
import numpy as np
import csv

def test(in_data):
    allX = []
    allY = []
    for i in range(len(in_data)):
        allX.append(in_data[i][0])
        allY.append(in_data[i][1])
    Ncount = len(in_data)
    Xcount = len(allX)
    Ycount = len(allY)
    negX = sum(n < 0 for n in allX)
    negY = sum(n < 0 for n in allY)

    if Ncount == 60 and Xcount == 60 and Ycount == 60 and negX == 0 and negY == 0:
        print "Sucess: no negative and sixty eneries"
    else:
        print "FAIL: something went wrong"
        print "Number of data points: ", Ncount
        print "Number of data points: ", Ncount
        print "Number of X points: ", Xcount
        print "Number of Y points: ", Ycount
        print "Number of neg X points: ", negX
        print "Number of neg Y points: ", negY

    return Ncount, Xcount, Ycount, negX, negY

input_file = 'Inputs/training_data.txt'

input_array =  np.genfromtxt(input_file, delimiter=',', dtype=int)

test(input_array[:60])
test(input_array)

