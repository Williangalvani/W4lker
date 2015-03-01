import abc
from genericLeg import Leg
import bge

from math import radians as d2r


scene = bge.logic.getCurrentScene()

co = bge.logic.getCurrentController()

source = scene.objects

class VirtualLeg(Leg):
    def __init__(self, name, position):
        Leg.__init__(self, name, position)
        self.armature = source.get(name)



    def move_to_angle(self, shoulderAngle, femurAngle, tibiaAngle):
        self.check_limits()

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
