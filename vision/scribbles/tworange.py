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
strict = {
    "hmin": pixel[0] - 10,
    'hmax': pixel[0] + 10,
    'smin': pixel[1] - 50,
    'smax': pixel[1] + 50,
    'vmin': pixel[2] - 50,
    'vmax': pixel[2] + 50
}

loose = {
    "hmin": pixel[0] - 10,
    'hmax': pixel[0] + 10,
    'smin': pixel[1] - 100,
    'smax': pixel[1] + 100,
    'vmin': pixel[2] - 100,
    'vmax': pixel[2] + 100
}
strict_ranges = [
    (strict['hmin'], strict['smin'], strict['vmin']),
    (strict['hmax'], strict['smax'], strict['vmax'])
]
loose_ranges = [
    (loose['hmin'], loose['smin'], loose['vmin']),
    (loose['hmax'], loose['smax'], loose['vmax'])
]
display = scv.Display()

history = []

tracker = Tracker()

while display.isNotDone():
    img = video.getImage()
    img = img.toHSV()

    #apply strict range, find biggest blob
    #near the biggest blob apply loose range



    res = cv2.inRange(img.getNumpyCv2(), np.array(strict_ranges[0]), np.array(strict_ranges[1]))

    simg = scv.Image(res.transpose(1, 0))

    blobs = simg.findBlobs()
    if blobs:
        x = int(blobs[0].minRectX() - 20)
        if x < 0:
            x = 0
        y = int(blobs[0].minRectY() - 20)
        if y < 0:
            y = 0
        w = int(blobs[0].minRectWidth() + 40)
        h = int(blobs[0].minRectHeight() + 40)
        bb = (x, y, w, h)
        # print x,y,w,h
        cropped = img.crop(bb)
        # print cropped.width, cropped.height
        loose_res = cv2.inRange(cropped.getNumpyCv2(), np.array(loose_ranges[0]), np.array(loose_ranges[1]))

        for i in range(y, y+cropped.height):
            for j in range(x, x+cropped.width):
                temp = loose_res[i - y, j - x]
                res[i, j] = temp
        simg = scv.Image(res.transpose(1, 0))



    simg = simg.morphClose()
    simg = simg.morphOpen()


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