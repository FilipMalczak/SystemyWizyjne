import SimpleCV as scv
import cv2
from SimpleCV.base import np
from vision.scribbles import modifyHistory, drawHistory
from vision.tracker import Tracker

video = scv.Camera()


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
    pixel = img.toHSV().getPixel(img.width/2, img.height/2)
    print pixel
    return pixel


pixel = calibrate()
hmin = pixel[0] - 10
hmax = pixel[0] + 10
smin = pixel[1] - 50
smax = pixel[1] + 50
vmin = pixel[2] - 50
vmax = pixel[2] + 50
ranges = [
    (hmin, smin, vmin),
    (hmax, smax, vmax)
]
display = scv.Display()
history = []
tracker = Tracker()
while display.isNotDone():
    img = video.getImage()
    img = img.toHSV()


    res = cv2.inRange(img.getNumpyCv2(), np.array(ranges[0]), np.array(ranges[1]))

    simg = scv.Image(res.transpose(1,0))

    simg = simg.morphClose()
    simg = simg.morphOpen()

    #znajdz najwiekszego bloba na masce i on pewnie bedzie pileczka, nowa maska
    #ewentualnie podejscie z dwoma filtrami, jeden "surowy", ma znalezc tylko kawalek pilki
    # a drugi lagodniejszy, ale dolaczamy tlyko to, co przylega do znalezionych
    # powinno rozrosnac znaleziony fragment pilki do calej pilki

    blobs = simg.findBlobs()
    if blobs:
        circles = blobs.filter([b.isCircle(0.6) for b in blobs])
        if circles:
            simg.drawCircle((circles[-1].x, circles[-1].y), circles[-1].radius(),
                            scv.Color.RED, -1)
            modifyHistory(circles[-1], history, simg)
            tracker.newBlob(circles[-1])

    drawHistory(history, simg)

    simg.save(display)
    if display.mouseRight:
        display.done = True

print tracker.getSymbolVector()