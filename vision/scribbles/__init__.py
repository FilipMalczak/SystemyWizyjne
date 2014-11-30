__author__ = 'Krecik'

import cv2
import SimpleCV as scv
from SimpleCV.base import np
import math

def readRanges():
    file = open("range.txt", "r")
    lower = eval(file.readline())
    upper = eval(file.readline())
    file.close()
    return (lower, upper)

def saveRanges(lower, upper):
    file = open("range.txt.", "w")
    file.write(str(lower))
    file.write("\n")
    file.write(str(upper))
    #file.writelines([str(lower), str(upper)])
    file.close()


class Trackbars:
    def __init__(self, lower = None, upper = None):
        ranges = readRanges()

        self.lower = lower if lower else ranges[0]
        self.upper = upper if upper else ranges[1]

    def setHmin(self, value):
        self.lower[0] = value

    def setHmax(self, value):
        self.upper[0] = value

    def setSmin(self, value):
        self.lower[1] = value

    def setSmax(self, value):
        self.upper[1] = value

    def setVmin(self, value):
        self.lower[2] = value

    def setVmax(self, value):
        self.upper[2] = value

    def getFromUser(self):
        video = scv.Camera()

        cv2.namedWindow('config')

        cv2.createTrackbar("Hmin", 'config', self.lower[0], 179, self.setHmin)
        cv2.createTrackbar("Hmax", "config", self.upper[0], 179, self.setHmax)

        cv2.createTrackbar("Smin", 'config', self.lower[1], 255, self.setSmin)
        cv2.createTrackbar("Smax", "config", self.upper[1], 255, self.setSmax)

        cv2.createTrackbar("Vmin", 'config', self.lower[2], 255, self.setVmin)
        cv2.createTrackbar("Vmax", "config", self.upper[2], 255, self.setVmax)


        display = scv.Display()

        while display.isNotDone():
            img = video.getImage()
            img = img.toHSV()


            thres = cv2.inRange(img.getNumpyCv2(), np.array(self.lower), np.array(self.upper))

            simg = scv.Image(thres.transpose(1,0))

            simg = simg.morphClose()
            simg = simg.morphOpen()

            simg.save(display)
            if display.mouseRight:
                display.done = True
        cv2.destroyAllWindows()
        saveRanges(self.lower, self.upper)
        return self.lower, self.upper

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def modifyHistory(blob, history, img):
    curr = (blob.x, blob.y)
    if len(history) != 0:
        d = distance(curr, history[-1])
        radius = blob.radius()
        if d > radius/2 and d < radius*5:
        # if d < img.width/5 and d > img.width/15:
            history.append(curr)
    else:
        history.append(curr)

def drawHistory(history, img):
    if len(history) > 1:
        for i in range(len(history)-1):
            img.drawLine(history[i], history[i+1], scv.Color.RED, 2)

def getSymbolFromPoints(p1, p2):
    return getSymbol(getAngle(p1, p2))

def getAngle(p1, p2):
    xDiff = p2[0] - p1[0]
    yDiff = p2[1] - p1[1]
    return math.atan2(yDiff, xDiff)

def getSymbol(angle):
    angle = angle * 8 / math.pi
    if angle > 7 or angle < -7:
        return 1
    if angle > 5:
        return 2
    if angle > 3:
        return 3
    if angle > 1:
        return 4
    if angle > -1:
        return 5
    if angle > -3:
        return 6
    if angle > -5:
        return 7
    return 8

symbols = {1: 'W', 2: 'NW', 3: 'N', 4: 'NE', 5: 'E', 6: 'SE', 7: 'S', 8: 'SW'}