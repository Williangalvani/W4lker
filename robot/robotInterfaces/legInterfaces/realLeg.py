__author__ = 'will'

from robot.robotInterfaces.legInterfaces.genericLeg import Leg

from math import pi
class RealLeg(Leg):

    def __init__(self, name, position, panServo, femurServo, tibiaServo):
        super(RealLeg, self).__init__(name, position)
        self.position = position
        self.panServo = panServo
        self.tibiaServo = tibiaServo
        self.femurServo = femurServo
        self.femurServo.set_angle_limits(-90, 65)
        self.tibiaServo.set_angle_limits(-55, 90)
        # viewer.create()


    def move_to_angle(self, shoulderAngle, femurAngle, tibiaAngle):
        print("trying to move to",shoulderAngle,femurAngle,tibiaAngle)
        self.panServo.move_to_angle(shoulderAngle)
        self.femurServo.move_to_angle(femurAngle)
        self.tibiaServo.move_to_angle(tibiaAngle - pi/2)
