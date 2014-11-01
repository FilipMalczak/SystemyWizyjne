import SimpleCV as scv


#video = scv.VirtualCamera('e:\Downloads\Fenka.MP4', 'video')
video = scv.Camera()
print video.getAllProperties()
display = scv.Display()
while display.isNotDone():
    img = video.getImage()
    try:
        img = img.gaussianBlur(sigmaX=1, sigmaY=1)
        img.save(display)
    except KeyboardInterrupt:
        display.done = True
        #break
    if display.mouseRight:
        display.done = True
display.quit()
