__author__ = 'will'

from robot.robotInterfaces.legInterfaces.genericLeg import Leg

from math import pi


class RealLeg(Leg):

    def __init__(self, name, position, panServo, femurServo, tibiaServo, resting_positions):
        super(RealLeg, self).__init__(name, position, resting_positions)
        self.position = position
        self.panServo = panServo
        self.tibiaServo = tibiaServo
        self.femurServo = femurServo
        self.femurServo.set_angle_limits(-90, 65)
        self.tibiaServo.set_angle_limits(-55, 90)
        # viewer.create()

        self.ydirection = -1 if "right" in self.name else 1

        #self.shoulderAngle = True if self.name in ["rear_right","front_left"] else False
        #self.offset = pi/2 if self.shoulderAngle else 0

    def move_to_angle(self, shoulderAngle, femurAngle, tibiaAngle):
        """
        Moves joints to specified angles
        """
        self.check_limits(shoulderAngle, femurAngle, tibiaAngle)
        #if self.shoulderAngle:
            #self.panServo.move_to_angle(-shoulderAngle - self.offset)
        #else:
        self.panServo.move_to_angle(shoulderAngle)

        self.femurServo.move_to_angle(femurAngle*self.ydirection)
        self.tibiaServo.move_to_angle(tibiaAngle)
