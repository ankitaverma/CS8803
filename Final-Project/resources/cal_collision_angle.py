__author__ = 'godfreyhobbs'
#
#Need to calculate the angle of the collision based on the following:
# angle <-- f(prior_path_est,posterior_path_est)
# repeat following for prior and posterior
# get points in a path -> preform linear regression to get slope.  Throw out paths that have high regression error (R2 values)
# refinement would be to cluster the angles, collision point to look for patterns
