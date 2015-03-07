import abc
from robot.robotInterfaces.legInterfaces.genericLeg import Leg
from vreptest import vrep
import time

class VirtualLegVrep(Leg):
    def __init__(self, name, handles, position,resting_positions):
        Leg.__init__(self, name, position,resting_positions)
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
