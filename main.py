#Pauldin Bebla - COEN243
import cv2
import sys
import numpy as np
from alert import email_alert
from threading import Thread
import datetime
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
from imutils.video.pivideostream import PiVideoStream
from PyQt5 import QtGui, QtCore

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads)

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    i=0
    #faceCascade = cv2.CascadeClassifier("C:/Users/Pauldin/PycharmProjects/coen243/venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
    #lowerBodyCascade = cv2.CascadeClassifier("C:/Users/Pauldin/PycharmProjects/coen243/venv/Lib/site-packages/cv2/data/haarcascade_lowerbody.xml")
    #fullBodyCascade = cv2.CascadeClassifier("C:/Users/Pauldin/PycharmProjects/coen243/venv/Lib/site-packages/cv2/data/haarcascade_fullbody.xml")
    #profileFaceCascade = cv2.CascadeClassifier("C:/Users/Pauldin/PycharmProjects/coen243/venv/Lib/site-packages/cv2/data/haarcascade_profileface.xml")
    #cap = cv2.VideoCapture(0)
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    if len(sys.argv)<2:
        print("Not enough arguments.")
        
    
    email = sys.argv[1]
    vs = PiVideoStream(resolution=(352,288), framerate=32).start()
    time.sleep(2.0)
    img1 = vs.read()
    img2 = vs.read()
    while True:
        isDetected = False
        diff = cv2.absdiff(img1, img2)
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(diff_gray, (21,21), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            (x,y,w,h) = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < 900:
                continue
            else:
                isDetected = True
            cv2.rectangle(img2,(x,y), (x+w,y+h), (0,0,255), 2)
        #faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)
        #lowerBody = lowerBodyCascade.detectMultiScale(imgGray, 1.05, 4)
        #fullBody = fullBodyCascade.detectMultiScale(imgGray, 1.4, 6)
        #profileFace = profileFaceCascade.detectMultiScale(imgGray, 1.05, 4)
        detected = ""
        #for(x,y,w,h) in fullBody:
            #cv2.rectangle(img, (x,y), (x+w, y+h), (255,255,0), 2)
        #if len(fullBody)>0:
            #isDetected = True
            #detected +="FullBody "
        #for(x,y,w,h) in lowerBody:
            #cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2)
        #if len(lowerBody)>0:
            #isDetected = True
            #detected +="LowerBody "
        #for(x,y,w,h) in profileFace:
            #cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,255), 2)
        #if len(profileFace)>0:
            #isDetected = True
            #detected +="ProfileFace: "
        #for(x,y,w,h) in faces:
            #cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
            #roi_gray = imgGray[y:y+h, x:x+w]
            #roi_color = img[y:y+h, x:x+w]
            #eyes = eyeCascade.detectMultiScale(roi_gray, scaleFactor=1.4, minNeighbors=6, minSize=(30,30), flags=cv2.CASCADE_SCALE_IMAGE)
        #if len(faces)>1:
            #isDetected=True
            #detected+="Face "
        cv2.imshow("Video", img2)
        if isDetected:
            detected+="Detected"
            thread = Thread(target=email_alert,
                              args=(detected, detected, email, i))
            print(detected, datetime.datetime.now())
            #fourcc = cv2.VideoWriter.fourcc(*'X264')
            #out = cv2.VideoWriter("D:/Users/Pauldin/Videos/output1.mp4", fourcc, 20, (640,360))
            start_time = time.time()
            #while (int(time.time() - start_time) < 10):
                #img = video_getter.frame
                #out.write(img)
                #cv2.imshow("Video", img)
            #out.release()
            #print("Done")
            cv2.imwrite("test%d.png" % i, img2)
            i+=1
            time.sleep(0.1)
            thread.start()
            thread.join()
            time.sleep(10)
            print("Active Now ", datetime.datetime.now())
            img1 = vs.read()
            img2 = vs.read()
        else:
            img1 = img2
            img2 = vs.read()
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            break

    cv2.destroyAllWindows()
    vs.stop()
    #video_getter.stop()
