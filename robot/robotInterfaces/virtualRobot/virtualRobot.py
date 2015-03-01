__author__ = 'will'


from math import *
import bge
from math import radians as d2r
from robot import robotData
from robot.robotInterfaces.genericRobot import Robot
# viewer.create()
key = bge.logic.keyboard.events

scene = bge.logic.getCurrentScene()

co = bge.logic.getCurrentController()

source = scene.objects

class Leg():
    panServo = None
    tibiaServo = None
    femurServo = None
    position = None
    orientation = None
    direction = 1

    def __init__(self, name, position):
        self.armature = source.get(name)
        self.name = name
        self.position = position
        self.tibiaLength = robotData.tibiaLength
        self.femurLength = robotData.femurLength

        if "right" in self.name:
            self.direction = -1


    def ik_to(self, x0, y0, z0):

        dx = x0 - self.position[0]
        dy = y0 - self.position[1]
        dz = z0 - self.position[2]
        COXA_LENGTH = 20
        FEMUR_LENGTH = robotData.femurLength
        TIBIA_LENGTH = robotData.tibiaLength

        x,y,z = dy*self.direction,-dz,-dx*self.direction

        tibiaAngle = acos(((sqrt(((sqrt(x ** 2 + z ** 2)) - COXA_LENGTH) ** 2 + y ** 2)) ** 2 - TIBIA_LENGTH ** 2 - FEMUR_LENGTH ** 2) / (-2 * FEMUR_LENGTH * TIBIA_LENGTH)) * 180 / pi
        coxaAngle = atan2(z , x) * 180 / pi
        femurAngle = (((atan(((sqrt(x ** 2 + z ** 2)) - COXA_LENGTH) / y)) + (acos((TIBIA_LENGTH ** 2 - FEMUR_LENGTH ** 2 - (sqrt(((sqrt(x ** 2 + z ** 2)) - COXA_LENGTH) ** 2 + y ** 2)) ** 2) / (-2 * FEMUR_LENGTH * (sqrt(((sqrt(x ** 2 + z ** 2)) - COXA_LENGTH) ** 2 + y ** 2)))))) * 180 / pi) - 90

        return d2r(coxaAngle), d2r(femurAngle), d2r(tibiaAngle-90)

    def move_to_pos(self, x, y, z):
        angles = self.ik_to(x, y, z)
        self.move_to_angle(*angles)

    def move_to_angle(self, shoulderAngle, femurAngle, tibiaAngle):
        shoulderAngle = degrees(shoulderAngle)
        femurAngle = degrees(femurAngle)
        tibiaAngle = degrees(tibiaAngle)

        femurServoLimits = robotData.femurServoLimits
        shoulderServoLimits = robotData.shoulderServoLimits
        tibiaServoLimits = robotData.tibiaServoLimits

        if self.direction == -1:
            shoulderServoLimits = [-shoulderServoLimits[1],-shoulderServoLimits[0]]

        if femurAngle<femurServoLimits[0]:
            raise Exception("femur out of bounds")
        if femurAngle>femurServoLimits[1]:
            raise Exception("femur out of bounds")
        if tibiaAngle<tibiaServoLimits[0]:
            raise Exception("tibia out of bounds")
        if tibiaAngle>tibiaServoLimits[1]:
            raise Exception("tibia out of bounds")
        if shoulderAngle<shoulderServoLimits[0]:
            raise Exception("shoulder out of bounds, attempted {0}".format(shoulderAngle))
        if shoulderAngle>shoulderServoLimits[1]:
            raise Exception("shoulder out of bounds, attempted {0}".format(shoulderAngle))


        leg = self.armature
        shoulder = leg.channels[0]
        shoulder.rotation_mode = bge.logic.ROT_MODE_XYZ
        shoulder.rotation_euler = (0, -d2r(shoulderAngle), 0)


        femur = leg.channels[2]
        femur.rotation_mode = bge.logic.ROT_MODE_XYZ
        femur.rotation_euler = (-d2r(femurAngle), 0, 0)


        tibia = leg.channels[3]
        tibia.rotation_mode = bge.logic.ROT_MODE_XYZ
        tibia.rotation_euler = (0, 0, -d2r(tibiaAngle))

        leg.update()



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
            "front_left": Leg("front left leg",   (length / 2,width/2,   heigth)),
            "front_right": Leg("front right leg", (length / 2, -width/2 , heigth)),
            "rear_right": Leg("rear right leg",   (-length / 2, -width/2, heigth)),
            "rear_left": Leg("rear left leg",     (-length / 2, width/2,  heigth)),
            }

        return legs

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


