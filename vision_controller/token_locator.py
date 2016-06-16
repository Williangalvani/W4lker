# !/usr/bin/env python


import cv2
import numpy as np

from itertools import tee, izip
import binascii
import math
import traceback
import time


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return izip(a, b)


def nothing(kargs=[]):
    pass


class QrFinder():
    cap = None
    img = None

    def try_to_decode(self, candidate, source, target):
        epsilon = 0.01 * cv2.arcLength(candidate, True)
        approx = cv2.approxPolyDP(candidate, epsilon, True)

        # makes sure epsilon gives us a square
        while len(approx) > 4:
            epsilon *= 1.01
            approx = cv2.approxPolyDP(candidate, epsilon, True)

        ### draw on screen
        for a, b in pairwise(approx):
            cv2.line(target, tuple(a[0]), tuple(b[0]), (0, 0, 255), 3)
        cv2.line(target, tuple(approx[-1][0]), tuple(approx[0][0]), (0, 0, 255), 3)


        ## detect center of mass, and each corner before decoding
        center = sum(approx) / 4
        self.center = center
        topleft = None
        topright = None
        bottomleft = None
        bottomright = None

        for i in approx:
            if i[0][0] < center[0][0] and i[0][1] < center[0][1]:
                topleft = i
            elif i[0][0] > center[0][0] and i[0][1] < center[0][1]:
                topright = i
            elif i[0][0] < center[0][0] and i[0][1] > center[0][1]:
                bottomleft = i
            elif i[0][0] > center[0][0] and i[0][1] > center[0][1]:
                bottomright = i


        if topleft is None or topright is None or bottomleft is None or bottomright is None:
            return None

        targetperspective = np.float32(
            [[[0, 0]], [[100, 0]], [[100, 100]], [[0, 100]]])  ### use points to calculate perspective matrix
        source_perspective = np.float32([topleft, topright, bottomright, bottomleft])

        uncorrected_angle = math.atan2(topleft[0][1]-bottomleft[0][1],topleft[0][0]-bottomleft[0][0])

        matrix = cv2.getPerspectiveTransform(source_perspective, targetperspective)
        cv2.warpPerspective(source, matrix, (100, 100),
                            self.corrected)  ### transforms the image to make the token planas


        gridsize = 3
        step = 100 / (gridsize + 2)
        min, max = cv2.minMaxLoc(self.corrected)[:2]
        avg = (min + max) / 2
        freeborder = 1


        topleftpos = (1 * step,1 * step)
        topleft = 1 if self.corrected[topleftpos[0]][topleftpos[1]] < avg else 0
        cv2.circle(self.corrected, topleftpos, 1, (255, 0, 0), 2)

        toprightpos = ((gridsize+freeborder)*step,freeborder * step)
        topright = 1 if self.corrected[toprightpos[1]][toprightpos[0]] < avg else 0
        cv2.circle(self.corrected, toprightpos, 1, (255, 0, 0), 2)

        bottomrightpos = ((gridsize + freeborder) * step, (gridsize + freeborder) * step)
        bottomright = 1 if self.corrected[bottomrightpos[0]][bottomrightpos[1]] < avg else 0
        cv2.circle(self.corrected, bottomrightpos, 1, (255, 0, 0), 2)

        bottomleftpos = (freeborder * step, (gridsize+freeborder)*step)
        bottomleft = 1 if self.corrected[bottomleftpos[1]][bottomleftpos[0]] < avg else 0
        cv2.circle(self.corrected, bottomleftpos, 1, (255, 0, 0), 2)

        cv2.namedWindow('corrected')
        cv2.imshow('corrected', self.corrected)

        ### abort if wrong number of markers
        if topleft + topright + bottomright + bottomleft != 3:
            #print "bad markers!"
            return None

        ### detects need of rotation
        angle = 0
        if not topleft:
            angle = 180
        elif not topright:
            angle = 270
        elif not bottomleft:
            angle = 90

        rotation = cv2.getRotationMatrix2D((50, 50), angle, 1.0)
        self.corrected = cv2.warpAffine(self.corrected, rotation, (100, 100))


        self.finalAngle = angle + math.degrees(uncorrected_angle)
        print "angle: ", self.finalAngle
        ### only gets here if the number of markers is right

        cv2.namedWindow('corrected')
        cv2.imshow('corrected', self.corrected)

        return True

    def clickCallback(self,event, x, y, flags,param):
        if event == cv2.EVENT_LBUTTONUP:
            self.target = (x,y)


    def __init__(self,standalone=False):
        self.cap = None
        self.corrected = np.zeros((100, 100), np.uint8)  # image with corrected perspective
        cv2.namedWindow('contours')
        cv2.setMouseCallback('contours',self.clickCallback)
        self.target = None
        self.center = None
        self.finalAngle = None
        self.standalone = standalone
        if standalone:

            try:
                self.cap = cv2.VideoCapture(0)  # open first camera?
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280);
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768);
            except:
                print "could not open camera!"

            cv2.namedWindow('edge')

            while True:
                flag, self.img = self.cap.read()  # read a frame
                self.find_code(self.img)
            cv2.destroyAllWindows()




    def find_code(self, img):
        h, w = img.shape[:2]

        if self.standalone:
            gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
        thrs1 = 2000#cv2.getTrackbarPos('thrs1', 'edge')
        thrs2 = 4000#cv2.getTrackbarPos('thrs2', 'edge')
        edge = cv2.Canny(gray, thrs1, thrs2, apertureSize=5)
        vis = img.copy()
        vis /= 2
        vis[edge != 0] = 0
        #cv2.imshow('edge', vis)

        vis2 = np.zeros((h, w), np.uint8)
        vis2[edge != 0] = 255

        _, contours0, hierarchy = cv2.findContours(vis2.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in contours0]

        selected = []
        # **[Next, Previous, First_Child, Parent]**
        if hierarchy is not None:
            for c, h in zip(contours, hierarchy[0]):
                if h[0] == -1 and h[1] == -1:
                    kid = h[2]
                    if kid != -1:
                        kidh = hierarchy[0][kid]
                        if kidh[0] == -1 and kidh[1] == -1:  ### only checking for nested circles, without brothers
                            selected.append(c)

            cv2.drawContours(vis, selected, -1, (255, 0, 0), 2, cv2.LINE_AA)
            for candidate in selected:
                try:
                    if self.try_to_decode(candidate, gray, vis):
                        break
                except Exception, e:

                    traceback.print_exc()
                    print e

            if self.center is not None and self.finalAngle is not None:
                p2 = (int(self.center[0][0]+math.cos(math.radians(self.finalAngle))*150),
                      int(self.center[0][1]+math.sin(math.radians(self.finalAngle))*150))
                cv2.line(vis, tuple(self.center[0]), tuple(p2), 255,3)

        if self.target is not None:
            cv2.circle(vis, self.target, 5, 255, 2)


        cv2.imshow('contours', vis)

        ch = cv2.waitKey(5) & 0xFF
        if ch == 27:
            exit()

if __name__ == '__main__':


    cv2.destroyAllWindows()
    finder = QrFinder(True)
