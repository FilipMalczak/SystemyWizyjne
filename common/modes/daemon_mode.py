# this one should work with pygame window, the display one. depending on given cli
# arg it should display preview or only text
from time import time
import SimpleCV as scv
from common.context import recognizer
from common.action_executor import ActionExecutor
from common.config import d_time, big_d_time
from vision.detection import Detector
from common.beeper import beep


label1 = {True: "ON", False: "OFF"}
no_disp_res = (500,200)

class DaemonMode:

    def __init__(self, display=False, stanby_mode = False, path=None, video=None):
        self.executor = ActionExecutor(path)
        self.display = display
        self.recognizer = recognizer
        self.video = video if video else scv.Camera()
        self.detector = Detector(self.video)
        self.standby_mode = stanby_mode

    def run(self):
        if self.display:
            display = scv.Display()
        else:
            display = scv.Display(resolution=no_disp_res)
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
                if self.display:
                    self.detector.tracker.drawPath(img)
                if self.standby_mode:
                    if self.detector.tracker.isStill():
                        if time() - moment > big_d_time:
                            beep()
                            self.endTracking()
                            tracking = False
                            moment = time()
            if self.display:
                frame = img
            else:
                frame = scv.Image(no_disp_res)
            pos = 0
            frame.drawText("Tracking: " + label1[tracking], 0, pos, fontsize=30)
            pos += 40
            if self.standby_mode:
                frame.drawText("Standby: " + label1[standby], 0, pos, fontsize=30)
                pos += 40
            frame.drawText("LMB to start/stop tracking, RMB to exit", 0, pos, fontsize=30)
            pos += 40
            frame.drawText("MMB to abort current gesture", 0, pos, fontsize=30)
            frame.save(display)
            if display.mouseLeft:
                if time() - moment > d_time:
                    if tracking:
                        self.endTracking()
                        tracking = False
                    else:
                        tracking = True
                    moment = time()
            if display.mouseMiddle:
                if tracking:
                    self.detector.resetTracker()
                    tracking = False
            if display.mouseRight:
                display.done = True

    def endTracking(self):
        recognized = self.recognizer.recognize(self.detector.tracker.getSymbolVector())
        if recognized[0]:
            self.executor.execute(recognized[0][0])
        else:
            print "No gesture recognized"
        self.detector.resetTracker()