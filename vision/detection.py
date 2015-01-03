import SimpleCV as scv
import cv2
import json
import time
from SimpleCV.base import np
from common import dirs
from vision.tracker import Tracker

CONFIG_FILE = dirs.vision_config

def transformFrame(img, twoRange, strict_ranges, loose_ranges):
    img = img.toHSV()
    res = cv2.inRange(img.getNumpyCv2(), np.array(strict_ranges[0]), np.array(strict_ranges[1]))
    simg = scv.Image(res.transpose(1, 0))

    if twoRange:
        blobs = simg.findBlobs()
        if blobs:
            x = int(blobs[0].minRectX() - 20)
            if x < 0:
                x = 0
            y = int(blobs[0].minRectY() - 20)
            if y < 0:
                y = 0
            w = int(blobs[0].minRectWidth() + 40)
            h = int(blobs[0].minRectHeight() + 40)
            bb = (x, y, w, h)
            cropped = img.crop(bb)
            loose_res = cv2.inRange(cropped.getNumpyCv2(), np.array(loose_ranges[0]), np.array(loose_ranges[1]))

            for i in range(y, y+cropped.height):
                for j in range(x, x+cropped.width):
                    temp = loose_res[i - y, j - x]
                    res[i, j] = temp
            simg = scv.Image(res.transpose(1, 0))

    simg = simg.morphClose()
    simg = simg.morphOpen()
    return simg

class Detector:

    def __init__(self, video = None):
        self.readConfig()
        self.video = video if video else scv.Camera()
        self.tracker = Tracker()


    def detectAndTrack(self):
        pass    #we need to deal with running this as long as key is pressed, no idea how

    def detectAndTrackForDuration(self, duration=5):
        startTime = time.time()
        while time.time() - startTime < duration:
            frame = self.video.getImage().flipHorizontal()
            self.detectAndTrackOnFrame(frame)


    def detectAndTrackOnFrame(self, frame):
        frame = transformFrame(frame, self.twoRange, self.strict_ranges, self.loose_ranges)
        blobs = frame.findBlobs()
        if blobs:
            circles = blobs.filter([b.isCircle(0.6) for b in blobs])
            if circles:
                self.tracker.newBlob(circles[-1])

    def readConfig(self):
        with open(CONFIG_FILE, 'r') as f:
            loaded = json.load(f)
            self.twoRange = loaded[u'twoRange']
            self.loose_ranges = loaded[u'loose_ranges']
            self.strict_ranges = loaded[u'strict_ranges']

    def resetTracker(self):
        self.tracker = Tracker()
