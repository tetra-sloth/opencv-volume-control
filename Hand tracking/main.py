import cv2
import time
import numpy as np
import math

import pycaw

import HandTrackingModule as htp


from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
#print(volume.GetVolumeRange())
#volume.SetMasterVolumeLevel(-20.0, None)


canChange = True


cap = cv2.VideoCapture(0)

detector = htp.handDetector()

changeVol = True

vol = 0
volBar = 400
volPer = 0

pTime = 0

length = 150
mLength = 150

mColor = (0, 255, 0)

while True:
    
    success, img = cap.read()

    img = detector.findHands(img)

    cv2.flip(img, 1)

    lmList = detector.findPosition(img, draw=False)
    #print(lmList)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    if len(lmList) != 0:

        #print(lmList[8], lmList[4])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy, cColor = (x1 + x2)//2, (y1 + y2)//2, (0, 255, 0)
        mx, my = lmList[12][1], lmList[12][2]

        length = math.hypot(x2 - x1, y2 - y1)
        mLength = math.hypot(mx - x2, my - y2)
        print(mLength)

        print(lmList[12])

        if length <= 50:
            cColor = (0, 0, 255)
        else:
            cColor = (0, 255, 0)

        cv2.circle(img, (x2, y2), 10, (0, 255, 0), cv2.FILLED)
        cv2.circle(img, (x1, y1), 10, (0, 255, 0), cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, cColor, cv2.FILLED)
        cv2.circle(img, (mx, my), 10, mColor, cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (0, 255, 0), 3)
        #cv2.line(img, (mx, my), (x2,y2), mColor, 3)

        
        
    cv2.putText(img, f"FPS: {int(fps)}", (40, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)


    if mLength <= 25:
        
        mColor = (255, 0, 255)

        if changeVol == True and canChange == True:

            changeVol = False
            canChange = False

        elif changeVol == False and canChange == True:

            changeVol = True
            canChange = False

        else:
            canChange = True
    else:

        mColor = (0, 0, 255)


    if changeVol == True:

        vol = np.interp(length ,[50, 150], [volume.GetVolumeRange()[0], volume.GetVolumeRange()[1]])
        volBar = np.interp(length, [50, 150], [400, 150])
        volPer = np.interp(length, [50, 150], [0, 100])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(int(vol), None)

    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)



    cv2.imshow("Img", img)
    cv2.waitKey(1)