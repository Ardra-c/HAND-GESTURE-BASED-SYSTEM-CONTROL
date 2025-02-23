import cv2
import time
import numpy as np
import HandtrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 1920, 1080

#Creating a video capture object to return video from first webcam on computer
cap = cv2.VideoCapture(0)
#setting the properties of frame
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)

#Creating object for the default audio output device
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)#activates an interface with the specified interface ID on the audio output device
volume = cast(interface, POINTER(IAudioEndpointVolume))#Casts the IAudioEndpointVolume interface to a pointer 

volRange = volume.GetVolumeRange()#Get the volume output range of the audio output device

minVol = volRange[0]
maxVol = volRange[1]
vol=0
volBar=400
volPer=0
while True:
    success, img = cap.read() #Read a frame 
    img = detector.findHands(img) #returns the processed image with landmarks and hand connections on it
    lmList = detector.findPosition(img, draw=False)#returns a list of x,y coordinates of each hand point. 
    if len(lmList) != 0:

        x1, y1 = lmList[4][1], lmList[4][2]#represents point on thumb
        x2, y2 = lmList[8][1], lmList[8][2]#represents point on index finger
        cx, cy = (x1+x2) // 2, (y1+y2) // 2#fiinding the midpoint 

        cv2.circle(img, (x1, y1), 15, (51, 0, 25), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (51, 0, 25), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (51, 0, 25), 3)
        cv2.circle(img, (cx, cy), 15, (51, 0, 25), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)#Calculating distance between the two points

        #Linear interpolation of the values from input range to output range
        vol = np.interp(length, [50,300], [minVol, maxVol])
        volBar = np.interp(length, [50,300], [400, 150])
        volPer = np.interp(length, [50,300], [0,100])
        
        volume.SetMasterVolumeLevel(vol, None)#set the master volume level of the default audio endpoint
        if(length < 50):
            cv2.circle(img, (cx, cy), 15, (153,0,76), cv2.FILLED)

    cv2.rectangle(img, (50, 150), (85, 400), (25,0,51), 3)#Border of vol bar
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (51,0,102), cv2.FILLED)#vol level 
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (25,0,51), 3)

    cTime = time.time()#current time
    fps = 1/(cTime-pTime)#to calculate frames per second(current time -previous time)
    pTime = cTime        #setting previous time as current time

    cv2.putText(img, f'FPS: {int(fps)}', (40, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (25,0,51), 3)#Display fps
    cv2.imshow("Img", img)
    cv2.waitKey(1)
