import SimpleCV as scv
import json
import cv2
from SimpleCV.base import np
from vision.detection import transformFrame

CONFIG_FILE = "./config.json"

class Calibrator:

    def __init__(self, video = None):
        self.twoRange = False
        self.pixel = None
        self.video = video if video else scv.Camera()

    def calibrate(self):
        ok = False
        while not ok:
            self.capturePixel()
            self.calculateRanges()
            ok = self.askUser()
        self.saveConfig()


    def capturePixel(self):
        display = scv.Display()
        while display.isNotDone():
            img = self.video.getImage()
            img2 = img.copy()
            img2.drawCircle((img2.width/2, img2.height/2), 5, scv.Color.RED, -1)
            img2.save(display)
            if display.mouseLeft:
                display.done = True
        display.quit()
        pixel = img.toHSV().getPixel(img.width/2, img.height/2)
        self.pixel = pixel


    def askUser(self):
        ok = False
        display = scv.Display()
        while display.isNotDone():
            img = self.video.getImage()
            img = transformFrame(img, self.twoRange, self.strict_ranges, self.loose_ranges)
            img.save(display)
            if display.mouseMiddle:
                self.twoRange = not self.twoRange
            if display.mouseLeft:
                ok = True
                display.done = True
            if display.mouseRight:
                display.done = True
        display.quit()
        return ok

    def saveConfig(self):
        config = {'twoRange': self.twoRange, 'loose_ranges': self.loose_ranges, 'strict_ranges': self.strict_ranges}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)

    def calculateRanges(self):
        strict = {
            "hmin": self.pixel[0] - 10,
            'hmax': self.pixel[0] + 10,
            'smin': self.pixel[1] - 50,
            'smax': self.pixel[1] + 50,
            'vmin': self.pixel[2] - 50,
            'vmax': self.pixel[2] + 50
        }
        loose = {
            "hmin": self.pixel[0] - 10,
            'hmax': self.pixel[0] + 10,
            'smin': self.pixel[1] - 100,
            'smax': self.pixel[1] + 100,
            'vmin': self.pixel[2] - 100,
            'vmax': self.pixel[2] + 100
        }
        self.strict_ranges = [
            (strict['hmin'], strict['smin'], strict['vmin']),
            (strict['hmax'], strict['smax'], strict['vmax'])
        ]
        self.loose_ranges = [
            (loose['hmin'], loose['smin'], loose['vmin']),
            (loose['hmax'], loose['smax'], loose['vmax'])
        ]