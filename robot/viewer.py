from matplotlib import pyplot as plt

import time
from pylab import ion
import pylab
# plt.show()

def create():
    fig = plt.figure()
    ax = fig.gca()
    ax.set_aspect("equal")

    ion()
    global patch
    patch = plt.Polygon([[0,0],[0,3],[3,0]], fc='y')
    ax.add_patch(patch)
    pylab.ylim([-100,100])
    pylab.xlim([-100,100])


def update_lines(lines):
    patch.set_xy(lines)
    plt.draw()
    plt.pause(0.0001)
