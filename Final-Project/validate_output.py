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

    return Ncount, Xcount, Ycount, negX, negY

input_file = 'Inputs/training_data.txt'

input_array =  np.genfromtxt(input_file, delimiter=',')

Ncount, Xcount, Ycount, negX, negY = test(input_array)
print "Number of data points: ", Ncount

print "Number of X points: ", Xcount

print "Number of Y points: ", Ycount
print "Number of neg X points: ", negX

print "Number of neg Y points: ", negY

