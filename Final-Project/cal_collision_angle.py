__author__ = 'godfreyhobbs'

import re
from math import *
import numpy as np
import csv
from collisions_detection import *
#
# Need to calculate the angle of the collision based on the following:
# angle <-- f(prior_path_est,posterior_path_est)
# repeat following for prior and posterior
# get points in a path -> preform linear regression to get slope.  Throw out paths that have high regression error (R2 values)
# refinement would be to cluster the angles, collision point to look for patterns


def cal_collision_angle(paths):
    prev_path = paths[0]
    for curr_path in paths[1:]:
        # TODO: use linear regression

        # Start simple
        # grab the initial the point of col and the then the furthest point from each the before and the after curr_path
        # check if curr_path start and en together.  if not here is some thrash.
        # print curr_path[1], curr_path[-1]
        # print prev_path[1], prev_path[-1]
        if (prev_path[-1] == curr_path[0]).all():
            # print "godfrey", curr_path
            incoming_angle = get_angle(prev_path[0], prev_path[len(prev_path)/2], prev_path[-1])
            print curr_path[0][0],',',curr_path[0][1],',',incoming_angle ,',',get_angle(prev_path[0], curr_path[0], curr_path[1])
        prev_path = curr_path


input_file = 'Inputs/training_data.txt'
input_array = np.genfromtxt(input_file, delimiter=',', dtype=int)
pixels, paths = cal_collision_pixles(input_array)
cal_collision_angle(paths)
# print_data_matrix(paths)
