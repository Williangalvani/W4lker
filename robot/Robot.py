import time

__author__ = 'will'

import math
from serialServoCommander import SerialComms
import viewer


def triangle_angle(a, b, c):
    if c == 0:
        return 0
    a = abs(a)
    b = abs(b)
    c = abs(c)

    cosA = (a ** 2 - b ** 2 - c ** 2) / (-2 * b * c)
    # print "triangle:",a,b,c , " cos: ", cos
    return math.acos(cosA)


RATE = -13.88


class Servo():
    def __init__(self, pin, pos0, rate, serial):
        self.pos0 = pos0
        self.rate = rate
        self.pin = pin
        self.serial = serial

    def move_to_angle(self, angle):
        pos = int(self.pos0 + angle * self.rate)
        # print angle, pos
        self.serial.queue.put(lambda: self.serial.move_servo_to(self.pin, pos))


class Leg():
    panServo = None
    tibiaServo = None
    femurServo = None
    position = None
    orientation = None

    def __init__(self, position, panServo, femurServo, tibiaServo, femurLength, tibiaLength,):
        self.position = position
        self.panServo = panServo
        self.tibiaServo = tibiaServo
        self.femurServo = femurServo
        self.tibiaLength = tibiaLength
        self.femurLength = femurLength
        viewer.create()


    def move_to(self, x, y, z):
        maxsize = self.femurLength + self.tibiaLength
        dx = dy = dz = 0
        coords = [x,y,z]
        if 'max' in coords or 'min' in coords:
            limit = 'max' if 'max' in coords else 'min'
            coords[coords.index(limit)] = 0
            length = None
            while not length or length < maxsize:
                coords[coords.index(limit)] += (1 if limit == 'max' else -1)
                dx, dy, dz = [coords[i] - self.position[i] for i in range(3)]
                length = (math.sqrt(dx ** 2 + dy ** 2 + dz ** 2) > self.femurLength + self.tibiaLength)

        else:
            dx = float(x) - self.position[0]
            dy = float(y) - self.position[1]
            dz = float(z) - self.position[2]
        #
        # print "pos:", self.position
        # print "target:", coords
        # print "dx:" , dx, dy, dz
        while (math.sqrt(dx ** 2 + dy ** 2 + dz ** 2) > self.femurLength + self.tibiaLength):
            dx *= 0.999
            dy *= 0.999
            dz *= 0.999

        distxyz = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)  # total distance
        # print "total distance: ", distxyz, [dx, dy, dz]

        tibiaAngle = triangle_angle(distxyz, self.tibiaLength, self.femurLength)

        xydist = math.sqrt(dx ** 2 + dy ** 2)
        dist_vectorAngle = math.atan2(dz, xydist)

        # relevant, shoulder tilt angle
        AbsshoulderTiltAngle = triangle_angle(self.tibiaLength, self.femurLength, distxyz) + dist_vectorAngle
        AbsshoulderTiltAngle = math.degrees(AbsshoulderTiltAngle)

        AbsshoulderPanAngle = math.degrees(math.atan2(dy, dx))
        if self.position[0] < 0:
            AbsshoulderPanAngle = 180 - AbsshoulderPanAngle
        print AbsshoulderPanAngle
        tibiaAngle = math.degrees(tibiaAngle)

        self.panServo.move_to_angle(AbsshoulderPanAngle)
        self.femurServo.move_to_angle(AbsshoulderTiltAngle)
        self.tibiaServo.move_to_angle(tibiaAngle - 90)
        # print "angles: ", AbsshoulderPanAngle, AbsshoulderTiltAngle, tibiaAngle, dist_vectorAngle
        # print "position: ", x, y, z

        pos0 = [0, 0]
        pos1 = [math.cos(math.radians(AbsshoulderTiltAngle)) * self.femurLength,
                math.sin(math.radians(AbsshoulderTiltAngle)) * self.femurLength, ]

        pos2 = [pos1[0] + math.cos(math.radians(AbsshoulderTiltAngle - (180 - tibiaAngle))) * self.tibiaLength,
                pos1[1] + math.sin(math.radians(AbsshoulderTiltAngle - (180 - tibiaAngle))) * self.tibiaLength, ]
        # viewer.update_lines([pos0, pos1, pos2])


class Robot():
    width = 100
    length = 150
    heigth = 30


    def __init__(self):
        width = 100
        length = 150
        heigth = 30
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

        self.legs = {"front_left": Leg((width / 2, length / 2, heigth), servos[1], servos[0], servos[2], 46, 92),
                     "front_right": Leg((-width/2,  length/2, heigth), servos[3], servos[4], servos[5], 46, 92), }
        # "rear_right" : Leg((-width/2, -length/2, heigth), 8, 9, 10, 100, 100),
        # "rear_left"  : Leg((width/2,  -length/2, heigth), 11, 12, 13, 100, 100)}
        self.feet = [False,False,False,False]

    def read_feet(self):
        self.serial.queue.put(lambda: self.serial.read_pins())
        data = self.serial.input_pins
        self.feet = [not ((data >> bit) & 1) for bit in range(4 - 1, -1, -1)]
        print self.feet

    def read_imu(self):
        self.serial.queue.put(lambda: self.serial.read_imu())
        self.orientation = self.serial.imu
        return self.serial.imu

    def move_leg(self, leg, x, y, z):
        leg_origin = self.legs[leg].position[0:2]
        leg_target = [x, y]
        # viewer.update_leg(leg,[leg_origin,leg_target])
        self.legs[leg].move_to(x, y, z)

    def run(self):
        print self.legs["front_left"].position
        self.serial.start()
        for servo in self.servos:
            servo.move_to_angle(0)
        time.sleep(5)

        # for i in range(100):
        #     time.sleep(0.1)
        #     print self.read_imu()
        # for i in xrange(1, 100):
        #     # for servo in self.servos:
        #     # servo.move_to_angle(0)
        #     print self.read_imu()
        #     self.move_leg('front_left', 50 + i, 75, -50)
        #     self.move_leg('front_right', -(50 + i), 75, -50)
        #     time.sleep(0.01)
        #     self.read_feet()
        #     # if self.feet[-1]:
        #     #     time.sleep(10)
        #     #     break

        for i in xrange(1, 1000):
            self.read_imu()
            print self.orientation
            roll = self.orientation[1]
            sin = math.sin(math.radians(roll))
            self.move_leg('front_left', 80, 75, -50 + sin*30)
            self.move_leg('front_right', -(80), 75, -50 - sin*30)
            time.sleep(0.05)



        print "done"
        self.serial.running = False
        self.serial.join()
        time.sleep(5)


r = Robot()
r.run()