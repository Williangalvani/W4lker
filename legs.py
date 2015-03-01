from robot import controller

from robot.robotInterfaces.virtualRobot.virtualRobot import VirtualRobot
from robot.robotInterfaces.realRobot.realRobot import RealRobot

robot1 = VirtualRobot()
robot2 = RealRobot()
controller1 = controller.RobotController(robot1)
controller1.start()

controller2 = controller.RobotController(robot2)
controller2.start()

print("script ready!")

def run():
    global controller1, controller2
    controller1.iterate()
    controller2.iterate()