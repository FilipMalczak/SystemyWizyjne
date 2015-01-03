import SimpleCV as scv
from common.context import recognizer
from vision.detection import Detector
from time import time
from common.config import d_time

label1 = {True: "ON", False: "OFF"}

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
            img = self.video.getImage().flipHorizontal()
            if tracking:
                self.detector.detectAndTrackOnFrame(img)
                self.detector.tracker.drawPath(img)
            img.drawText(label1[tracking], 0, 0, fontsize=30)
            img.drawText("LMB to start/stop tracking, RMB to exit", 0, 40, fontsize=30)
            img.save(display)
            if display.mouseLeft:
                if time() - moment > d_time:
                    if tracking:
                        recognized = recognizer.recognize(self.detector.tracker.getSymbolVector())
                        print recognized[0][0] if recognized[0] else None
                        self.detector.resetTracker()
                        tracking = False
                    else:
                        tracking = True
                    moment = time()
            if display.mouseRight:
                display.done = True
        display.quit()