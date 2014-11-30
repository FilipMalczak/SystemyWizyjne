import SimpleCV as scv
import cv2
from SimpleCV.base import np
from vision.scribbles import readRanges, saveRanges

video = scv.Camera()

#lower = [21, 23, 0]
#upper = [49, 237, 123]

ranges = readRanges()
lower = ranges[0]
upper = ranges[1]

def setValue(value, list, index):
    list[index] = value

def setHmin(value):
    setValue(value, lower, 0)

def setHmax(value):
    setValue(value, upper, 0)

def setSmin(value):
    setValue(value, lower, 1)

def setSmax(value):
    setValue(value, upper, 1)

def setVmin(value):
    setValue(value, lower, 2)

def setVmax(value):
    setValue(value, upper, 2)



cv2.namedWindow('config')

cv2.createTrackbar("Hmin", 'config', lower[0], 179, setHmin)
cv2.createTrackbar("Hmax", "config", upper[0], 179, setHmax)

cv2.createTrackbar("Smin", 'config', lower[1], 255, setSmin)
cv2.createTrackbar("Smax", "config", upper[1], 255, setSmax)

cv2.createTrackbar("Vmin", 'config', lower[2], 255, setVmin)
cv2.createTrackbar("Vmax", "config", upper[2], 255, setVmax)


display = scv.Display()

while display.isNotDone():
    img = video.getImage()
    img = img.toHSV()
    #img = img.gaussianBlur((5, 5))
    thres = cv2.inRange(img.getNumpyCv2(), np.array(lower), np.array(upper))

    #simg = scv.Image(thres, cv2image=False)
    simg = scv.Image(thres.transpose(1,0))

    #simg = simg.morphOpen()
    simg = simg.morphClose()
    simg = simg.morphOpen()

    #circles = simg.findCircle(thresh=250)
    #if circles:
    #    circles.show(color=scv.Color.RED, width=1)

    simg.save(display)
    if display.mouseRight:
        display.done = True

saveRanges(lower, upper)