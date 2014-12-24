from SimpleCV import *

from trash.vision.scribbles import Trackbars

# Example for CAMShift Tracker
def foo(image):
    return image.meanColor()

def camshift(lower, upper):
    cam = Camera()
    img = cam.getImage()
    d = Display(img.size())
    bb1 = getBBFromUser(cam,d)
    fs1=[]

    while d.isNotDone():
        img1 = cam.getImage()
        fs1 = img1.track("camshift", fs1, img, bb1, lower=lower, upper=upper)
        fs1.drawBB()
        fs1.drawPath()
        #fs1.showCoordinates()
        #fs1.showSizeRatio()
        #fs1.showPixelVelocity()
        #fs1.showPixelVelocityRT()
        img1.show()
        if d.mouseRight:
            d.done = True


def getBBFromUser(cam, d):
    p1 = None
    p2 = None
    h= 100
    w = 100
    img = cam.getImage()
    x = (img.width/2) - (w/2)
    y = (img.height/2) - (h/2)
    while d.isNotDone():
        try:
            img = cam.getImage()
            img.drawRectangle(x, y, w, h)
            img.save(d)


            dwn = d.leftButtonDownPosition()
            up = d.leftButtonUpPosition()

            if dwn:
                p1 = dwn
            if up:
                p2 = up
                break

            time.sleep(0.05)
        except KeyboardInterrupt:
            break
    #print p1,p2
    #if not p1 or not p2:
    #    return None

    #xmax = np.max((p1[0],p2[0]))
    #xmin = np.min((p1[0],p2[0]))
    #ymax = np.max((p1[1],p2[1]))
    #ymin = np.min((p1[1],p2[1]))
    #print xmin,ymin,xmax,ymax


    return (x, y, w, h)

tbars = Trackbars()
ranges = tbars.getFromUser()
camshift(ranges[0], ranges[1])
