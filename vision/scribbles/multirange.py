import SimpleCV as scv
import cv2
from SimpleCV.base import np

video = scv.Camera()

ranges = [
    ([34, 25, 51], [38, 255, 255]),
    ([72, 0, 137], [85, 23, 182]),
    ([45, 3, 110], [67, 31, 162]),
    ([21, 23, 0], [49, 237, 67])
]

display = scv.Display()

while display.isNotDone():
    img = video.getImage()
    img = img.toHSV()


    thres = []
    for range in ranges:
        thres.append(cv2.inRange(img.getNumpyCv2(), np.array(range[0]), np.array(range[1])))

    res = reduce(lambda x, y: cv2.add(x, y), thres)

    #simg = scv.Image(thres, cv2image=False)
    simg = scv.Image(res.transpose(1,0))

    #simg = simg.morphOpen()
    simg = simg.morphClose()
    simg = simg.morphOpen()

    blobs = simg.findBlobs()
    if blobs:
        circles = blobs.filter([b.isCircle(0.4) for b in blobs])
        if circles:
        #    for c in circles:
        #        dist.drawCircle((c.x, c.y), c.radius(), scv.Color.RED, -1)
            simg.drawCircle((circles[-1].x, circles[-1].y), circles[-1].radius(),
                           scv.Color.RED, -1)

    simg.save(display)
    if display.mouseRight:
        display.done = True