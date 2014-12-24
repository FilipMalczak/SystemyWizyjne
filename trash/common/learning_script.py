import SimpleCV as scv
from vision.calibrator import Calibrator
from vision.calibrator_alt import AltCalibrator
from vision.detection import Detector
from pattern.recognition import default_recognizer
from time import time


gesture = 'down'
examples = []
d_time = 0.5

recognizer = default_recognizer()
video = scv.Camera()

calibrator = Calibrator(video)
# calibrator = AltCalibrator(video)

calibrator.calibrate()

display = scv.Display()
tracking = False
moment = time()

detector = Detector(video)
while display.isNotDone():
    img = video.getImage()
    if tracking:
        detector.detectAndTrackOnFrame(img)
        detector.tracker.drawPath(img)
    img.drawText(str(tracking), 0, 0, fontsize=30)
    img.save(display)
    if display.mouseLeft:
        if time() - moment > d_time:
            if tracking:
                examples.append(detector.tracker.getSymbolVector())
                detector.resetTracker()
                tracking = False
            else:
                tracking = True
            moment = time()
    if display.mouseRight:
        display.done = True

display.quit()
recognizer.learn(gesture, *examples)
recognizer.dump()