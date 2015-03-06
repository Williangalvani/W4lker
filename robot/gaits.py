__author__ = 'will'
import math
import time
from robot import robotData
import numpy
from robot.tranforms import rotateAroundCenter, distance


class Gait():
    def __init__(self, robot):
        self.lasttime = time.time()

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

        prog = (prog if prog <= 0.5 else 1-prog)
        speed = prog * 2

        # direction = 2 if value else 0
        return value, speed



    def iterate(self, linear_speed, angular_speed):


        rotationalDistance = distance(robotData.legs_resting_positions[0], rotateAroundCenter(robotData.legs_resting_positions[0], 'z', angular_speed[2]))
        thisDistance = math.sqrt(linear_speed[0]**2 + linear_speed[1]**2 + linear_speed[2]**2) + rotationalDistance
        self.currentDistance = (self.currentDistance + thisDistance) % self.stepDistance


        #### current feet height depends on distance (maybe shoudl depend on time? )
        step_progression = self.currentDistance / self.stepDistance
        step_progression_alternate = (step_progression + 0.5) % 1.0

        ### if stopeed, put feet down
        if (linear_speed[0]**2 + linear_speed[1]**2 + linear_speed[2]**2) < 10:
            step_progression = 0
            step_progression_alternate =0
            self.currentDistance = 0



        fl_rest, fr_rest, rr_rest, rl_rest = robotData.legs_resting_positions

        height_pair1, speed_direction_pair1 = self.height_at_progression(step_progression)

        height_pair2, speed_direction_pair2 = self.height_at_progression(step_progression_alternate)

        rotations = []
        for pos in robotData.legs_resting_positions:
            vector = rotateAroundCenter(pos, 'z', angular_speed[2]) - pos
            rotations.append(vector)

        factor = 1
        front_left_offset =  [(factor*linear_speed[0]+rotations[0][0])*speed_direction_pair1, (factor*linear_speed[1]+rotations[0][1])*speed_direction_pair1, linear_speed[2]+height_pair1]
        front_right_offset = [(factor*linear_speed[0]+rotations[1][0])*speed_direction_pair2, (factor*linear_speed[1]+rotations[1][1])*speed_direction_pair2, linear_speed[2]+height_pair2]
        rear_right_offset = [(factor*linear_speed[0]+rotations[2][0])*speed_direction_pair1, (factor*linear_speed[1]+rotations[2][1])*speed_direction_pair1, linear_speed[2]+height_pair1]
        rear_left_offset =  [(factor*linear_speed[0]+rotations[3][0])*speed_direction_pair2, (factor*linear_speed[1]+rotations[3][1])*speed_direction_pair2, linear_speed[2]+height_pair2]


        startDistance = 0
        fl_angle = math.atan2(front_left_offset[1],front_left_offset[0])
        fl_startPoint = [math.cos(fl_angle)*startDistance,math.sin(fl_angle)*startDistance,0]

        fr_angle = math.atan2(front_right_offset[1],front_right_offset[0])
        fr_startPoint = [math.cos(fr_angle)*startDistance,math.sin(fr_angle)*startDistance,0]

        rl_angle = math.atan2(rear_left_offset[1],rear_left_offset[0])
        rl_startPoint = [math.cos(rl_angle)*startDistance,math.sin(rl_angle)*startDistance,0]

        rr_angle = math.atan2(rear_right_offset[1],rear_right_offset[0])
        rr_startPoint = [math.cos(rr_angle)*startDistance,math.sin(rr_angle)*startDistance,0]


        print "fl_offset:", front_left_offset
        self.robot.move_leg_to_point('front_left',  *(fl_rest + front_left_offset - fl_startPoint))
        self.robot.move_leg_to_point('front_right', *(fr_rest + front_right_offset - fr_startPoint))
        self.robot.move_leg_to_point('rear_left',  *(rl_rest + rear_left_offset - rl_startPoint))
        self.robot.move_leg_to_point('rear_right', *(rr_rest + rear_right_offset - rr_startPoint))

    def reset(self):
        pass