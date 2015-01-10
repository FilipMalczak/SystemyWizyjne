import SimpleCV as scv
from common.context import recognizer
from vision.detection import Detector
from time import time
from common.config import d_time, big_d_time
from common.beeper import beep

label1 = {True: "ON", False: "OFF"}

class TestMode:

    def __init__(self, standby_mode=False, video =None):
        self.recognizer = recognizer
        self.video = video if video else scv.Camera()
        self.detector = Detector(self.video)
        self.standby_mode = standby_mode

    def run(self):
        display = scv.Display()
        tracking = False
        standby = False


        moment = time()
        while display.isNotDone():
            img = self.video.getImage().flipHorizontal()
            if self.standby_mode:
                if self.detector.isTrackerClose(img) and not standby:
                    if time() - moment > big_d_time:
                        standby = True
                        beep()
                        moment = time()
                if standby:
                    self.detector.detectAndTrackOnFrame(img)
                    if self.detector.tracker.isStill():
                        if time() - moment > big_d_time:
                            standby = False
                            self.detector.tracker.forgetHistory()
                            tracking = True
                            beep()
                            moment = time()
            if tracking:
                self.detector.detectAndTrackOnFrame(img)
                self.detector.tracker.drawPath(img)
                if self.standby_mode:
                    if self.detector.tracker.isStill():
                        if time() - moment > big_d_time:
                            beep()
                            self.endTracking()
                            tracking = False
                            moment = time()

            pos = 0
            img.drawText("Tracking: " + label1[tracking], 0, pos, fontsize=30)
            pos += 40
            if self.standby_mode:
                img.drawText("Standby: " + label1[standby], 0, pos, fontsize=30)
                pos += 40
            img.drawText("LMB to start/stop tracking, RMB to exit", 0, pos, fontsize=30)
            img.save(display)

            if display.mouseLeft:
                if time() - moment > d_time:
                    if tracking:
                        self.endTracking()
                        tracking = False
                    else:
                        tracking = True
                    moment = time()
            if display.mouseRight:
                display.done = True
        display.quit()

    def endTracking(self):
        recognized = self.recognizer.recognize(self.detector.tracker.getSymbolVector())
        print recognized[0][0] if recognized[0] else None
        self.detector.resetTracker()