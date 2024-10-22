import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)


    if results.multi_hand_landmarks:
        for lms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, lms, mpHands.HAND_CONNECTIONS)
            for id, lm, in enumerate(lms.landmark):
                #print(id, lm)

                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)


    cv2.imshow("Image", img)
    cv2.waitKey(1)