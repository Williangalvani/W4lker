import time
from robot.gaits import TrotGait, TrotGait

__author__ = 'will'

import math
from math import radians as d2r
from robot.tranforms import rotate
from robot import robotData
from robot.input.keylistener import KeyListener
import numpy

class RobotController():
    def __init__(self, robot):
        self.robot = robot
        self.dx = 100
        self.dy = 0
        self.dz = 0
        self.drot = [0, 0, 0]

        self.keyListener = KeyListener()
        self.startTime = time.time()
        self.trotgait = TrotGait(self.robot)
        self.trotgait.reset()



    def keep_feet_horizontal(self):
            self.robot.read_imu()
            # print "orientation:", self.orientation
            roll = self.robot.orientation[1]
            pitch = self.robot.orientation[0]
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
        self.robot.start()


    def run(self):
        for i in range(1, 1000):
            self.iterate()

    def trot(self):
        self.trotgait.iterate([self.dx,self.dy,self.dz],self.drot)

    def get_ground_rotated_legs_resting_position(self):
        pass

    def move_legs_to_offset(self, offset):
        self.move_legs_to_offsets(offset, offset, offset, offset)

    def move_legs_to_offsets(self, front_left_offset, front_right_offset, rear_left_offset, rear_right_offset):

        fl_rest, fr_rest, rr_rest, rl_rest = robotData.legs_resting_positions

        self.robot.move_leg_to_point('front_left', *(fl_rest + front_left_offset))
        self.robot.move_leg_to_point('front_right',*(fr_rest + front_right_offset))
        self.robot.move_leg_to_point('rear_left',  *(rl_rest + rear_left_offset))
        self.robot.move_leg_to_point('rear_right', *(rr_rest + rear_right_offset))


    def move_legs_to_angles(self,a,b,c):
        self.robot.move_legs_to_angles( [a,b,c])

    def iterate(self):
        # self.i += 1
        # print("iterating i = ", self.i, self.dx, self.dy, self.dz)
        try:
            self.read_keyboard()
        except Exception as e:
            print("could not read keyboard:", e)
        # self.move_legs_to_offset([self.dx,self.dy,self.dz])
        # self.move_legs_to_angles(math.pi/4,math.pi/4,math.pi/4)
        self.trot()
        self.robot.finish_iteration()
        time.sleep(0.005)


    def read_keyboard(self):

        dx = dy = dz = 0


        if self.keyListener.get_key(119):
            dx = 1
        elif self.keyListener.get_key(115):
            dx = -1
        else:
            dx = 0
        if self.keyListener.get_key(97):
            dy = 1
        elif self.keyListener.get_key(100):
            dy = -1
        else:
            dy = 0
        if self.keyListener.get_key(114):
            dz = 1
        elif self.keyListener.get_key(102):
            dz = -1
        else:
            dz = 0
        if self.keyListener.get_key(116):
            self.dx = self.dy = self.dz = self.drot[2] = 0
        if self.keyListener.get_key(113):
            self.drot[2] += 0.006
        elif self.keyListener.get_key(101):
            self.drot[2] -= 0.006

        if self.keyListener.get_key(49):
            self.robot.disconnect()
        self.dx+=dx
        self.dy+=dy
        self.dz+=dz
        # print(self.dx,self.dy,self.dz)


def run_with_real_robot():
    from robot.robotInterfaces.realRobot.realRobot import RealRobot
    r = RealRobot()
    controller = RobotController(r)
    controller.start()
    controller.run()


if __name__ == "__main__":
    run_with_real_robot()



