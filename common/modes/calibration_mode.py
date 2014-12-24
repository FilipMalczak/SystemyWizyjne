import SimpleCV as scv
from vision.calibrator import Calibrator
from vision.calibrator_alt import AltCalibrator


class CalibrationMode:

    def __init__(self, histogram=False, video=None):
        self.video = video if video else scv.Camera()
        if histogram:
            self.calibrator = AltCalibrator(self.video)
        else:
            self.calibrator = Calibrator(self.video)

    def run(self):
        self.calibrator.calibrate()