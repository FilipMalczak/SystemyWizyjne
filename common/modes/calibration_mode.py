import SimpleCV as scv
from vision.calibrator import Calibrator


class CalibrationMode:

    def __init__(self, video=None):
        self.video = video if video else scv.Camera()
        self.calibrator = Calibrator(self.video)

    def run(self):
        self.calibrator.calibrate()