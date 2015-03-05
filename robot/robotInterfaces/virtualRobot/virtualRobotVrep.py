__author__ = 'will'


from robot import robotData
from robot.robotInterfaces.genericRobot import Robot
from robot.robotInterfaces.legInterfaces.virtualLegVrep import VirtualLegVrep

from vreptest import vrep



class VirtualRobotVrep(Robot):
    width = robotData.width
    length = robotData.length
    heigth = robotData.heigth
    orientation = [0, 0, 0]

    def __init__(self):
        vrep.simxFinish(-1)  # just in case, close all opened connections
        self.clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
        self.legs = self.load_legs()
        self.i = 0
        vrep.simxSynchronous(self.clientID,True)
        print "connected with id ", self.clientID

    def finish_iteration(self):
        vrep.simxSynchronousTrigger(self.clientID)

    def get_joints(self):
        if self.clientID != -1:
            errorCode, handles, intData, floatData, array = vrep.simxGetObjectGroupData(self.clientID,vrep.sim_appobj_object_type,0,vrep.simx_opmode_oneshot_wait)

            data = dict(zip(array, handles))

            joints = {}
            for name in data:
                if "joint" in name:
                    joints[name] = data[name]
            # print joints

            fl_leg = dict((key,value) for key, value in data.iteritems() if "fl" in key and "joint" in key)
            fr_leg = dict((key,value) for key, value in data.iteritems() if "fr" in key and "joint" in key)
            rr_leg = dict((key,value) for key, value in data.iteritems() if "rr" in key and "joint" in key)
            rl_leg = dict((key,value) for key, value in data.iteritems() if "rl" in key and "joint" in key)

            return fl_leg,fr_leg,rr_leg,rl_leg
        return None

    def load_legs(self):
        width = self.width
        length = self.length
        heigth = self.heigth
        fl,fr,rr,rl = self.get_joints()
        # print "joints:" , self.get_joints()
        legs = {
            "front_left": VirtualLegVrep("front_left", (fl,self.clientID),   (length / 2,width/2,   heigth)),
            "front_right": VirtualLegVrep("front_right",(fr,self.clientID), (length / 2, -width/2 , heigth)),
            "rear_right": VirtualLegVrep("rear_right", (rr,self.clientID),  (-length / 2, -width/2, heigth)),
            "rear_left": VirtualLegVrep("rear_left",   (rl,self.clientID),    (-length / 2, width/2,  heigth)),
            }

        return legs

    def move_legs_to_angles(self, angles):
        for leg in self.legs.items():
            # print leg[1]
            leg[1].move_to_angle(*angles)

    def read_feet(self):
            return [0, 0, 0, 0]

    def read_imu(self):
        self.orientation[1] += 0.1
        self.orientation[1]%= 30
        print(self.orientation)
        return self.orientation

    def move_leg_to_point(self, leg, x, y, z):
        try:
            self.legs[leg].move_to_pos(x, y, z)
        except Exception as e:
            print("out of bounds", e)

    def start(self):
        pass

    def disconnect(self):
        pass
