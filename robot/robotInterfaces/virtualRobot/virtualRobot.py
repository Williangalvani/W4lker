__author__ = 'will'


from math import *
import math
import bge
from math import radians as d2r
from math import degrees as r2d
from robot import robotData
from robot.tranforms import *
# viewer.create()
key = bge.logic.keyboard.events

scene = bge.logic.getCurrentScene()

co = bge.logic.getCurrentController()

source = scene.objects

def triangle_angle(a, b, c):
    if c == 0:
        return 0
    a = abs(a)
    b = abs(b)
    c = abs(c)

    cosA = (a ** 2 - b ** 2 - c ** 2) / (-2 * b * c)
    # print "triangle:",a,b,c , " cos: ", cos
    return math.acos(cosA)


class Leg():
    panServo = None
    tibiaServo = None
    femurServo = None
    position = None
    orientation = None

    def __init__(self, name, position):
        self.armature = source.get(name)
        self.name = name
        self.position = position
        self.tibiaLength = robotData.tibiaLength
        self.femurLength = robotData.femurLength


    def ik_to2(self, x, y, z):
        maxsize = self.femurLength + self.tibiaLength
        dx = dy = dz = 0
        coords = [x, y, z]
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

        while (math.sqrt(dx ** 2 + dy ** 2 + dz ** 2) > self.femurLength + self.tibiaLength):
            dx *= 0.995
            dy *= 0.995
            dz *= 0.995

        distxyz = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)  # total distance

        tibiaAngle = triangle_angle(distxyz, self.tibiaLength, self.femurLength)

        xydist = math.sqrt(dx ** 2 + dy ** 2)

        dist_vectorAngle = math.atan2(dz, xydist)

        if "right" in self.name:
            if dx < 0:
                dist_vectorAngle = pi - dist_vectorAngle



        # relevant, shoulder tilt angle
        AbsshoulderTiltAngle = triangle_angle(self.tibiaLength, self.femurLength, distxyz) + dist_vectorAngle
        AbsshoulderTiltAngle = math.degrees(AbsshoulderTiltAngle)

        try:
            AbsshoulderPanAngle = math.degrees(math.atan(dy/dx))
        except:
            AbsshoulderPanAngle = pi/2

        tibiaAngle = math.degrees(tibiaAngle)

        if "right" in self.name:

            AbsshoulderPanAngle = -AbsshoulderPanAngle
            print("dist_vector_angle:", r2d(dist_vectorAngle), dx, self.position[1], xydist)

        # pos0 = [0, 0]
        # pos1 = [math.cos(math.radians(AbsshoulderTiltAngle)) * self.femurLength,
        #         math.sin(math.radians(AbsshoulderTiltAngle)) * self.femurLength, ]
        #
        # pos2 = [pos1[0] + math.cos(math.radians(AbsshoulderTiltAngle - (180 - tibiaAngle))) * self.tibiaLength,
        #         pos1[1] + math.sin(math.radians(AbsshoulderTiltAngle - (180 - tibiaAngle))) * self.tibiaLength, ]
        # viewer.update_lines([pos0, pos1, pos2])
        # print(AbsshoulderPanAngle, AbsshoulderTiltAngle, tibiaAngle)
        return AbsshoulderPanAngle, AbsshoulderTiltAngle, tibiaAngle - 90


    def ik_to(self, x, y, z):
        import scipy.optimize as opt
        def forward_ik(args):
            shoulder, femur, tibia = args
            pos0 = self.position[1:]
            femurLength = 50
            tibiaLength = 50

            femur = femur
            sinShoulder = sin(shoulder)
            cosShoulder = cos(shoulder)
            pos1 = [pos0[0] + cos(femur) * femurLength,
                    pos0[1] + sin(femur) * femurLength, ]


            pos2 = [pos1[0] + cos(femur - (pi - tibia)) * tibiaLength,
                    pos1[1] + sin(femur - (pi - tibia)) * tibiaLength, ]

            # print pos1, pos2
            #
            # pos1 = [pos1[0]*sinShoulder,
            #         pos1[0]*cosShoulder,
            #         pos1[1]]

            pos2 = [pos2[0]*sinShoulder,
                    pos2[0]*cosShoulder,
                     pos2[1]]
            return pos2

        def error(args):
            x2,y2,z2 = forward_ik(args)
            return sqrt((x2-x)**2 +(y2-y)**2 +(z2-z)**2)

        return opt.fmin_slsqp(func=error,
                x0=[0,0,pi/2],
                bounds=[(-pi/2,pi/2),(-pi/2,pi/2),(0,pi)],
                iprint=0,
                acc=0.01)



    def move_to_pos(self, x, y, z):
        angles = self.ik_to(x, y, z)
        angles[-1]-=pi/2
        angles[0]*=-1
        if "left" in self.name:
            print([degrees(angle) for angle in angles])
        self.move_to_angle(*angles)

    def move_to_angle(self, shoulderAngle, femurAngle, tibiaAngle):
        shoulderAngle = degrees(shoulderAngle)
        femurAngle = degrees(femurAngle)
        tibiaAngle = degrees(tibiaAngle)

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



class VirtualRobot():
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
            "front_left": Leg("front left leg", (width / 2, length / 2, heigth)),
            "front_right": Leg("front right leg", (-width / 2, length / 2, heigth)),
            "rear_right": Leg("rear right leg", (width / 2, -length / 2, heigth)),
            "rear_left": Leg("rear left leg", (-width / 2, -length / 2, heigth)),
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
        leg_origin = self.legs[leg].position[0:2]
        leg_target = [x, y]
        # print(leg_origin, leg_target)

        # viewer.update_leg(leg,[leg_origin,leg_target])
        self.legs[leg].move_to_pos(x, y, z)

    def start(self):
        pass


