from time import time
import SimpleCV as scv
from common.config import d_time, min_examples
from common.context import recognizer
from vision.detection import Detector
import toolbox.EasyGame as dialog

label1 = {True: "ON", False: "OFF"}

class LearningMode:

    def __init__(self, name, new=False, video=None):
        self.recognizer = recognizer
        self.video = video if video else scv.Camera()
        self.detector = Detector(self.video)
        self.name = name
        self.examples = []
        self.new = new

    def run(self):
        abort = False
        display = scv.Display()
        tracking = False
        moment = time()
        while display.isNotDone():
            img = self.video.getImage()
            if tracking:
                self.detector.detectAndTrackOnFrame(img)
                self.detector.tracker.drawPath(img)
            img.drawText(label1[tracking], 0, 0, fontsize=30)
            img.save(display)
            if display.mouseLeft:
                if time() - moment > d_time:
                    if tracking:
                        self.examples.append(self.detector.tracker.getSymbolVector())
                        self.detector.resetTracker()
                        tracking = False
                    else:
                        tracking = True
                    moment = time()
            if display.mouseMiddle:
                if tracking:
                    self.detector.resetTracker()
                    tracking = False
            if display.mouseRight:
                if self.new and len(self.examples) < min_examples:
                    res = dialog.confirm(self._get_dialog_label(), 'Warning', mode=2)
                    abort = res
                else:
                    res = True
                display.done = res
        display.quit()
        if not abort:
            recognizer.learn(self.name, *self.examples)
            recognizer.dump()

    def _get_dialog_label(self):
        return "When teaching a new gesture you need to provide " + str(min_examples) +\
            " examples, but you only provided " + str(len(self.examples)) +". Do you" +\
            " wish to abort and lose those changes?"
