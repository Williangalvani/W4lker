from robot import controller

from robot.robotInterfaces.virtualRobot.virtualRobot import VirtualRobot
from robot.robotInterfaces.realRobot.realRobot import RealRobot

robot1 = VirtualRobot()
try:
    robot2 = RealRobot()
except:
    robot2 = None
controller1 = controller.RobotController(robot1)
controller1.start()

controller2 = None
if robot2:
    controller2 = controller.RobotController(robot2)
    controller2.start()

print("script ready!")

def run():
    global controller1, controller2
    controller1.iterate()

    if robot2:
        controller2.iterate()