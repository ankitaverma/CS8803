author = 'godfreyhobbs'

import re
from math import *
import numpy as np
import csv

MIN_Y = 105
MAX_Y = 974
MIN_X = 240
MAX_X = 1696
COLLISION_ZONE_X_MIN = 330
COLLISION_ZONE_X_MAX = 1600
COLLISION_ZONE_Y_MIN = 200
COLLISION_ZONE_Y_MAX = 880


def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def in_zone(data_point):
    if COLLISION_ZONE_X_MIN < data_point[0] < COLLISION_ZONE_X_MAX:
        if COLLISION_ZONE_Y_MIN < data_point[1] < COLLISION_ZONE_Y_MAX:
            return False
    return True


center = (1008.5, 542.5)
collision_buffer = 60
radius = (227 / 2)


def in_circle(data_point):
    # diameter is 227
    # radius is 227/2

    return distance_between(center, data_point) < (radius + collision_buffer)


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
    return np.degrees(heading)


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


def print_data_matrix(data_matrix):
    print('\n'.join([','.join(['{0}'.format(item) for item in row]) for row in data_matrix]))


# Naively detect collisions.  Look for a change in heading > than say 15 degrees
def cal_collision_pixles(data_array):
    result = []
    data_array_values = np.array(data_array)

    prev_prev_x = data_array_values[0][0]
    prev_prev_y = data_array_values[0][1]
    prev_x = data_array_values[1][0]
    prev_y = data_array_values[1][1]
    current_x_increasing = 0 < prev_x - prev_prev_x
    current_y_increasing = 0 < prev_y - prev_prev_y
    prev_heading = get_heading((prev_prev_x, prev_prev_y), (prev_x, prev_y))
    direction_change = False
    steps_between_collisions = 0
    max_steps_between_collisions = 0
    thrash = 0
    max_thrash = 0
    # create a list of paths between each collision. used to help find collision angle
    paths = []
    curr_path = []
    for curr_xy in data_array_values[2:]:
        direction_change = False
        curr_path.append(curr_xy)
        steps_between_collisions += 1
        curr_x = curr_xy[0]
        curr_y = curr_xy[1]
        curr_heading = get_heading((prev_x, prev_y), (curr_x, curr_y))

        if current_x_increasing != (0 < curr_x - prev_x):
            current_x_increasing = not current_x_increasing
            direction_change = True
        if current_y_increasing != (0 < curr_y - prev_y):
            current_y_increasing = not current_y_increasing
            direction_change = True

        if direction_change and abs(curr_heading - prev_heading) > 26 and (in_zone(curr_xy) or in_circle(curr_xy)):
            if steps_between_collisions == 1:
                thrash += 1
            else:
                thrash = 0
                paths.append(curr_path)
            max_thrash = max(max_thrash, thrash)
            max_steps_between_collisions = max(steps_between_collisions, max_steps_between_collisions)
            steps_between_collisions = 0
            curr_path = []
            result.append(curr_xy)
        prev_heading = curr_heading
        # print get_angle((curr_x, curr_y), (prev_x, prev_y), (prev_prev_x, prev_prev_y)), \
        #     curr_heading,curr_xy
        prev_prev_x = prev_x
        prev_prev_y = prev_y
        prev_x = curr_x
        prev_y = curr_y

    print "max max_steps_between_collisions [", max_steps_between_collisions, "]"
    print "max_thrash [", max_thrash, "]"
    print_data_matrix(paths)
    return result, paths



input_file = 'Inputs/training_data.txt'

input_array = np.genfromtxt(input_file, delimiter=',', dtype=int)

pixels,paths = cal_collision_pixles(input_array)
print_data_matrix(pixels)


#
# def cal_candle_pixels(data_array):
#     num_y = MAX_Y - MIN_Y
#     num_x = MAX_X - MIN_X
#     arena = np.ones((num_y, num_x), dtype=bool)
#     for row in data_array:
#         x = row[0] - MIN_X
#         y = row[1] - MIN_Y
#         # clear a 7 by 7 matrix
#         # do not worry about negatives as we only really care aobut the center
#         for curr_x in range(x, x + 28):
#             for curr_y in range(y, y + 14):
#                 if curr_y < num_y and curr_x < num_x:
#                     arena[curr_y][curr_x] = False
#
#     # return arena[200:MAX_Y - 200, 200:MAX_X - 200]
#     arena = np.transpose(np.nonzero(arena[200:-200, 200:-200])) + [MIN_Y + 200, MIN_X + 200]
#     swap_cols(arena, 0, 1)
#     return arena


def swap_cols(arr, frm, to):
    arr[:, [frm, to]] = arr[:, [to, frm]]

# print(pixels.shape)
# print(np.count_nonzero(pixels))
# print_data_matrix(np.transpose(np.nonzero(pixels)) + [MIN_Y, MIN_X])
# print_data_matrix(np.transpose(np.nonzero(pixels[200:-200,200:-200])) + [MIN_Y+200, MIN_X+200])
# print_data_matrix(pixels)
# print_data_matrix(pixels)
