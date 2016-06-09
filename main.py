import time
from robot import legscontroller
# from robot.robotInterfaces.virtualRobot.virtualRobot import VirtualRobot
from robot.robotInterfaces.virtualRobot.virtualRobotVrep import VirtualRobotVrep as VirtualRobot
from robot.robotInterfaces.realRobot.realRobot import RealRobot
from vision_controller.viewController import ViewController


robot1 = VirtualRobot()

try:
    robot2 = RealRobot()
except Exception, e:
    print "could not connect to real robot, error: ", e
    robot2 = None


controller1 = legscontroller.RobotController(robot1)
viewcontroller = ViewController(controller1, robot1)


controller1.start()


controller2 = None

if robot2:
    controller2 = legscontroller.RobotController(robot2)
    controller2.start()

print("script ready!")


def run():
    global controller1, controller2
    controller1.iterate()
    # time.sleep(0.02)
    if robot2:
        controller2.iterate()

if __name__ == "__main__":
    while(1):
        run()