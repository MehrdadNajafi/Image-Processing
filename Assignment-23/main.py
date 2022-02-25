import cv2
import keyboard
import numpy as np

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_detector = cv2.CascadeClassifier('haarcascade_eye.xml')
smile_detector = cv2.CascadeClassifier('haarcascade_smile.xml')

video_cap = cv2.VideoCapture(0)

face_emoji = cv2.imread('emoji.png', 0)
eye_emoji = cv2.imread('eye emoji.png', 0)
lip_emoji = cv2.imread('lip emoji.png', 0)

user_choice = int(input("1-Emoji on face\n2-Eye and lip emoji\n3-Blur face\n4-Flip effect\nNote: Press 'ESC' for close cam and exit program\nPlease choose an option: "))
flag = user_choice

while True:
    if keyboard.is_pressed('1'):
        flag = 1
    elif keyboard.is_pressed('2'):
        flag = 2
    elif keyboard.is_pressed('3'):
        flag = 3
    elif keyboard.is_pressed('4'):
        flag = 4
    elif keyboard.is_pressed('esc'):
        break

    ret, frame = video_cap.read()
    if ret == False:
        break
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    backup_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.putText(frame_gray, '1- Emoji on face', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(frame_gray, '2- Eye and lip emoji', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(frame_gray, '3- Blur face', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(frame_gray, '4- Flip effect', (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(frame_gray, 'esc- exit', (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    if flag == 1:
        faces = face_detector.detectMultiScale(frame_gray, 1.3)
        for face in faces:
            x, y, w, h = face
            new_emoji = cv2.resize(face_emoji, (h, w))
            frame_gray[y:y+h, x:x+w] = new_emoji
            for i in range(y, y+h):
                for j in range(x, x+w):
                    if frame_gray[i, j] == 0:
                        frame_gray[i, j] = backup_frame[i, j]
    
    elif flag == 2:
        faces = face_detector.detectMultiScale(frame_gray, 1.3)
        eyes = eye_detector.detectMultiScale(frame_gray, 1.1, minNeighbors= 8)
        smiles = smile_detector.detectMultiScale(frame_gray, 2.2, minNeighbors=14)
        for eye in eyes:
            x, y, w, h = eye
            new_eye_emoji = cv2.resize(eye_emoji, (w, h))
            frame_gray[y:y+h, x:x+w] = new_eye_emoji
            for i in range(y, y+h):
                for j in range(x, x+w):
                    if frame_gray[i, j] == 0:
                        frame_gray[i, j] = backup_frame[i, j]
        for face in faces:
            x, y, w, h = face
            # cv2.rectangle(frame_gray, (x, y), (x+w, y+h), (0, 0, 0), 4)
            for smile in smiles:
                x2, y2, w2, h2 = smile
                if x <= x2 <= x+h and y <= y2 <= y+h:
                    new_lip_emoji = cv2.resize(lip_emoji, (w2, h2))
                    frame_gray[y2:y2+h2, x2:x2+w2] = new_lip_emoji
                    for i in range(y2, y2+h2):
                        for j in range(x2,x2+w2):
                            if frame_gray[i, j] == 0:
                                frame_gray[i, j] = backup_frame[i, j]

    elif flag == 3:
        faces = face_detector.detectMultiScale(frame_gray, 1.3)
        for face in faces:
            x, y, w, h = face
            # frame_gray[y:y+h, x:x+w] = cv2.blur(frame_gray[y:y+h, x:x+w], (23, 23))
            for i in range(y, y+h, 10):
                for j in range(x, x+w, 10):
                    frame_gray[i:i+10, j:j+10] = frame_gray[i, j]
    
    elif flag == 4:
        height, width = frame_gray.shape
        result = np.zeros((height, width*2), 'uint8')
        result[:, :width] = frame_gray
        result[:, width:width*2] = frame_gray[:, ::-1]
        frame_gray = result

    else:
        print('Index out of range')
        break

    cv2.imshow('cam', frame_gray)
    cv2.waitKey(1)