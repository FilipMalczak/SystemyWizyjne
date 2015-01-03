# this one should work with pygame window, the display one. depending on given cli
# arg it should display preview or only text
from time import time
import SimpleCV as scv
from common.context import recognizer
from common.action_executor import ActionExecutor
from common.config import d_time
from vision.detection import Detector


label1 = {True: "ON", False: "OFF"}

class DaemonMode:

    def __init__(self, display=False, path=None, video=None):
        self.executor = ActionExecutor(path)
        self.display = display
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
                if self.display:
                    self.detector.tracker.drawPath(img)
            if self.display:
                frame = img
            else:
                frame = scv.Image((500,200))
            frame.drawText(label1[tracking], 0, 0, fontsize=30)
            frame.drawText("LMB to start/stop tracking, RMB to exit", 0, 40, fontsize=30)
            frame.save(display)
            if display.mouseLeft:
                if time() - moment > d_time:
                    if tracking:
                        recognized = self.recognizer.recognize(self.detector.tracker.getSymbolVector())
                        if recognized[0]:
                            self.executor.execute(recognized[0][0])
                        else:
                            print "No gesture recognized"
                        self.detector.resetTracker()
                        tracking = False
                    else:
                        tracking = True
                    moment = time()
            if display.mouseRight:
                display.done = True