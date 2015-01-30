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
        pos = int(1500 + angle * self.rate)
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
        dx = float(x) - self.position[0]
        dy = float(y) - self.position[1]
        dz = float(z) - self.position[2]

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

        AbsshoulderPanAngle = math.degrees(math.atan2(x, y))

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
        viewer.update_lines([pos0, pos1, pos2])


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
                       Servo(pin=7, rate=RATE, pos0=1500, serial=serial),
                       Servo(pin=8, rate=RATE, pos0=1500, serial=serial),
                       Servo(pin=9, rate=RATE, pos0=1500, serial=serial),
                       Servo(pin=10, rate=RATE, pos0=1500, serial=serial),
                       Servo(pin=11, rate=RATE, pos0=1500, serial=serial),
                       Servo(pin=12, rate=RATE, pos0=1500, serial=serial),
                       Servo(pin=13, rate=RATE, pos0=1500, serial=serial)]
        servos = self.servos

        self.legs = {"front_left": Leg((width / 2, length / 2, heigth), servos[1], servos[0], servos[2], 45, 80), }
        # "front_right": Leg((-width/2,  length/2, heigth), 5, 6, 7, 100, 100),
        # "rear_right" : Leg((-width/2, -length/2, heigth), 8, 9, 10, 100, 100),
        # "rear_left"  : Leg((width/2,  -length/2, heigth), 11, 12, 13, 100, 100)}
        self.feet = [False,False,False,False]

    def read_feet(self):
        self.serial.queue.put(lambda: self.serial.read_pins())
        data = self.serial.input_pins
        self.feet = [not ((data >> bit) & 1) for bit in range(4 - 1, -1, -1)]
        print self.feet

    def run(self):
        print self.legs["front_left"].position
        self.serial.start()
        for servo in self.servos:
            servo.move_to_angle(0)
        time.sleep(5)
        for i in xrange(-40,60):
            # for servo in self.servos:
            # servo.move_to_angle(0)
            self.legs['front_left'].move_to(90, 115, -i)
            print i
            time.sleep(0.03)
            self.read_feet()
            if self.feet[-1]:
                time.sleep(10)
                break

        print "done"
        self.serial.running = False
        self.serial.join()
        time.sleep(5)


r = Robot()
r.run()