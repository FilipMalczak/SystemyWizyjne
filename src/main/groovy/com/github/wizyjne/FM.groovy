package com.github.wizyjne

import org.bytedeco.javacv.CanvasFrame
import org.bytedeco.javacv.FFmpegFrameGrabber
import org.bytedeco.javacv.FrameGrabber

import java.awt.Image

import static com.github.wizyjne.Resources.getExample


FrameGrabber grabber = new FFmpegFrameGrabber(getExample("up-down.avi"));
def frame = new CanvasFrame("Example")
frame.width = grabber.imageWidth
frame.height = grabber.imageHeight
long startTime = System.currentTimeMillis()
int frames = 200
grabber.start()
frame.visible = true
frames.times { int i ->
    Image image = grabber.grab().bufferedImage
    frame.showImage(image)
}
long stopTime = System.currentTimeMillis()
println "$frames frames took ${(stopTime-startTime)/1000.0} s"
