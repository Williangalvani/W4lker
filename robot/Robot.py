import time

__author__ = 'will'

import math
from math import radians as d2r
from robot.tranforms import rotate

class RobotController():
    def __init__(self, robot):
        self.robot = robot
        self.dx = 0
        self.dy = 0
        self.dz = 0


    def keep_feet_horizontal(self):
            self.robot.read_imu()
            # print "orientation:", self.orientation
            roll = self.orientation[1]
            pitch = self.orientation[0]
            sin = math.sin(math.radians(pitch))
            # self.move_leg_to_point('front_left', 80, 75, -50 + sin*30)
            # self.move_leg_to_point('front_right', -(80), 75, -50 - sin*30)
            self.robot.move_leg_to_point('front_left', *rotate([60,75,-50],'y',-d2r(roll)))
            self.robot.move_leg_to_point('front_right', *rotate([-60,75,-50],'y',-d2r(roll)))

    def keep_body_horizontal(self):
        self.robot.read_imu()
        # print "orientation:", self.orientation
        roll = self.robot.orientation[1]
        pitch = self.robot.orientation[0]
        sin = math.sin(math.radians(pitch))
        # self.move_leg_to_point('front_left', 80, 75, -50 + sin*30)
        # self.move_leg_to_point('front_right', -(80), 75, -50 - sin*30)
        self.robot.move_leg_to_point('front_left', *rotate([0,75,-50],'y',d2r(roll)))
        self.robot.move_leg_to_point('front_right', *rotate([0,75,-50],'y',d2r(roll)))


    def start(self):
        pass


    def run(self):

        for i in xrange(1, 1000):
            self.iterate()
            time.sleep(0.04)


    i = 0
    def iterate(self):
        self.i += 1
        print(self.dx,self.dy,self.dz)
        self.read_keyboard()
        self.robot.move_leg_to_point('front_left',
                                     50+self.dx,
                                     75+self.dy,
                                     -50+self.dz)
        self.robot.move_leg_to_point('front_right',
                                     -50+self.dx,
                                     75+self.dy,
                                     -50+self.dz)

        # self.keep_body_horizontal()


    def read_keyboard(self):
        import bge
        co = bge.logic.getCurrentController()
        # 'Keyboard' is a keyboard sensor
        sensor = co.sensors["Keyboard"]
        dx = dy = dz = 0
        for key,status in sensor.events:
                # key[0] == bge.events.keycode, key[1] = status
                # print(key,status)
                if status == bge.logic.KX_INPUT_ACTIVE:
                        if key == 119:
                            dx = 1
                        elif key == 115:
                            dx = -1
                        else:
                            dx = 0
                        if key == 97:
                            dy = 1
                        elif key == 100:
                            dy = -1
                        else:
                            dy = 0
                        if key == 114:
                            dz = 1
                        elif key == 102:
                            dz = -1
                        else:
                            dz = 0
        self.dx+=dx
        self.dy+=dy
        self.dz+=dz



def run_with_real_robot():
    r = RealRobot()
    controller = RobotController(r)
    controller.start()
    controller.run()


if __name__ == "__main__":
    from robot.robotInterfaces.realRobot.realRobot import RealRobot
    run_with_real_robot()



