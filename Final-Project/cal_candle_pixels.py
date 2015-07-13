author = 'godfreyhobbs'

import re
from math import *
import numpy as np
import csv

MIN_Y = 105
MAX_Y = 974
MIN_X = 240
MAX_X = 1696

CANDLE_EXTENT_MIN_X = 895 - MIN_X
CANDLE_EXTENT_MAX_X = 1122 - MIN_X
CANDLE_EXTENT_MIN_Y = 420 - MIN_Y
CANDLE_EXTENT_MAX_Y = 656


def cal_candle_pixels(data_array):
    num_y = MAX_Y - MIN_Y
    num_x = MAX_X - MIN_X
    arena = np.zeros((num_y, num_x), dtype=bool)
    # Turn on the in zone region
    for curr_x in range(CANDLE_EXTENT_MIN_X, CANDLE_EXTENT_MAX_X+1):
            for curr_y in range(CANDLE_EXTENT_MIN_Y, CANDLE_EXTENT_MAX_Y+1):
                 arena[curr_y][curr_x] = True

    for row in data_array:
        x = row[0] - MIN_X
        y = row[1] - MIN_Y
        # clear a 7 by 7 matrix
        # do not worry about negatives as we only really care aobut the center
        for curr_x in range(x, x + 28):
            for curr_y in range(y, y + 14):
                if CANDLE_EXTENT_MIN_Y <= curr_y <= CANDLE_EXTENT_MAX_Y and CANDLE_EXTENT_MIN_X <= curr_x <= CANDLE_EXTENT_MAX_X:
                    arena[curr_y][curr_x] = False

    # return arena[200:MAX_Y - 200, 200:MAX_X - 200]
    arena = np.transpose(np.nonzero(arena[200:-200, 200:-200])) + [MIN_Y + 200, MIN_X + 200]
    swap_cols(arena, 0, 1)
    return arena


def swap_cols(arr, frm, to):
    arr[:, [frm, to]] = arr[:, [to, frm]]


def print_data_matrix(data_matrix):
    print('\n'.join([','.join(['{0}'.format(item) for item in row]) for row in data_matrix]))
    # candle_pixels = [
    #     [(rowIndex, col_index) for col_index in range(len(data_matrix[0])) if data_matrix[rowIndex][col_index]] for
    #     rowIndex in range(len(data_matrix))]
    # print np.transpose(candle_pixels)


input_file = 'Inputs/training_data.txt'

input_array = np.genfromtxt(input_file, delimiter=',', dtype=int)

pixels = cal_candle_pixels(input_array)

print(pixels.shape)
print(np.count_nonzero(pixels))
# print_data_matrix(np.transpose(np.nonzero(pixels)) + [MIN_Y, MIN_X])
# print_data_matrix(np.transpose(np.nonzero(pixels[200:-200,200:-200])) + [MIN_Y+200, MIN_X+200])
print_data_matrix(pixels)
# print_data_matrix(pixels)
