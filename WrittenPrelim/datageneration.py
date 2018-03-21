import numpy as np
from math import sin, cos, sqrt

def rotate2D(point, t):
    M = [[cos(t), -sin(t)],
         [sin(t), cos(t)]]
    pt = [point[0], point[1]]
    o = np.dot(M, pt)
    return o

def rotation_matrix_numpy(axis, theta):
    axis = axis/sqrt(np.dot(axis, axis))
    a = cos(theta/2.)
    b, c, d = -axis*sin(theta/2.)

    return np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                  [2*(b*c+a*d), a*a+c*c-b*b-d*d, 2*(c*d-a*b)],
                  [2*(b*d-a*c), 2*(c*d+a*b), a*a+d*d-b*b-c*c]])

def rotate3D(point, v, t):
    M = rotation_matrix_numpy(np.array(v), t)
    pt = [point[0], point[1], point[2]]
    o = np.dot(M, pt)
    return o
