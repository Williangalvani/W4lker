
import numpy as np
import cv2
import time
from token_locator import QrFinder
from math import radians, sin, cos

class ViewController():
    def __init__(self, controller, robot):
        self.controller = controller
        self.robot = robot
        self.controller.camera_handler = self.handle_image

        self.token_locator = QrFinder()



    def handle_image(self,img):
        start= time.time()
        if img is not None:
            #cv2.imshow("camera", img)
            cv2.waitKey(1)

            self.token_locator.find_code(img)
            target, center, angle = self.token_locator.target, \
                                    self.token_locator.center, \
                                    self.token_locator.finalAngle

            if center is not None and target is not None and angle is not None:
                ex = target[0] - center[0][0]
                ey = target[1] - center[0][1]
                angle = radians(angle)
                rex = cos(angle)*ex + sin(angle)*ey
                rey = -sin(angle)*ex + cos(angle)*ey
                x = max(min(10*rex, 100), -100)
                y = max(min(10*rey, 100), -100)

                self.controller.dy = y
                self.controller.dx = x

                print x,y
        print "image handling took", time.time() - start
