package com.github.wizyjne

import org.bytedeco.javacpp.IntPointer
import org.bytedeco.javacv.CanvasFrame
import org.bytedeco.javacv.FFmpegFrameGrabber
import org.bytedeco.javacv.FrameGrabber
import org.bytedeco.javacv.OpenCVFrameGrabber
import org.bytedeco.javacpp.opencv_highgui

import java.awt.Image
import java.nio.IntBuffer

import static com.github.wizyjne.Resources.getExample


//opencv_highgui.namedWindow("control", opencv_highgui.CV_WINDOW_AUTOSIZE)


//int iLowH = 0;
//int iHighH = 179;
int[] iLowH = new int[1]
iLowH[0] = 0
int[] iHighH = new int[1]
iLowH[0] = 179

//int iLowS = 0;
//int iHighS = 255;
int[] iLowS = new int[1]
iLowH[0] = 0
int[] iHighS = new int[1]
iLowH[0] = 255

//int iLowV = 0;
//int iHighV = 255;
int[] iLowV = new int[1]
iLowH[0] = 0
int[] iHighV = new int[1]
iLowH[0] = 255

//Create trackbars in "Control" window
//cvCreateTrackbar("LowH", "Control", &iLowH, 179); //Hue (0 - 179)
//cvCreateTrackbar("HighH", "Control", &iHighH, 179);

//opencv_highgui.cvCreateTrackbar("LowH", "control", iLowH, 179)
//opencv_highgui.cvCreateTrackbar("HighH", "control", iHighH, 179)

//cvCreateTrackbar("LowS", "Control", &iLowS, 255); //Saturation (0 - 255)
//cvCreateTrackbar("HighS", "Control", &iHighS, 255);

//opencv_highgui.cvCreateTrackbar("LowS", "control", iLowS, 255)
//opencv_highgui.cvCreateTrackbar("HighS", "control", iHighS, 255)

//cvCreateTrackbar("LowV", "Control", &iLowV, 255); //Value (0 - 255)
//cvCreateTrackbar("HighV", "Control", &iHighV, 255);

//opencv_highgui.cvCreateTrackbar("LowV", "control", iLowV, 255)
//opencv_highgui.cvCreateTrackbar("HighV", "control", iHighV, 255)



//FrameGrabber grabber = new FFmpegFrameGrabber(getExample("up-down.avi"));
FrameGrabber grabber = new OpenCVFrameGrabber(getExample("circle.avi"))
def frame = new CanvasFrame("Example")
//frame.width = grabber.imageWidth
//frame.height = grabber.imageHeight
long startTime = System.currentTimeMillis()
grabber.start()
int frames = grabber.lengthInFrames-2       // nie wiem czemu, ale jak jest wiecej klatek to umiera
frame.visible = true

frames.times { int i ->
    Image image = grabber.grab().bufferedImage
//    opencv_highgui.imshow("example", grabber.grab().asCvMat())
    frame.showImage(image)
}

grabber.stop()
long stopTime = System.currentTimeMillis()
println "$frames frames took ${(stopTime-startTime)/1000.0} s"
frame.dispose()
