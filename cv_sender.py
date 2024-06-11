import cv2
import mediapipe as mp
import time
import numpy as np
import zmq

port = input("Port: ")

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=1,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

onScreen = False
old_loc = np.array([0,0,0])

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect("tcp://localhost:"+port)

while True:
    success, img = cap.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:

        handLms = results.multi_hand_landmarks[0]
        locs = []
        for lm in handLms.landmark:
            locs.append([lm.x, lm.y,lm.z])
        loc = np.sum(locs,0)/len(locs)

        if onScreen:
            delta = np.add(loc,-1*old_loc)
        else:
            delta = np.array([0,0,0])
        old_loc = loc
        onScreen = True
        print(np.round(delta,2))
        outString = str(delta[0])+","+str(delta[1])+","+str(delta[2])

        mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    else:
        old_loc = None
        onScreen = False
        outString = "0,0,0"



    socket.send(bytes(outString, 'utf-8'))

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)