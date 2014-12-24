import SimpleCV as scv
import cv2

video = scv.Camera()

display = scv.Display()

fgbg = cv2.BackgroundSubtractorMOG(24*60, 1, 0.9, 0.01)

while display.isNotDone():
    img = video.getImage()
    cvimg = fgbg.apply(img.getNumpyCv2())
    simg = scv.Image(cvimg.transpose(1,0))
    simg.save(display)
    if display.mouseRight:
        display.done = True
