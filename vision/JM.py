from vision.calibrator import Calibrator
from vision.detection import Detector

calibrator = Calibrator()
calibrator.calibrate()

detector = Detector()
detector.detectAndTrackForDuration(5)
print detector.tracker.getSymbolVector()
print detector.tracker.getReadableSymbolVector()