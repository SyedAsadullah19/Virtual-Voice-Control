import cv2
import numpy as np
import time
import math
import HandTracking as hm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
############################################
wCam,hCam=640,480
############################################
cap =cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
detector=hm.handDetector(detectionCon=0.5)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()
minVol=int(volRange[0])
maxVol=int(volRange[1])
pTime=0
vol=0
while True:
    sucess, img = cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=True)
    if len(lmList)!=0:
        #print(lmList[4],lmList[8])
        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]
        cx,cy=(x1+x2)//2,(y1+y1)//2
        cv2.circle(img,(x1,y1),15,(0,255,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(0,255,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(0,255,255),3)
        cv2.circle(img,(cx,cy),15,(0,255,255),cv2.FILLED)
        length=math.hypot(x2-x1,y2-y2)
        #print(length)
        # HandRange=0-100
        # VolumeRange=-65-0
        vol=np.interp(length,[0,100],[minVol,maxVol])
        volBar=np.interp(length,[0,100],[400,120])
        volPer=np.interp(length,[0,100],[0,100])
        volume.SetMasterVolumeLevel(vol, None)
        if length<50:
            cv2.circle(img,(cx,cy),15,(0,155,0),cv2.FILLED)
        cv2.rectangle(img,(20,120),(90,400),(0,195,0),3)
        cv2.rectangle(img,(20,int(volBar)),(90,400),(0,195,0),cv2.FILLED)
        cv2.putText(img,f'{int(volPer)}%',(20,100),cv2.FONT_HERSHEY_COMPLEX,0.6,(0,0,255),3)
    #print(lmList)
    cTime=time.time()
    fps=1/cTime-pTime
    pTime=cTime
    cv2.putText(img,f'{int(fps)}',(40,78),cv2.FONT_HERSHEY_COMPLEX,0.6,(355,0,255),1)
    cv2.imshow('img',img)
    cv2.waitKey(1)
