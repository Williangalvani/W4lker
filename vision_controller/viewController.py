
import numpy as np
import cv2
import time
from token_locator import QrFinder

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
            #print "Vision system took ", time.time() - start

