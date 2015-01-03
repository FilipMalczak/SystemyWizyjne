import SimpleCV as scv
import json
# from SimpleCV.Shell import plot
import cv2
from SimpleCV.base import np
from common import dirs
from vision.detection import transformFrame

CONFIG_FILE = dirs.vision_config

class AltCalibrator:

    radius = 50
    x = None
    y = None

    def __init__(self, video = None):
        self.twoRange = False
        self.pixel = None
        self.video = video if video else scv.Camera()

    def calibrate(self):
        ok = False
        while not ok:
            self.captureHistogram()
            self.calculateRanges()
            ok = self.askUser()
        self.saveConfig()

    def captureHistogram(self):
        img = self.video.getImage().flipHorizontal()
        self.x = img.width/2
        self.y = img.height/2
        display = scv.Display()
        while display.isNotDone():
            img = self.video.getImage().flipHorizontal()
            img2 = img.copy()
            img2.drawCircle((self.x, self.y), self.radius, scv.Color.RED, 2)
            img2.save(display)
            if display.mouseWheelUp:
                self.radius += 5
            if display.mouseWheelDown:
                self.radius -= 5
            if display.mouseLeft:
                display.done = True
        display.quit()
        cropped = img.crop(self.x, self.y, self.radius*2, self.radius*2, True)

        # print cropped.huePeaks()
        # plot(cropped.hueHistogram())
        cropped = cropped.toHSV()

        hmax = self._findMaxBin(np.histogram(cropped.getNumpy()[:,:,2], 179)[0])
        # smax = self._findMaxBin(np.histogram(cropped.getNumpy()[:,2,:], 255)[0])
        # vmax = self._findMaxBin(np.histogram(cropped.getNumpy()[2,:,:], 255)[0])
        pix = cropped.getPixel(cropped.width/2, cropped.height/2)
        smax = pix[1]
        vmax = pix[2]
        self.pixel = (hmax, smax, vmax)
        # self.pixel = (hmax, 97, 160)
        print self.pixel

    def _findMaxBin(self, histogram):
        max = histogram[0]
        maxi = 0
        for i, val in enumerate(histogram):
            if val > max:
                max = val
                maxi = i
        return maxi

    def askUser(self):
        ok = False
        display = scv.Display()
        while display.isNotDone():
            img = self.video.getImage().flipHorizontal()
            img = transformFrame(img, self.twoRange, self.strict_ranges, self.loose_ranges)
            mode = "double" if self.twoRange else "single"
            img.drawText("Mode: " + mode, 0, 0, fontsize=30)
            img.drawText("LMB to accept, MMB to change mode, RMB to discard", 0, 40, fontsize=30)
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

if __name__ == '__main__':
    calibrator = AltCalibrator()
    calibrator.calibrate()