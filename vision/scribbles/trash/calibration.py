import SimpleCV as scv



video = scv.Camera()
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
print img.getPixel(img.width/2, img.height/2)