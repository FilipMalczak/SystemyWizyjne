import math

class Tracker:

    SYMBOLS = {1: 'E', 2: 'NE', 3: 'N', 4: 'NW', 5: 'W', 6: 'SW', 7: 'S', 8: 'SE'}

    def __init__(self):
        self.history = []

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
        else:
            d = self.distance(curr, self.previous)
            radius = blob.radius()
            if d > radius/2 and d < radius*5:
                self.history.append(curr)
        return symbol

    def getSymbolVector(self):
        res = []
        for i in range(len(self.history)-1):
            res.append(self.getSymbolFromPoints(self.history[i+1], self.history[i]))
        return res

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

