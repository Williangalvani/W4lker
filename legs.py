
from robot import Robot

from robot.robotInterfaces.virtualRobot.virtualRobot import VirtualRobot

robot = VirtualRobot()
controller = Robot.RobotController(robot)
controller.start()




def run():
    global controller
    controller.iterate()