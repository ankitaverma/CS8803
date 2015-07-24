# Insert code here
__author__ = 'godfreyhobbs'

import csv
from math import *
import numpy as np
import sys
import os
import random
# from scipy import linspace, polyval, polyfit, sqrt, stats, randn


MIN_Y = 105
MAX_Y = 974
MIN_X = 240
MAX_X = 1696

FPS = 30
NUM_SECONDS = 2

COUNT_TRAINING_DATA = 36319
DELTA_X_TRAINING_DATA = float(448830 - 780)
DELTA_Y_TRAINING_DATA = float(400782 - 186)
DELTA_X = DELTA_X_TRAINING_DATA / COUNT_TRAINING_DATA
DELTA_Y = DELTA_Y_TRAINING_DATA / COUNT_TRAINING_DATA

center = (1008.5, 542.5)
collision_buffer = 60
radius = (227 / 2)

COLLISION_ZONE_X_MIN = 330
COLLISION_ZONE_X_MAX = 1600
COLLISION_ZONE_Y_MIN = 200
COLLISION_ZONE_Y_MAX = 880


def trunc_xy(curr_xy):
    curr_xy[0] = min(curr_xy[0], MAX_X)
    curr_xy[1] = min(curr_xy[1], MAX_Y)
    return curr_xy


def angle_trunc(a):
    """This maps all angles to a domain of [-pi, pi]"""
    while a < 0.0:
        a += pi * 2
    return ((a + pi) % (pi * 2)) - pi


def get_heading(hunter_position, target_position):
    """Returns the angle, in radians, between the target and hunter positions"""
    hunter_x, hunter_y = hunter_position
    target_x, target_y = target_position
    heading = atan2(target_y - hunter_y, target_x - hunter_x)
    heading = angle_trunc(heading)
    return heading


def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def get_angle(p0, p1=np.array([0, 0]), p2=None):
    ''' compute angle (in degrees) for p0p1p2 corner
    Inputs:
        p0,p1,p2 - points in the form of [x,y]
    '''
    if p2 is None:
        p2 = p1 + np.array([1, 0])
    v0 = np.array(p0) - np.array(p1)
    v1 = np.array(p2) - np.array(p1)

    angle = np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))
    angle = angle_trunc(angle)
    return np.degrees(angle)


def in_zone(data_point):
    if COLLISION_ZONE_X_MIN < data_point[0] < COLLISION_ZONE_X_MAX:
        if COLLISION_ZONE_Y_MIN < data_point[1] < COLLISION_ZONE_Y_MAX:
            return False
    return True


def in_circle(data_point):
    # diameter is 227
    # radius is 227/2
    return distance_between(center, data_point) < (radius + collision_buffer)


def predict(data_matrix):
    result = []
    last_xy = data_matrix[-1]
    prev_xy = last_xy
    num_prediction_steps = NUM_SECONDS * FPS

    prev_prev_x = data_matrix[-2][0]
    prev_prev_y = data_matrix[-2][1]
    prev_x = last_xy[0]
    prev_y = last_xy[1]
    current_x_increasing = 0 < prev_x - prev_prev_x
    current_y_increasing = 0 < prev_y - prev_prev_y

    # To prevent getting stuck probability of a true decrease if last move was a turn
    prob_turn = 1.0
    while num_prediction_steps:
        num_prediction_steps -= 1
        heading = get_heading(data_matrix[-1], data_matrix[-2])
        curr_xy = get_next_step(current_y_increasing, current_x_increasing, prev_xy, heading)

        # Turn with probability .01 when in collision zone
        turn_dampner = .05
        if (in_zone(curr_xy) or in_circle(
                curr_xy)) and random.random() < prob_turn:  # and random.choice([True, False]):
            # make it unlikely to do a turn immedialy follow by another turn
            prob_turn *= turn_dampner
            # try change x see if we are now clear
            curr_xy = get_next_step(current_y_increasing, not current_x_increasing, prev_xy, 5 / 6 * pi)
            if not (in_zone(curr_xy) or in_circle(curr_xy)):
                current_x_increasing = not current_x_increasing
            else:
                # then try change just y and see if we are now clear
                curr_xy = get_next_step(not current_y_increasing, current_x_increasing, prev_xy, None)
                if not (in_zone(curr_xy) or in_circle(curr_xy)):
                    current_y_increasing = not current_y_increasing
                else:
                    # finally change both
                    current_x_increasing = not current_x_increasing
                    current_y_increasing = not current_y_increasing
                    curr_xy = get_next_step(current_y_increasing, current_x_increasing, prev_xy, heading)
        else:
            # restore likihood of a turn
            if prob_turn < 1.0:
                prob_turn *= turn_dampner

        curr_xy = trunc_xy(curr_xy)
        result.append(curr_xy)
        prev_xy = curr_xy
        # print 'godfrey', num_prediction_steps

    return result


def get_next_step(current_y_increasing, current_x_increasing, prev_xy, heading):
    x_delta = DELTA_X
    y_delta = DELTA_Y
    # TODO: need to figure out if this should increasing or decreasing:
    if not current_x_increasing:
        x_delta = -x_delta
    if not current_y_increasing:
        y_delta = -y_delta

    if (heading):
        heading = angle_trunc(heading)
        # curr_xy = prev_xy + (x_delta * cos(heading), y_delta * sin(heading))
        # based on trial and error the following produces best results
        curr_xy = prev_xy + (x_delta * sin(heading), y_delta * cos(heading))
    else:
        curr_xy = prev_xy + (x_delta, y_delta)
    # // the following allows -- 3212.063668 so maybe using heading is not great
    # curr_xy = prev_xy + (x_delta, y_delta)
    return curr_xy


# predict randomly
def predict_random(data_matrix):
    num_prediction_steps = NUM_SECONDS * FPS
    result = np.random.random((num_prediction_steps, 2)) * (MAX_X - MIN_X, MAX_Y - MIN_Y) + (MIN_X, MIN_Y)
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
    # prediction_matrix = predict_random(data_matrix)
    prediction_matrix = predict(data_matrix)
    np.savetxt('prediction.txt', prediction_matrix, delimiter=',', fmt='%i')

#     run the finalproject

if __name__ == "__main__":
    sys.exit(main(sys.argv))
