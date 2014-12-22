import SimpleCV as scv
from vision.detection import Detector
from time import time
from common.config import d_time, recognizer


class TestMode:

    def __init__(self, video =None):
        self.recognizer = recognizer
        self.video = video if video else scv.Camera()
        self.detector = Detector(self.video)

    def run(self):
        display = scv.Display()
        tracking = False


        moment = time()
        while display.isNotDone():
            img = self.video.getImage()
            if tracking:
                self.detector.detectAndTrackOnFrame(img)
                self.detector.tracker.drawPath(img)
            img.drawText(str(tracking), 0, 0, fontsize=30)
            img.save(display)
            if display.mouseLeft:
                if time() - moment > d_time:
                    if tracking:
                        recognized = recognizer.recognize(self.detector.tracker.getSymbolVector())
                        print recognized
                        self.detector.resetTracker()
                        tracking = False
                    else:
                        tracking = True
                    moment = time()
            if display.mouseRight:
                display.done = True
        display.quit()