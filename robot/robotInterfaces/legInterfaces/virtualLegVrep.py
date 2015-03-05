import abc
from robot.robotInterfaces.legInterfaces.genericLeg import Leg
from vreptest import vrep
import time

class VirtualLegVrep(Leg):
    def __init__(self, name, handles, position):
        Leg.__init__(self, name, position)
        self.torque = 1
        self.handles, self.clientID = handles
        for key in self.handles:
            if "shoulder" in key:
                self.shoulderHandle = self.handles[key]
            elif "femur" in key:
                self.femurHandle = self.handles[key]
            elif "tibia" in key:
                self.tibiaHandle = self.handles[key]
        print(self.name, self.handles)
        self.ydirection = -1 if "right" in self.name else 1


        # for name, handle in self.handles.iteritems():
        #     print vrep.simxSetJointForce(self.clientID,handle,10,vrep.simx_opmode_oneshot_wait)


    def move_to_angle(self, shoulderAngle, femurAngle, tibiaAngle):

        vrep.simxSetJointTargetPosition(self.clientID,self.shoulderHandle,shoulderAngle,vrep.simx_opmode_oneshot)

        vrep.simxSetJointTargetPosition(self.clientID,self.femurHandle,femurAngle*self.ydirection,vrep.simx_opmode_oneshot)

        vrep.simxSetJointTargetPosition(self.clientID,self.tibiaHandle,tibiaAngle*self.ydirection,vrep.simx_opmode_oneshot)
        import math
        # self.torque= 0#-math.pi/2#(self.torque+ 0.0011) % 90
        # print "pos:", self.torque
        # for name,handle in self.handles.iteritems():
        # #     print handle
        # #     print vrep.simxSetJointForce(self.clientID, handle, self.torque, vrep.simx_opmode_oneshot_wait)
        #     vrep.simxSetJointTargetPosition(self.clientID, handle, self.torque, vrep.simx_opmode_oneshot)
        #     # # print vrep.simxSetJointTargetVelocity(self.clientID, handle, 10, vrep.simx_opmode_oneshot)
        #     # print "currentpos:", vrep.simxGetJointPosition(self.clientID, handle, vrep.simx_opmode_oneshot)
        #     # # print vrep.simxSetJointTargetVelocity(self.clientID, handle, 10, vrep.simx_opmode_oneshot)
            # print "currentforce:", vrep.simxGetJointForce(self.clientID, handle, vrep.simx_opmode_oneshot)

        # print(self.name, tibiaAngle)# print(self.name, tibiaAngle)
        # """
        # angles in radians.
        # :par  am shoulderAngle:
        # :param femurAngle:
        # :param tibiaAngle:
        # :return:
        # """
        # self.check_limits(shoulderAngle,femurAngle,tibiaAngle)
        # # print(self.name, "virtual shoulder:" , shoulderAngle)
        # leg = self#.armature
        # shoulder = leg.channels[0]
        # shoulder.rotation_mode = bge.logic.ROT_MODE_XYZ
        # shoulder.rotation_euler = (0, -shoulderAngle, 0)
        #
        #
        # femur = leg.channels[2]
        # femur.rotation_mode = bge.logic.ROT_MODE_XYZ
        # femur.rotation_euler = (-femurAngle, 0, 0)
        #
        #
        # tibia = leg.channels[3]
        # tibia.rotation_mode = bge.logic.ROT_MODE_XYZ
        # tibia.rotation_euler = (0, 0, -tibiaAngle*self.direction)
        #
        # self.armature.update()

