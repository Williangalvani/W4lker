import time

__author__ = 'will'

import math
from serialServoCommander import SerialComms

def triangle_angle(a,b,c):
    return math.acos((a**2 - b**2 - c**2)/(-2*b*c))


RATE = 10

class Servo():
    def __init__(self, pin, pos0, rate, serial):
        self.pos0 = pos0
        self.rate = rate
        self.pin = pin
        self.serial = serial

    def move_to_angle(self, angle):
        pos = 1500 + angle * self.rate
        self.serial.queue.put(lambda: self.serial.move_servo_to(self.pin, pos))


class Leg():
    panServo = None
    tibiaServo = None
    femurServo = None
    position = None
    orientation = None

    def __init__(self, position, panServo, tibiaServo, femurServo,tibiaLength,femurLength):
        self.position = position
        self.panServo = panServo
        self.tibiaServo = tibiaServo
        self.femurServo = femurServo
        self.tibiaLength = tibiaLength
        self.femurLength = femurLength




        def move_to(x, y, z):
            dist = math.sqrt(x-(self.position[0])**2 + (y-self.position[1])**2+(y-self.position[2])**2)  # total distance
            height = z - self.position[2]

            # relevant Elbow angle !
            distAngle = triangle_angle(dist,femurLength,tibiaLength)
            AbsElbowAngle = distAngle

            tibiaAngle = triangle_angle(tibiaLength,femurLength,dist)

            xydist = math.sqrt((x-self.position[0])**2 + (y-self.position[1])**2)
            xyzdist = dist
            dist_vectorAngle = triangle_angle(xydist, xyzdist, height)

            #relevant, shoulder tilt angle!
            AbsshoulderTiltAngle = dist_vectorAngle + tibiaAngle - math.pi/2

            AbsshoulderPanAngle = math.atan(x/y)




class Robot():
    width = 100
    length = 150
    heigth = 30

    serial = SerialComms()

    servos = [Servo(pin=2, rate=RATE, pos0=1500, serial=serial),
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



    legs = {"front_left" : Leg((-width/2,  -length/2, heigth), 2, 3, 4, 100, 100),
            "front_right": Leg(( width/2,  -length/2, heigth), 5, 6, 7, 100, 100),
            "rear_right" : Leg(( width/2,   length/2, heigth), 8, 9, 10, 100, 100),
            "rear_left"  : Leg((-width/2,   length/2, heigth), 11, 12, 13, 100, 100)}



    def __init__(self):
        self.serial.start()
        for i in range(10):
            for servo in self.servos:
                print "moving"
                servo.move_to_angle(i*5)
            time.sleep(3)
        print "done"
        self.serial.running = False
        self.serial.join()





Robot()



























