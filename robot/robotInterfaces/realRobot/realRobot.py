import time
import math

from robot import robotData
from robot.robotInterfaces.legInterfaces.realLeg import RealLeg
from robot.robotInterfaces.realRobot import viewer
from serialServoCommander import SerialComms

RATE = robotData.genericServoRate

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


class Servo():
    def __init__(self, pin, pos0, rate, serial):
        self.pos0 = pos0
        self.rate = rate
        self.pin = pin
        self.maxAngle = 180
        self.minAngle = -180
        self.serial = serial

    def set_angle_limits(self, minAngle, maxAngle):
        self.maxAngle = maxAngle
        self.minAngle = minAngle

    def move_to_angle(self, angle):
        newAngle = clamp(angle, self.minAngle, self.maxAngle)
        # print newAngle
        pos = int(self.pos0 + newAngle * self.rate)
        self.serial.queue.put(lambda: self.serial.move_servo_to(self.pin, pos))


class RealRobot():
    width = robotData.width
    length = robotData.length
    heigth = robotData.heigth

    def __init__(self):
        width = self.width
        length = self.length
        heigth = self.heigth
        self.serial = SerialComms()
        serial = self.serial
        self.servos = [Servo(pin=2, rate=-RATE, pos0=1500, serial=serial),
                       Servo(pin=3, rate=RATE, pos0=1500, serial=serial),
                       Servo(pin=4, rate=RATE, pos0=1500, serial=serial),
                       Servo(pin=5, rate=RATE, pos0=1500, serial=serial),
                       Servo(pin=6, rate=RATE, pos0=1500, serial=serial),
                       Servo(pin=7, rate=-RATE, pos0=1500, serial=serial),
                       Servo(pin=8, rate=RATE, pos0=1500, serial=serial),
                       Servo(pin=9, rate=RATE, pos0=1500, serial=serial),
                       Servo(pin=10, rate=RATE, pos0=1500, serial=serial),
                       Servo(pin=11, rate=RATE, pos0=1500, serial=serial),
                       Servo(pin=12, rate=RATE, pos0=1500, serial=serial),
                       Servo(pin=13, rate=RATE, pos0=1500, serial=serial)]
        servos = self.servos

        self.legs = {"front_left": RealLeg((width / 2, length / 2, heigth), servos[1], servos[0], servos[2], 46, 92),
                     "front_right": RealLeg((-width/2,  length/2, heigth), servos[3], servos[4], servos[5], 46, 92), }
        # "rear_right" : Leg((-width/2, -length/2, heigth), 8, 9, 10, 100, 100),
        # "rear_left"  : Leg((width/2,  -length/2, heigth), 11, 12, 13, 100, 100)}
        self.feet = [False, False, False, False]

    def read_feet(self):
        self.serial.queue.put(lambda: self.serial.read_pins())
        data = self.serial.input_pins
        self.feet = [not ((data >> bit) & 1) for bit in range(4 - 1, -1, -1)]

    def read_imu(self):
        self.serial.queue.put(lambda: self.serial.read_imu())
        self.orientation = self.serial.imu
        return self.serial.imu

    def move_leg_to_point(self, leg, x, y, z):
        # viewer.update_leg(leg,[leg_origin,leg_target])
        self.legs[leg].move_to_pos(x, y, z)

    def start(self):
        self.serial.start()
        for servo in self.servos:
            servo.move_to_angle(0)
        time.sleep(5)
