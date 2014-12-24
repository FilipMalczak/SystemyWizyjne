# this one should work with pygame window, the display one. depending on given cli
# arg it should display preview or only text
import SimpleCV as scv

from common.action_executor import ActionExecutor
from common.config import default_recognizer, d_time
from vision.detection import Detector


label1 = {True: "ON", False: "OFF"}

class DaemonMode:

    def __init__(self, display=False, path=None, video=None):
        self.executor = ActionExecutor(path)
        self.display = display
        self.recognizer = default_recognizer()
        self.video = video if video else scv.Camera()
        self.detector = Detector(self.video)

    def run(self):
        display = scv.Display()
        tracking = False
        while display.isNotDone():
            img = self.video.getImage()
            if tracking:
                self.detector.detectAndTrackOnFrame(img)
                if self.display:
                    self.detector.tracker.drawPath(img)
            if self.display:
                frame = img
            else:
                frame = scv.Image((100,100))
            frame.drawText(label1[tracking], 0, 0, fontsize=30)