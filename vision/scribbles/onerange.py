import SimpleCV as scv
import cv2
from SimpleCV.base import np
from vision.scribbles import Trackbars



tbars = Trackbars()
ranges = tbars.getFromUser()

video = scv.Camera()
display = scv.Display()

while display.isNotDone():
    img = video.getImage()
    img = img.toHSV()


    res = cv2.inRange(img.getNumpyCv2(), np.array(range[0]), np.array(range[1]))

    #simg = scv.Image(thres, cv2image=False)
    simg = scv.Image(res.transpose(1,0))

    #simg = simg.morphOpen()
    simg = simg.morphClose()
    simg = simg.morphOpen()

    #blobs = simg.findBlobs()
    #if blobs:
    #    circles = blobs.filter([b.isCircle(0.4) for b in blobs])
    #    if circles:
    #    #    for c in circles:
    #    #        dist.drawCircle((c.x, c.y), c.radius(), scv.Color.RED, -1)
    #        simg.drawCircle((circles[-1].x, circles[-1].y), circles[-1].radius(),
    #                       scv.Color.RED, -1)

    circles = simg.findCircle()
    if circles:
        circles.show(color=scv.Color.RED, width=-1)

    simg.save(display)
    if display.mouseRight:
        display.done = True