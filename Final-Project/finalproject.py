# Insert code here
__author__ = 'godfreyhobbs'

import csv
import numpy as np


def read_input_files(filename, add_time_step=False):
    result = np.genfromtxt(filename, delimiter=',', dtype=int)
    if add_time_step:
        counter = 0
        new_result = []
        for row in result:
            new_result.append([counter, row[0], row[1]])
            counter += 1
        return new_result
    return result


def print_data_matrix(data_matrix):
    print('\n'.join([','.join(['{0}'.format(item) for item in row]) for row in data_matrix]))


def unwind(data_array, add_time_step=False):
    # always increasing is not really correct but is a good start
    # TODO: refine with collision detection
    result = []
    data_array_values = np.array(data_array)

    current_max_x = 0
    prev_x = 0
    current_max_y = 0
    prev_y = 0
    counter = 0
    for curr_xy in data_array_values:
        current_max_x += abs(curr_xy[0] - prev_x)
        current_max_y += abs(curr_xy[1] - prev_y)
        if add_time_step:
            result.append((counter, current_max_x, current_max_y))
            counter += 1
        else:
            result.append((current_max_x, current_max_y))
        prev_x = curr_xy[0]
        prev_y = curr_xy[1]

    return result

# print read_input_files('/Users/godfreyhobbs/PycharmProjects/CS8803/Final-Project/Inputs/training_data.txt',True)[:200]
first_two_hundred = read_input_files(
    '/Users/godfreyhobbs/PycharmProjects/CS8803/Final-Project/Inputs/training_data.txt', True)[:20]
print_data_matrix(first_two_hundred)
# print_data_matrix (unwind(first_two_hundred, True))
