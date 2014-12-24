import SimpleCV as scv
from vision.calibrator import Calibrator
from vision.calibrator_alt import AltCalibrator
from vision.detection import Detector

video = scv.Camera()

calibrator = Calibrator(video)
# calibrator = AltCalibrator(video)

calibrator.calibrate()

detector = Detector(video)
display = scv.Display()
while display.isNotDone():
    img = video.getImage()
    detector.detectAndTrackOnFrame(img)
    detector.tracker.drawPath(img)
    img.save(display)
    if display.mouseLeft:
        display.done = True
display.quit()

print detector.tracker.getReadableSymbolVector()