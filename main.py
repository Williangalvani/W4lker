import time
from robot import legscontroller
# from robot.robotInterfaces.virtualRobot.virtualRobot import VirtualRobot
from robot.robotInterfaces.virtualRobot.virtualRobotVrep import VirtualRobotVrep as VirtualRobot
from robot.robotInterfaces.realRobot.realRobot import RealRobot
from PyQt4 import QtCore, QtGui, uic
from vision_controller.viewController import ViewController
import sys

robot1 = None
try:
    robot1 = VirtualRobot()
except:
    print "no virtual robot" \
          ""
try:
    robot2 = RealRobot()
except Exception, e:
    print "could not connect to real robot, error: ", e
    robot2 = None

controllers = []
if robot1 is not None:
    controller1 = legscontroller.RobotController(robot1)
#viewcontroller = ViewController(controller1, robot1)
    controllers.append(controller1)


if robot2 is not None:
    controller2 = legscontroller.RobotController(robot2)
    controllers.append(controller2)

print("script ready!")
for controller in controllers:
    controller.start()



from gui.manualinterface import MyWindowClass

app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(controllers=controllers)
myWindow.show()
app.exec_()
