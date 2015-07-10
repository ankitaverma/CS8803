#Insert code here
__author__ = 'godfreyhobbs'

import csv


def read_input_files(filename, add_time_step=False):
    counter = 0
    result = []
    with open(filename, 'rb') as csv_file:
        my_reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
        for row in my_reader:
            row_data = [int(x) for x in row[0].strip().split(",")]
            if add_time_step:
                result.append([counter] + row_data)
                counter += 1
            else:
                result.append(row_data)
    return result


def print_data_matrix(data_matrix):
    print('\n'.join([','.join(['{0}'.format(item) for item in row]) for row in data_matrix]))

# print read_input_files('/Users/godfreyhobbs/PycharmProjects/CS8803/Final-Project/Inputs/training_data.txt',True)[:200]
first_two_hundred = read_input_files('/Users/godfreyhobbs/PycharmProjects/CS8803/Final-Project/Inputs/training_data.txt', True)[
        :200]

def unwind(data_array):
    return data_array


print unwind(first_two_hundred)
