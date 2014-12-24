import SimpleCV as scv
import cv2
from SimpleCV.base import np


video = scv.Camera()

#markerColor = (99, 105, 79)
markerColor = (95.0, 105.0, 80.0)


def track(markerColor = (95, 105, 80)):
    display = scv.Display()
    while display.isNotDone():
        img = video.getImage()

        #dist = img.colorDistance(markerColor).invert()
        dist = img.hueDistance(markerColor, 20, 20).invert()
        #dist = dist.dilate(1)
        #dist = dist.stretch(230, 255)
        dist = dist.threshold(240)

#mask = cv2.inRange(hsv, np.array(lower), np.array(upper))

        dist = dist.morphClose()
        dist = dist.morphOpen()

        # blobs = dist.findBlobs()
        # if blobs:
        #     circles = blobs.filter([b.isCircle(0.4) for b in blobs])
        #     if circles:
        #     #    for c in circles:
        #     #        dist.drawCircle((c.x, c.y), c.radius(), scv.Color.RED, -1)
        #         dist.drawCircle((circles[-1].x, circles[-1].y), circles[-1].radius(),
        #                        scv.Color.RED, -1)

        circles = dist.findCircle()
        if circles:
            circles.show(color=scv.Color.RED, width=-1)

        dist.save(display)

        if display.mouseRight:
            display.done = True
    display.quit()

def calibrate():
    display = scv.Display()
    while display.isNotDone():
        img = video.getImage()
        try:
            img2 = img.copy()
            img2.drawCircle((img2.width/2, img2.height/2), 5, scv.Color.RED, -1)
            img2.save(display)
        except KeyboardInterrupt:
            display.done = True
            #break
        if display.mouseRight:
            display.done = True
    display.quit()
    pixel = img.getPixel(img.width/2, img.height/2)
    print pixel
    return pixel

track(calibrate())