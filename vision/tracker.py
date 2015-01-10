import math
import SimpleCV as scv
from vision.postprocessing import postprocess
from common.config import still_frames



class Tracker:

    SYMBOLS = {1: 'E', 2: 'NE', 3: 'N', 4: 'NW', 5: 'W', 6: 'SW', 7: 'S', 8: 'SE'}

    def __init__(self, observation_size = 100):
        self.history = []
        self.observation_size = observation_size
        self.counter = 0

    @property
    def previous(self):
        return self.history[-1] if self.history else None

    def newBlob(self, blob):
        '''
        Invoke this and pass newly detected blob. Tracker will compare the blob with history.
        If it's suspected to be new marker position and it satisfies movement rules
        it is then added to the history
        :param blob: newly detected blob
        :return: None
        '''
        symbol = None
        curr = (blob.x, blob.y)
        if self.previous is None:
            self.history.append(curr)
            self.counter = 0
        else:
            d = self.distance(curr, self.previous)
            radius = blob.radius()
            if d > radius/1.5 and d < radius*5:
                self.history.append(curr)
                self.counter = 0
            else:
                self.counter += 1
        return symbol

    def isStill(self):
        return self.counter >= still_frames

    def forgetHistory(self):
        self.history = [self.history[-1]] if self.history else []

    def drawPath(self, img):
        if len(self.history) > 1:
            for i in range(len(self.history)-1):
                img.drawLine(self.history[i], self.history[i+1], scv.Color.RED, 2)

    def getSymbolVector(self):
        # res = []
        # for i in range(len(self.history)-1):
        #     res.append(self.getSymbolFromPoints(self.history[i+1], self.history[i]))
        if len(self.history)>1:
            observations = postprocess(self.history, self.observation_size)
            return map(lambda x: self.getSymbolFromPoints(*x), zip(observations[:-1], observations[1:]))
        return []

    def getReadableSymbolVector(self):
        vector = self.getSymbolVector()
        return [self.SYMBOLS[symbol] for symbol in vector]

    def distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def getSymbolFromPoints(self, p1, p2):
        return self.getSymbol(self.getAngle(p1, p2))

    def getAngle(self, p1, p2):
        xDiff = p2[0] - p1[0]
        yDiff = p2[1] - p1[1]
        return math.atan2(yDiff, xDiff)

    def getSymbol(self, angle):
        angle = angle * 8 / math.pi
        if angle >= 7 or angle <= -7:
            return 1
        if angle >= 5:
            return 2
        if angle >= 3:
            return 3
        if angle >= 1:
            return 4
        if angle >= -1:
            return 5
        if angle >= -3:
            return 6
        if angle >= -5:
            return 7
        return 8

