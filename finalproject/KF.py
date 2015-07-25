import re
from math import *
import numpy as np



def get_input(filename):
    p = re.compile('[-0-9]+')  
    ia = []
    f = open(filename, 'r')
    for line in f:
        x,y = p.findall(line)
        ia.append([int(x),int(y)])
    f.close()
    return ia


def dat(in_data):
    in_data = in_data[0:60:1]
    allX = []
    allY = []
    for i in range(len(in_data)):
            allX.append(in_data[i][0])
            allY.append(in_data[i][1])
    return allX, allY


def KF(input_array):
    Ncount = len(input_array)
    Nmean  = np.mean(input_array)
    Nstd   = np.std(input_array)
    
    z = input_array
    n_iter = Ncount
    x = Nmean
    R = Nstd**2 # estimate of measurement variance, change to see effect
    
    sz = (n_iter,)
    
    # allocate space for arrays
    xhat=np.zeros(sz)      # a posteri estimate of x
    P=np.zeros(sz)         # a posteri error estimate
    xhatminus=np.zeros(sz) # a priori estimate of x
    Pminus=np.zeros(sz)    # a priori error estimate
    K=np.zeros(sz)         # gain or blending factor
    
    
    Q = 1e-5 # process variance
    
    # intial guesses
    xhat[0] = input_array[0]
    P[0] = input_array[1]
    
    
    for k in range(1,n_iter):
        # time update
        xhatminus[k] = xhat[k-1]
        Pminus[k] = P[k-1]+Q
    
        # measurement update
        K[k] = Pminus[k]/( Pminus[k]+R )
        xhat[k] = xhatminus[k]+K[k]*(z[k]-xhatminus[k])
        P[k] = (1-K[k])*Pminus[k]
    return xhat


input_file = 'test01.txt'
input_array = get_input(input_file)

allX, allY = dat(input_array)

xhat = KF(allX)

print allX
print xhat
