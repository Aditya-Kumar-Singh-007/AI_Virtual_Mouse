import cv2
import autopy
import time
import numpy as np
import HandTrackingModule as htm
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import os

# Volume control setup
try:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volRange = volume.GetVolumeRange()
    minVol = volRange[0]
    maxVol = volRange[1]
except:
    volume = None

############################
wCam, hCam = 640, 480   ##width and height of the space to move our hands
frameR = 100 # Frame Reduction
smoothening = 7  #smoothing the movement of mouse it shows how fast the mouse would respond
############################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1, detectionCon=0.8, trackCon=0.8)
wScr, hScr = autopy.screen.size()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList)!=0:
        x1, y1 = lmList[8][1:]  # Index finger
        x2, y2 = lmList[12][1:] # Middle finger
        x3, y3 = lmList[4][1:]  # Thumb
        x4, y4 = lmList[20][1:] # Pinky

        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
        
        # 1. Only index Finger: Moving Mode
        if fingers[1] == 1 and fingers[2] == 0 and fingers[0] == 0:
            x_mapped = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
            y_mapped = np.interp(y1, (frameR, hCam-frameR), (0, hScr))
            clocX = plocX +(x_mapped -plocX) /smoothening
            clocY = plocY + (y_mapped - plocY) / smoothening
            autopy.mouse.move(wScr-clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # 2. Left Click: Index and Middle finger meet
        elif fingers[1] == 1 and fingers[2] == 1 and fingers[0] == 0:
            length = detector.findDistance(8, 12, img)[0]
            if length < 40:
                cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

        # 3. Right Click: Thumb and Index finger meet
        elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0:
            length = detector.findDistance(4, 8, img)[0]
            if length < 40:
                cv2.circle(img, (x3, y3), 15, (0, 0, 255), cv2.FILLED)
                autopy.mouse.click(autopy.mouse.Button.RIGHT)

        # 4. Volume Control: All fingers closed (fist)
        elif fingers == [0, 0, 0, 0, 0]:
            vol_level = np.interp(y1, (frameR, hCam-frameR), (100, 0))
            if volume:
                vol = np.interp(vol_level, [0, 100], [minVol, maxVol])
                volume.SetMasterVolumeLevel(vol, None)
            cv2.putText(img, f'Volume: {int(vol_level)}%', (40, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # 5. Brightness Control: Only pinky up
        elif fingers == [0, 0, 0, 0, 1]:
            bright_level = np.interp(y4, (frameR, hCam-frameR), (100, 0))
            try:
                os.system(f'powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{int(bright_level)})')
            except:
                pass
            cv2.putText(img, f'Brightness: {int(bright_level)}%', (40, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        # 6. Scroll: Only thumb up
        elif fingers == [1, 0, 0, 0, 0]:
            if y3 < hCam//2:
                try:
                    autopy.mouse.scroll(3)
                except:
                    pass
                cv2.putText(img, 'Scroll Up', (40, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            else:
                try:
                    autopy.mouse.scroll(-3)
                except:
                    pass
                cv2.putText(img, 'Scroll Down', (40, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

        # 7. All fingers open: No action
        elif fingers == [1, 1, 1, 1, 1]:
            cv2.putText(img, 'No Action', (40, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (128, 128, 128), 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (40, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)

    cv2.imshow("Img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()