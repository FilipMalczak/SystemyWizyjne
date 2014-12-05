import SimpleCV as scv
import json
from SimpleCV.Shell import plot
import cv2
from SimpleCV.base import np
from vision.detection import transformFrame


video = scv.Camera()
img = video.getImage()
x = img.width/2
y = img.height/2
radius = 50

display = scv.Display()
while display.isNotDone():
    img = video.getImage()
    img2 = img.copy()
    img2.drawCircle((x, y), radius, scv.Color.RED, 2)
    img2.save(display)
    if display.mouseLeft:
        display.done = True

display.quit()
cropped = img.crop(x, y, radius*2, radius*2, True)

cropped = cropped

print cropped.huePeaks()

# hist = cropped.hueHistogram()
#
# plot(hist)
#
# hist = np.histogram(cropped.getNumpy()[:,:,2], bins=179)[0]
# plot(hist)
#
# hist = np.histogram(cropped.getNumpy()[:,2,:], bins=255)[0]
# plot(hist)

# np.histogram(self.toHSV().getNumpy()[:,:,2], bins = bins)[0]