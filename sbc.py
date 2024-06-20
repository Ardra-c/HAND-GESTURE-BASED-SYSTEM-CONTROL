import cv2 as cv
import numpy as np
import screen_brightness_control as sbc
from cvzone.HandTrackingModule import HandDetector

cap=cv.VideoCapture(0)#Creating a video capture object to return video from first webcam on computer
hd=HandDetector()#creating an instance of the HandDetector class
val=0
while 1:
    _,img= cap.read()#read a frame
    hands,img= hd.findHands(img)#method of the HandDetector class 
                                #takes an image or video frame as input 
                                #returns (a tuple containing the positions of all the hands detected) &
                                        #(the processed image with the hand landmarks and bounding boxes drawn).
    
    if hands:
        lm= hands[0]['lmList']# access the landmark coordinates for the first detected hand in the image 
                              # hands is a list of dictionaries containing information about all the hands detected in the input image
                              # lmList is a key in each dictionary that contains a list of landmark coordinates for the hand.
        
        length,info,img=hd.findDistance(lm[8][0:2],lm[4][0:2],img)#length-distance between tip of thumb and index finger
                                                                  #info-additional info like coordintes of midpoint & line connecting landmarks
        
        blevel=np.interp(length,[25,145],[0,100])#interpolation to show %
        val=np.interp(length,[25,145],[400,150])#interpolation to show level
        blevel=int(blevel)
        
        sbc.set_brightness(blevel)
        cv.rectangle(img,(20,150),(85,400),(139,139,0),4)
        cv.rectangle(img,(20,int(val)),(85,400),(255,255,153),-1)
        cv.putText(img,str(blevel)+'%',(20,430),cv.FONT_HERSHEY_COMPLEX,1,(255,255,153),3)
    
    cv.imshow('frame',img)
    cv.waitKey(1)
    
    
    