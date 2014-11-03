__author__ = 'Krecik'

import cv2
import SimpleCV as scv
from SimpleCV.base import np

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
        #if lower:
        #    self.lower = lower
        #else:
        #    self.lower = ranges[0]
        #
        #if upper:
        #    self.upper = upper
        #else:
        #    self.upper = ranges[0]

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

            #img = img.gaussianBlur((5, 5))

            thres = cv2.inRange(img.getNumpyCv2(), np.array(self.lower), np.array(self.upper))

            simg = scv.Image(thres.transpose(1,0))

            #simg = simg.morphOpen()
            simg = simg.morphClose()
            simg = simg.morphOpen()

            #circles = simg.findCircle(thresh=250)
            #if circles:
            #    circles.show(color=scv.Color.RED, width=1)

            simg.save(display)
            if display.mouseRight:
                display.done = True
        cv2.destroyAllWindows()
        saveRanges(self.lower, self.upper)
        return self.lower, self.upper