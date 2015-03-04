__author__ = 'will'


from math import *
import bge
from math import radians as d2r
from robot import robotData
from robot.robotInterfaces.genericRobot import Robot
from robot.robotInterfaces.legInterfaces.virtualLeg import VirtualLeg
# viewer.create()
key = bge.logic.keyboard.events
scene = bge.logic.getCurrentScene()
co = bge.logic.getCurrentController()
source = scene.objects

class VirtualRobot(Robot):
    width = robotData.width
    length = robotData.length
    heigth = robotData.heigth
    orientation = [0, 0, 0]

    def __init__(self):
        self.legs = self.load_legs()
        self.i = 0

    def load_legs(self):
        width = self.width
        length = self.length
        heigth = self.heigth

        legs = {
            "front_left": VirtualLeg("front_left",   (length / 2,width/2,   heigth)),
            "front_right": VirtualLeg("front_right", (length / 2, -width/2 , heigth)),
            "rear_right": VirtualLeg("rear_right",   (-length / 2, -width/2, heigth)),
            "rear_left": VirtualLeg("rear_left",     (-length / 2, width/2,  heigth)),
            }

        return legs

    def move_legs_to_angles(self, angles):
        for leg in self.legs.items():
            leg[1].move_to_angle(*angles)

    def read_feet(self):
            return [0, 0, 0, 0]

    def read_imu(self):
        self.orientation[1] += 0.1
        self.orientation[1]%= 30
        print(self.orientation)
        return self.orientation

    def move_leg_to_point(self, leg, x, y, z):
        try:
            self.legs[leg].move_to_pos(x, y, z)
        except Exception as e:
            print("out of bounds", e)

    def start(self):
        pass

    def disconnect(self):
        pass
