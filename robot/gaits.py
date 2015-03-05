__author__ = 'will'
import math
import time
from robot import robotData
import numpy
from robot.tranforms import rotateAroundCenter, distance


class Gait():
    def __init__(self, robot):
        pass

    def height_at_progression(self, prog):
        pass

    def reset(self):
        pass

    def iterate(self, delta, deltaRot):
        pass

class TrotGait(Gait):

    z_profile = [0, 0, 0, 0, 0, 5, 20, 25, 20, 3] #leg height x time

    z_points = len(z_profile)
    startTime = 0
    stepDistance = 2000
    lastDelta = numpy.array([0, 0, 0])
    currentDistance = 0

    def __init__(self, robot):
        Gait.__init__(self, robot)
        self.z_profile.append(self.z_profile[0])
        self.robot = robot



    def height_at_progression(self, prog):
        """

        :param prog: [0,1]
        :return:
        """
        index = math.floor(prog*self.z_points)
        diff = prog * self.z_points - index
        value = self.z_profile[int(index)] + (self.z_profile[int(index+1)] - self.z_profile[int(index)])*diff

        prog = prog if prog <= 0.5 else 1-prog
        speed = prog * 2

        # direction = 2 if value else 0
        return value, speed



    def iterate(self, delta, deltaRot):

        rotationalDistance = distance(robotData.legs_resting_positions[0], rotateAroundCenter(robotData.legs_resting_positions[0], 'z', deltaRot[2]))
        thisDistance = math.sqrt(delta[0]**2 + delta[1]**2 + delta[2]**2) + rotationalDistance
        self.currentDistance = (self.currentDistance + thisDistance) % self.stepDistance

        step_progression = self.currentDistance / self.stepDistance
        step_progression_alternate = (step_progression + 0.5) % 1.0
        # print(step_progression, step_progression_alternate)

        fl_rest, fr_rest, rr_rest, rl_rest = robotData.legs_resting_positions

        height1, speed1 = self.height_at_progression(step_progression)

        height2, speed2 = self.height_at_progression(step_progression_alternate)

        rotations = []
        for pos in robotData.legs_resting_positions:
            vector = rotateAroundCenter(pos, 'z', deltaRot[2]) - pos
            rotations.append(vector)


        front_left_offset =  [(delta[0]+rotations[0][0])*speed1, (delta[1]+rotations[0][1])*speed1, delta[2]+height1]
        front_right_offset = [(delta[0]+rotations[1][0])*speed2, (delta[1]+rotations[1][1])*speed2, delta[2]+height2]
        rear_right_offset = [(delta[0]+rotations[2][0])*speed1, (delta[1]+rotations[2][1])*speed1, delta[2]+height1]
        rear_left_offset =  [(delta[0]+rotations[3][0])*speed2, (delta[1]+rotations[3][1])*speed2, delta[2]+height2]

        self.robot.move_leg_to_point('front_left',  *(fl_rest + front_left_offset))
        self.robot.move_leg_to_point('front_right', *(fr_rest + front_right_offset))
        self.robot.move_leg_to_point('rear_left',  *(rl_rest + rear_left_offset))
        self.robot.move_leg_to_point('rear_right', *(rr_rest + rear_right_offset))

    def reset(self):
        pass