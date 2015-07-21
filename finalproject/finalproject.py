# Insert code here
__author__ = 'godfreyhobbs'

import csv
import numpy as np
import sys
import os
# from scipy import linspace, polyval, polyfit, sqrt, stats, randn


MIN_Y = 105
MAX_Y = 974
MIN_X = 240
MAX_X = 1696

FPS = 30
NUM_SECONDS = 2

#predict randomly
def predict(data_matrix):
    num_prediction_steps = NUM_SECONDS * FPS
    result = np.random.random((num_prediction_steps,2))* (MAX_X - MIN_X,MAX_Y - MIN_Y) + (MIN_X,MIN_Y)
    return result



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
# first_two_hundred = read_input_files('Inputs/training_data.txt', True)[:200]
# print_data_matrix(first_two_hundred)
# print_data_matrix (unwind(first_two_hundred, True))


def main(argv):
    if len(argv) < 2:
        sys.stderr.write("Usage: %s <inputFileName.txt>" % (argv[0],))
        return 1

    # input_file_name = "inputs/%s" % argv[1]
    input_file_name = "%s" % argv[1]
    if not os.path.exists(input_file_name):
        sys.stderr.write("ERROR: Inputfile %r was not found!" % (input_file_name,))
        return 1

    data_matrix = read_input_files(input_file_name)
    # print_data_matrix(predict(data_matrix))
    prediction_matrix = predict(data_matrix)
    np.savetxt('prediction.txt', prediction_matrix, delimiter=',',fmt='%i')

#     run the finalproject

if __name__ == "__main__":
    sys.exit(main(sys.argv))