import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import numpy as  np
import serial

ser=serial.Serial('/dev/ttyACM0', 9600)
time.sleep(1)

pos1=90
pos2=90
pos3=90
pos4=90
step=2

resX=320
resY=240

mov_thresh_x = resX/20;
mov_thresh_y = resY/20;

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

camera=PiCamera()
camera.resolution=(resX,resY)
camera.framerate=5

output=PiRGBArray(camera, size=(resX,resY))

time.sleep(0.1)

while 1:
    for frame in camera.capture_continuous(output, format='bgr', use_video_port=True):
        img=output.array
        grey=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces1 = face_cascade.detectMultiScale(grey, 1.3, 5)
         
        for (x,y,w,h) in faces1:
                           
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_grey=grey[y:y+h, x:x+w]
            roi_color=img[y:y+h, x:x+w]

            posX=x+w/2
            posY=y+h/2
            if pos3 >179:
                ser.write(bytes([3]))
                ser.write(bytes([160]))
                time.sleep(0.01)
                ser.write(bytes([4]))
                ser.write(bytes([160]))
                pos3 = 160
                pos4 = 160
                
            if pos3 < 1:
                ser.write(bytes([3]))
                ser.write(bytes([20]))
                time.sleep(0.01)
                ser.write(bytes([4]))
                ser.write(bytes([20]))
                pos3 = 20
                pos4 = 20
                
            if posX > ((resX/2) + mov_thresh_x):
                pos3=pos3-step
                pos4=pos4-step
                ser.write(bytes([3]))
                ser.write(bytes([pos3]))
                time.sleep(0.01)
                ser.write(bytes([4]))
                ser.write(bytes([pos4]))
                #print("+x")
            elif posX < ((resX/2) - mov_thresh_x):
                pos3=pos3+step
                pos4=pos4+step
                ser.write(bytes([3]))
                ser.write(bytes([pos3]))
                time.sleep(0.01)
                ser.write(bytes([4]))
                ser.write(bytes([pos4]))
                #print("-x")
            time.sleep(0.00001)
            if pos1 >179:
                ser.write(bytes([1]))
                ser.write(bytes([160]))
                time.sleep(0.01)
                ser.write(bytes([2]))
                ser.write(bytes([160]))
                pos1 = 160
                pos2 = 160
                
            if pos1 < 1:
                ser.write(bytes([1]))
                ser.write(bytes([20]))
                time.sleep(0.01)
                ser.write(bytes([2]))
                ser.write(bytes([20]))
                pos1 = 20
                #pos2 = 20
                
            if posY < ((resY/2) - mov_thresh_y):
                pos1=pos1+step
                pos2=pos2+step
                ser.write(bytes([1]))
                ser.write(bytes([pos1]))
                time.sleep(0.01)
                ser.write(bytes([2]))
                ser.write(bytes([pos2]))
                #print("+y")
            elif posY > ((resY/2)+ mov_thresh_y):
                pos1=pos1-step
                pos2=pos2-step
                ser.write(bytes([1]))
                ser.write(bytes([pos1]))
                time.sleep(0.01)
                ser.write(bytes([2]))
                ser.write(bytes([pos2]))
                #print("-y")
            time.sleep(0.00001)

        #print(pos1," ",pos2," ",pos3," ",pos4," ")

        cv2.imshow('img',img)
        k=cv2.waitKey(1)&0xFF
        output.truncate(0)
        if k==ord("q"):
            ser.write(bytes([1]))
            ser.write(bytes([90]))
            time.sleep(0.01)
            ser.write(bytes([2]))
            ser.write(bytes([90]))

            ser.write(bytes([3]))
            ser.write(bytes([90]))
            time.sleep(0.01)
            ser.write(bytes([4]))
            ser.write(bytes([90]))
            break
        #time.sleep(0.01)

    break

