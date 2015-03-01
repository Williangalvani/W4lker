__author__ = 'will'

from math import radians as d2r
from math import *
import scipy.optimize as opt

def ik_solver(x, y, z):

    def forward_ik(args):
        shoulder, femur, tibia = args
        pos0 = [0, 0]
        femurLength = 50
        tibiaLength = 50

        femur = femur
        sinShoulder = sin(shoulder)
        cosShoulder = cos(shoulder)
        pos1 = [pos0[0] + cos(femur) * femurLength,
                pos0[1] + sin(femur) * femurLength, ]


        pos2 = [pos1[0] + cos(femur - (pi - tibia)) * tibiaLength,
                pos1[1] + sin(femur - (pi - tibia)) * tibiaLength, ]

        # print pos1, pos2
        #
        # pos1 = [pos1[0]*sinShoulder,
        #         pos1[0]*cosShoulder,
        #         pos1[1]]

        pos2 = [pos2[0]*sinShoulder,
                pos2[0]*cosShoulder,
                 pos2[1]]
        return pos2

    def error(args):
        x2,y2,z2 = forward_ik(args)
        return sqrt((x2-x)**2 +(y2-y)**2 +(z2-z)**2)

    return opt.fmin_slsqp(func=error,
            x0=[0,0,pi/2],
            bounds=[(-pi/2,pi/2),(-pi/2,pi/2),(0,pi)],
            iprint=2,
            acc=0.1)


print ik_solver(0,0,100)